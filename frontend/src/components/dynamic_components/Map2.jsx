/**
 * Composant de carte interactive de la Terre du Milieu
 * @module Map2
 */

import React, { useState, useEffect } from 'react';
import {
  MapContainer,
  Marker,
  Popup,
  Polygon,
  ImageOverlay,
  useMapEvents,
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { CATEGORY_ICONS } from './Bulle_map.jsx';
import DetailPlace from './Detail_place.jsx';

// Chemin vers l'image de fond de la carte
const terre_du_milieu = '/public/terre_du_milieu.jpg';

// Configuration des icônes Leaflet par défaut (pour éviter les erreurs d'affichage)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

/**
 * Affiche une carte interactive de la Terre du Milieu avec marqueurs et régions cliquables
 * Gère le zoom adaptatif des icônes et l'affichage de détails en modal
 *
 * @component
 * @returns {JSX.Element} Carte interactive Leaflet
 */
const Map2 = () => {
  // États pour les données de la carte
  const [markers, setMarkers] = useState([]);          // Liste des marqueurs sur la carte
  const [polygons, setPolygons] = useState([]);       // Liste des polygones (régions)
  const [loading, setLoading] = useState(true);       // Indique si la carte est en cours de chargement
  const [error, setError] = useState(null);           // Message d'erreur si la récupération échoue
  const [iconSize, setIconSize] = useState(30);       // Taille des icônes des marqueurs (adaptative)

  // États pour la modal de détails
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [detailedInfo, setDetailedInfo] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);

  // Dimensions de l'image de la carte en pixels
  const MAP_WIDTH = 5658; // Largeur en pixels de l'image
  const MAP_HEIGHT = 3633; // Hauteur en pixels de l'image

  // Limites de la carte pour Leaflet (système de coordonnées simple)
  const bounds = [
    [0, 0],
    [MAP_HEIGHT, MAP_WIDTH],
  ];

  /**
   * Convertit des coordonnées pixel (x, y) en coordonnées Leaflet
   * Leaflet utilise un système de coordonnées inversé pour l'axe Y
   *
   * @param {number} x - Coordonnée X en pixels
   * @param {number} y - Coordonnée Y en pixels
   * @returns {Array<number>} Coordonnées Leaflet [lat, lng]
   */
  const pixelToLeaflet = (x, y) => {
    return [MAP_HEIGHT - y, x];
  };

  /**
   * Récupère les descriptions détaillées d'une entité depuis l'API
   *
   * @async
   * @param {string} entityType - Type d'entité ('region', 'ville', 'montagne', etc.)
   * @param {number|string} entityId - ID de l'entité
   * @returns {Promise<Array>} Liste des descriptions ou tableau vide si erreur
   */
  const fetchDescriptions = async (entityType, entityId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/descriptions/${entityType}/${entityId}`);
      const data = await response.json();
	  if (!data.success) return []; // Retourne tableau vide si erreur API
      return data.data;
    } catch (err) {
      console.error('Erreur lors du chargement des descriptions:', err);
      return [];
    }
  };

/**
 * Charge les informations détaillées d'un lieu et affiche la modal
 * Normalise le type de lieu (retire les accents) et récupère les descriptions
 *
 * @async
 * @param {number} placeId - ID du lieu
 * @param {string} placeName - Nom du lieu
 * @param {string} placeDescription - Description courte
 * @param {Object} placeDetails - Détails additionnels
 * @param {string} placeType - Type de lieu (région, ville, etc.)
 */
const loadPlaceDetails = async (placeId, placeName, placeDescription, placeDetails, placeType) => {
  setLoadingDetails(true);
  try {
    // Normalisation du type : retire les accents (ex: "région" → "region")
    // Nécessaire pour la cohérence avec l'API
    const typeNormalized = placeType.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

    // Récupération des descriptions liées
    const descriptions = await fetchDescriptions(typeNormalized, placeId);

    // Récupération des détails supplémentaires depuis l'API
    const response = await fetch(`http://localhost:5000/api/v1/map/places/${placeId}/details`);
    const result = await response.json();

    if (result.success) {
      // Combine toutes les informations pour la modal
      setDetailedInfo({
        name: placeName,
        description: placeDescription,
        details: placeDetails,
        type: typeNormalized,
        descriptions,
        ...result.data
      });
    }
  } catch (error) {
    console.error('Erreur lors du chargement des détails:', error);
  } finally {
    setLoadingDetails(false);
  }
};

  /** Ferme la modal de détails */
  const closeDetailedView = () => {
    setDetailedInfo(null);
  };

/**
 * Charge les données de la carte depuis l'API backend
 * Récupère les marqueurs et régions, puis les transforme pour Leaflet
 *
 * @async
 */
const chargerDonneesCarte = async () => {
  try {
    setLoading(true);
    setError(null);

    const response = await fetch('http://localhost:5000/api/v1/map/data');
    if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

    const result = await response.json();

    if (result.success) {
      const mapData = result.data;

      // Transformation des marqueurs pour Leaflet
      // Pour chaque marqueur, on charge aussi ses descriptions
      const transformedMarkers = await Promise.all(
        mapData.markers.map(async (marker) => {
          // Normalisation du type pour enlever les accents
          const normalizedType = (marker.type || 'default').normalize("NFD").replace(/[\u0300-\u036f]/g, "");
          const descriptions = await fetchDescriptions(normalizedType, marker.place_id);

          return {
            id: marker.id,
            name: marker.name,
            // Conversion des coordonnées pixel vers Leaflet
            position: pixelToLeaflet(
              marker.geometry.coordinates[0],
              marker.geometry.coordinates[1]
            ),
            placeId: marker.place_id,
            type: normalizedType,
            description: marker.description || "Aucune description disponible",
            details: marker.details || {},
            descriptions,
          };
        })
      );

      // Transformation des polygones (régions) pour Leaflet
      const transformedPolygons = await Promise.all(
        mapData.regions.map(async (region) => {
          // Normaliser le type "région" pour enlever les accents
          const normalizedType = 'région'.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
          const descriptions = await fetchDescriptions(normalizedType, region.place_id);

          return {
            id: region.id,
            name: region.name,
            // Chaque coordonnée du polygone doit être convertie
            positions: region.geometry.coordinates.map((coord) =>
              pixelToLeaflet(coord[0], coord[1])
            ),
            placeId: region.place_id,
            description: region.description || "Aucune description disponible",
            details: region.details || {},
            descriptions,
          };
        })
      );

      // Mise à jour des états
      setMarkers(transformedMarkers);
      setPolygons(transformedPolygons);
    } else {
      throw new Error('Échec du chargement des données');
    }
  } catch (error) {
    console.error('Erreur lors du chargement:', error);
    setError(error.message);
  } finally {
    setLoading(false);
  }
};

  /**
   * Effet pour charger les données de la carte au montage du composant
   */
  useEffect(() => {
    chargerDonneesCarte(); // Charge les marqueurs et polygones au démarrage
  }, []);

  // Affichage pendant le chargement
  if (loading) {
    return (
      <div className="map2-loading">
        <div className="map2-loading-content">
          <div className="map2-spinner"></div>
          <p>Chargement de la carte...</p>
        </div>
      </div>
    );
  }

  // Affichage en cas d'erreur
  if (error) {
    return (
      <div className="map2-error-conteneur">
        <div className="map2-error-box">
          <p className="map2-error-text">❌ Erreur: {error}</p>
        </div>
        <button onClick={chargerDonneesCarte} className="map2-retry-button">
          Réessayer
        </button>
      </div>
    );
  }

  /**
   * Composant interne pour gérer le zoom adaptatif des icônes
   * Écoute les événements de zoom et ajuste la taille des icônes en conséquence
   *
   * @component
   * @param {Object} props
   * @param {Function} props.setIconSize - Fonction pour mettre à jour la taille des icônes
   * @returns {null} Ne rend rien visuellement
   */
  function ZoomAdaptiveIcons({ setIconSize }) {
    const map = useMapEvents({
      // Met à jour la taille des icônes lors d'un zoom
      zoom: () => {
        const zoom = map.getZoom();
        const newSize = computeIconSize(zoom);
        setIconSize(newSize);
      },
      // Initialisation de la taille des icônes au chargement
      load: () => {
        const zoom = map.getZoom();
        const newSize = computeIconSize(zoom);
        setIconSize(newSize);
      },
    });

    return null; // Ne rend rien visuellement
  }

  /**
   * Calcule la taille des icônes en fonction du niveau de zoom
   * Plus on zoom, plus les icônes sont grandes (dans une limite)
   *
   * @param {number} zoom - Niveau de zoom actuel
   * @returns {number} Taille de l'icône en pixels (entre 30 et 96)
   */
  function computeIconSize(zoom) {
    const minSize = 30;  // Taille minimale
    const maxSize = 96;  // Taille maximale
    const baseSize = 30; // Taille de base
    const factor = 8;    // Facteur de multiplication

    // Formule : taille = base + (zoom + 3) * facteur
    let size = baseSize + (zoom + 3) * factor;

    // On limite entre minSize et maxSize
    size = Math.max(minSize, Math.min(maxSize, size));

    return size;
  }

  return (
    <div className="map2-conteneur-carte">
      <MapContainer
        center={[MAP_HEIGHT / 2, MAP_WIDTH / 2]} // Centre de la carte
        zoom={-3}                                 // Zoom initial (négatif car image grande)
        crs={L.CRS.Simple}                        // Système de coordonnées simple (pas géographique)
        className="map2-conteneur"
        minZoom={-2.7}                            // Zoom minimum (vue complète)
        maxZoom={0}                               // Zoom maximum (vue détaillée)
        zoomControl={true}                        // Afficher les boutons +/-
        dragging={true}                           // Permettre le déplacement
        scrollWheelZoom={true}                    // Permettre le zoom à la molette
        doubleClickZoom={true}                    // Permettre le zoom au double-clic
        touchZoom={true}                          // Permettre le zoom tactile
        boxZoom={false}                           // Désactiver le zoom par sélection
        keyboard={false}                          // Désactiver les raccourcis clavier
        maxBounds={bounds}                        // Limites de la carte
        maxBoundsViscosity={1.0}                  // Empêcher de sortir des limites
        attributionControl={false}                // Masquer les crédits Leaflet
      >
        {/* Composant pour adapter la taille des icônes au zoom */}
        <ZoomAdaptiveIcons setIconSize={setIconSize} />

        {/* Image de fond de la carte */}
        <ImageOverlay
          url={terre_du_milieu}
          bounds={bounds}
          interactive={false}
        />

        {/* Affichage des régions (polygones) */}
        {polygons.map((polygon) => (
          <Polygon
            key={polygon.id}
            positions={polygon.positions}
            pathOptions={{
              className: 'polygon-style',
              color: 'black',
              fillColor: '#403221',
              fillOpacity: 0,     // Transparent par défaut
              weight: 0,          // Pas de bordure
            }}
          >
            <Popup>
              <div className="map2-popup">
                <h3 className="map2-popup-title">{polygon.name}</h3>
                <p className="map2-popup-description">{polygon.description}</p>

                <button
                  className="map2-popup-details-btn"
                  onClick={() => loadPlaceDetails(
                    polygon.placeId,
                    polygon.name,
                    polygon.description,
                    polygon.details,
                    'région'
                  )}
                >
                  Voir les détails
                </button>
              </div>
            </Popup>
          </Polygon>
        ))}

        {/* Affichage des marqueurs (lieux spécifiques) */}
        {markers.map((marker) => {
          // Sélection de l'icône en fonction du type de lieu
          const iconType = marker.type || "default";
          const icon = CATEGORY_ICONS[iconType]?.(iconSize) || CATEGORY_ICONS.default(iconSize);

          return (
            <Marker key={marker.id} position={marker.position} icon={icon}>
              <Popup>
                <div className="map2-popup">
                  <h3 className="map2-popup-title">{marker.name}</h3>
                  <p className="map2-popup-description">{marker.description}</p>

                  {/* Affichage des détails supplémentaires s'ils existent */}
                  {marker.details && Object.keys(marker.details).length > 0 && (
                    <div className="map2-popup-details">
                      {Object.entries(marker.details).map(([key, value]) => (
                        <p key={key}>
                          <strong>{key}:</strong> {value}
                        </p>
                      ))}
                    </div>
                  )}

                  <button
                    className="map2-popup-details-btn"
                    onClick={() => {
                      loadPlaceDetails(
                        marker.placeId,
                        marker.name,
                        marker.description,
                        marker.details,
                        marker.type
                      );
                    }}
                    disabled={loadingDetails}
                  >
                    {loadingDetails ? 'Chargement...' : 'Voir les détails'}
                  </button>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>

      {/* Modal de détails (affichée quand detailedInfo est défini) */}
      {detailedInfo && (
        <DetailPlace
          place={detailedInfo}
          onClose={closeDetailedView}
        />
      )}
    </div>
  );
};

export default Map2;
