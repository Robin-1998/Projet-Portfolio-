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

// Fonction générique pour créer une icône
const createCategoryIcon = (emoji, colorClass) => {
  return L.divIcon({
    className: `custom-marker-${colorClass}`,
    html: `
      <div class="marker-icon marker-${colorClass}">
        <span class="marker-emoji">${emoji}</span>
      </div>
    `,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -14]
  });
};



// ========== COMPOSANT POUR DÉTECTER LES CLICS AVEC COORDONNEES  ==========
/*
const CoordinatesFinder = ({ mapHeight, onCoordinatesUpdate }) => {
  console.log('CoordinatesFinder monté');

  useMapEvents({
    click: (e) => {
      console.log('Event complet:', e);

      const { lat, lng } = e.latlng;
      const pixelX = Math.round(lng);
      const pixelY = Math.round(mapHeight - lat);

      console.log('Coordonnées en pixels:', { x: pixelX, y: pixelY });
      console.log('Coordonnées Leaflet:', { lat, lng });

      onCoordinatesUpdate({ x: pixelX, y: pixelY, lat, lng });

      alert(`Coordonnées: X=${pixelX}, Y=${pixelY}`);
    },
  });

  return null;
};
*/

const Map2 = () => {
  const [markers, setMarkers] = useState([]); // Liste des marqueurs
  const [polygons, setPolygons] = useState([]); // Liste des polygones
  const [loading, setLoading] = useState(true); // État de chargement
  const [error, setError] = useState(null); // Gestion des erreurs
  // const [clickedCoords, setClickedCoords] = useState(null); // Pour réactives CoordinatesFinder uniquement pour gérer les click

  const MAP_WIDTH = 5658; // Largeur en pixels de la carte
  const MAP_HEIGHT = 3633; // Hauteur en pixels de la carte

  const bounds = [
    [0, 0],
    [MAP_HEIGHT, MAP_WIDTH],
  ]; // Définition des limites de l’image (pour l’affichage CRS.Simple)

  const pixelToLeaflet = (x, y) => {
    return [MAP_HEIGHT - y, x]; // Convertit des coordonnées pixels en coordonnées Leaflet
  };

   // Fonction pour charger les données depuis l’API backend
  const chargerDonneesCarte = async () => {
    try {
      setLoading(true); // Active le mode chargement
      setError(null); // Réinitialise les erreurs

      const response = await fetch('http://localhost:5000/api/v1/map/data'); // Appel API backend

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`); // Gère les erreurs HTTP
      }

      const result = await response.json(); // Parse la réponse JSON

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
        }));

        // Transformation des régions (liste de points)
        const transformedPolygons = mapData.regions.map((region) => ({
          id: region.id,
          name: region.name,
          positions: region.geometry.coordinates.map((coord) =>
            pixelToLeaflet(coord[0], coord[1])
          ),
          placeId: region.place_id,
        }));

        setMarkers(transformedMarkers); // Met à jour les marqueurs
        setPolygons(transformedPolygons); // Met à jour les polygones
      } else {
        throw new Error('Échec du chargement des données'); // Erreur personnalisée si échec du backend
      }
    } catch (error) {
      console.error('Erreur lors du chargement:', error); // Log de l’erreur
      setError(error.message); // Stocke l’erreur dans l’état
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
          🔄 Réessayer
        </button>
      </div>
    );
  }

  console.log('🗺️ Rendu de la carte, image:', terre_du_milieu);

  return (
    <div
      className="map2-conteneur-carte"
      style={{
        width: '100%',
        height: '100%',
        position: 'relative',
        margin: 0,
        padding: 0,
      }}
    >
      {/* ========== AFFICHAGE DES COORDONNÉES ========== */}
      {/*
      {clickedCoords ? (
        <div className="map2-coords-display">
          <strong>Coordonnées : </strong>
          <span className="map2-coords-value">
            X: {clickedCoords.x} | Y: {clickedCoords.y}
          </span>
        </div>
      ) : (
        <div className="map2-coords-hint">Cliquez sur la carte</div>
      )}
      */}

      <MapContainer
        center={[MAP_HEIGHT / 2, MAP_WIDTH / 2]}
        zoom={-3}
        crs={L.CRS.Simple}
        className="map2-conteneur"
        minZoom={-4}
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
      >
        <ImageOverlay
          url={terre_du_milieu}
          bounds={bounds}
          interactive={false}
        />

        {/* ========== DÉTECTION DES CLICS ========== */}
        {/*
        <CoordinatesFinder
          mapHeight={MAP_HEIGHT}
          onCoordinatesUpdate={setClickedCoords}
        />
        */}

        {polygons.map((polygon) => (
          <Polygon
            key={polygon.id}
            positions={polygon.positions}
            pathOptions={{
              color: 'black',
              fillColor: '#403221',
              fillOpacity: 0.1,
              weight: 1,
            }}
          >
            <Popup>
              <div className="map2-popup">
                <h3 className="map2-popup-title">{polygon.name}</h3>
                <p className="map2-popup-info">Place ID: {polygon.placeId}</p>
              </div>
            </Popup>
          </Polygon>
        ))}

        {markers.map((marker) => (
          <Marker key={marker.id} position={marker.position}>
            <Popup>
              <div className="map2-popup">
                <h3 className="map2-popup-title">{marker.name}</h3>
                <p className="map2-popup-info">Place ID: {marker.placeId}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default Map2;
