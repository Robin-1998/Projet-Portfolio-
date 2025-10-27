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

// Chemin pour l'image de la carte
const terre_du_milieu = '/public/terre_du_milieu.jpg';

// Fix pour les icônes de marqueurs Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const Map2 = () => {
  const [markers, setMarkers] = useState([]); // Liste des marqueurs
  const [polygons, setPolygons] = useState([]); // Liste des polygones
  const [loading, setLoading] = useState(true); // État de chargement
  const [error, setError] = useState(null); // Gestion des erreurs
  const [iconSize, setIconSize] = useState(30);

  const [selectedPlace, setSelectedPlace] = useState(null);
  const [detailedInfo, setDetailedInfo] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);

  const MAP_WIDTH = 5658; // Largeur en pixels de la carte
  const MAP_HEIGHT = 3633; // Hauteur en pixels de la carte

  const bounds = [
    [0, 0],
    [MAP_HEIGHT, MAP_WIDTH],
  ]; // Définition des limites de l'image (pour l'affichage CRS.Simple)

  const pixelToLeaflet = (x, y) => {
    return [MAP_HEIGHT - y, x]; // Convertit des coordonnées pixels en coordonnées Leaflet
  };

  // Fonction pour charger les détails d'un lieu
  const loadPlaceDetails = async (placeId, placeName, placeDescription, placeDetails, placeType) => {
    setLoadingDetails(true);
    try {
      const response = await fetch(`http://localhost:5000/api/v1/map/places/${placeId}/details`);

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const result = await response.json();

      if (result.success) {
        setDetailedInfo({
          name: placeName,
          description: placeDescription,
          details: placeDetails,
          type: placeType,
          ...result.data // image_url, detailed_sections, etc.
        });
      }
    } catch (error) {
      console.error('Erreur lors du chargement des détails:', error);
      // Affiche quand même les infos de base
      setDetailedInfo({
        name: placeName,
        description: placeDescription,
        details: placeDetails,
        type: placeType,
        detailed_sections: [],
        error: 'Impossible de charger les détails complets'
      });
    } finally {
      setLoadingDetails(false);
    }
  };

  // Fonction pour fermer la modal
  const closeDetailedView = () => {
    setDetailedInfo(null);
  };

  // Fonction pour charger les données depuis l'API backend
  const chargerDonneesCarte = async () => {
    try {
      setLoading(true); // Active le mode chargement
      setError(null); // Réinitialise les erreurs

      const response = await fetch('http://localhost:5000/api/v1/map/data'); // Appel API backend

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`); // Gère les erreurs HTTP
      }

      const result = await response.json(); // extrait la réponse JSON

      if (result.success) {
        const mapData = result.data;

        // Transformation des marqueurs (coordonnées pixels → coordonnées Leaflet)
        const transformedMarkers = mapData.markers.map((marker) => ({
          id: marker.id,
          name: marker.name,
          position: pixelToLeaflet(
            marker.geometry.coordinates[0],
            marker.geometry.coordinates[1]
          ),
          placeId: marker.place_id,
          type: marker.type || "default",
          description: marker.description || "Aucune description disponible",
          details: marker.details || {},
        }));

        // Transformation des régions (liste de points)
        const transformedPolygons = mapData.regions.map((region) => ({
          id: region.id,
          name: region.name,
          positions: region.geometry.coordinates.map((coord) =>
            pixelToLeaflet(coord[0], coord[1])
          ),
          placeId: region.place_id,
          description: region.description || "Aucune description disponible",
          details: region.details || {},
        }));

        setMarkers(transformedMarkers); // Met à jour les marqueurs
        setPolygons(transformedPolygons); // Met à jour les polygones

      } else {
        throw new Error('Échec du chargement des données'); // Erreur personnalisée si échec du backend
      }
    } catch (error) {
      console.error('Erreur lors du chargement:', error); // Log de l'erreur
      setError(error.message); // Stocke l'erreur dans l'état
    } finally {
      setLoading(false); // Désactive le mode chargement
    }
  };

  useEffect(() => {
    chargerDonneesCarte();
  }, []);

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

  // Adapte la taille des icônes en fonction du zoom
  function ZoomAdaptiveIcons({ setIconSize }) {
    const map = useMapEvents({
      zoom: () => {
        const zoom = map.getZoom();
        const newSize = computeIconSize(zoom);
        setIconSize(newSize);
      },
      load: () => {
        const zoom = map.getZoom();
        const newSize = computeIconSize(zoom);
        setIconSize(newSize);
      },
    });

    return null;
  }

  // Fonction pour calculer la taille adaptive des icônes
  function computeIconSize(zoom) {
    const minSize = 30;      // taille minimale
    const maxSize = 96;      // taille maximale
    const baseSize = 30;     // taille de référence
    const factor = 8;        // sensibilité du zoom

    // Formule : taille proportionnelle au zoom
    let size = baseSize + (zoom + 3) * factor; // +3 pour compenser le zoom négatif initial

    // Clamp pour rester entre min et max
    size = Math.max(minSize, Math.min(maxSize, size));

    return size;
  }

  return (
    <div className="map2-conteneur-carte">
      <MapContainer
        center={[MAP_HEIGHT / 2, MAP_WIDTH / 2]}
        zoom={-3}
        crs={L.CRS.Simple}
        className="map2-conteneur"
        minZoom={-2.7}
        maxZoom={0}
        zoomControl={true}
        dragging={true}
        scrollWheelZoom={true}
        doubleClickZoom={true}
        touchZoom={true}
        boxZoom={false}
        keyboard={false}
        maxBounds={bounds}
        maxBoundsViscosity={1.0}
        attributionControl={false}
      >
        <ZoomAdaptiveIcons setIconSize={setIconSize} />

        <ImageOverlay
          url={terre_du_milieu}
          bounds={bounds}
          interactive={false}
        />

        {/* Affichage des Régions */}
        {polygons.map((polygon) => (
          <Polygon
            key={polygon.id}
            positions={polygon.positions}
            pathOptions={{
              className: 'polygon-style',
              color: 'black',
              fillColor: '#403221',
              fillOpacity: 0.1,
              weight: 0,
            }}
          >
            <Popup>
              <div className="map2-popup">
                <h3 className="map2-popup-title">{polygon.name}</h3>
                <p className="map2-popup-description">{polygon.description}</p>

                {/* Bouton pour voir les détails */}
                <button
                  className="map2-popup-details-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    loadPlaceDetails(
                      polygon.placeId,
                      polygon.name,
                      polygon.description,
                      polygon.details,
                      'région'
                    );
                  }}
                >
                  Voir les détails
                </button>
              </div>
            </Popup>
          </Polygon>
        ))}

        {/* Affichage des Marqueurs */}
        {markers.map((marker) => {
          const iconType = marker.type || "default";
          const icon = CATEGORY_ICONS[iconType]?.(iconSize) || CATEGORY_ICONS.default(iconSize);

          return (
            <Marker
              key={marker.id}
              position={marker.position}
              icon={icon}
            >
              <Popup>
                <div className="map2-popup">
                  <h3 className="map2-popup-title">{marker.name}</h3>
                  <p className="map2-popup-description">{marker.description}</p>

                  {marker.details && Object.keys(marker.details).length > 0 && (
                    <div className="map2-popup-details">
                      {Object.entries(marker.details).map(([key, value]) => (
                        <p key={key}>
                          <strong>{key}:</strong> {value}
                        </p>
                      ))}
                    </div>
                  )}

                  {/* Bouton pour voir les détails */}
                  <button
                    className="map2-popup-details-btn"
                    onClick={(e) => {
                      e.stopPropagation();
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

      {/* Modal de détails */}
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
