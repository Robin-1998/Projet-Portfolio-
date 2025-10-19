import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon, ImageOverlay, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import terre_du_milieu from '../../assets/terre_du_milieu.jpg';


// Fix pour les icônes de marqueurs Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const Map2 = () => {
  const [markers, setMarkers] = useState([]);
  const [polygons, setPolygons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Dimensions de votre carte image
  const MAP_WIDTH = 5658;
  const MAP_HEIGHT = 3633;

  // Définir bounds
  const bounds = [[0, 0], [MAP_HEIGHT, MAP_WIDTH]];

  // Convertir coordonnées pixel en coordonnées Leaflet
  const pixelToLeaflet = (x, y) => {
    return [MAP_HEIGHT - y, x];
  };

  const chargerDonneesCarte = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:5000/api/v1/map/data');

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const result = await response.json();

      if (result.success) {
        const mapData = result.data;

        // Transformer les markers
        const transformedMarkers = mapData.markers.map(marker => ({
          id: marker.id,
          name: marker.name,
          position: pixelToLeaflet(
            marker.geometry.coordinates[0],
            marker.geometry.coordinates[1]
          ),
          placeId: marker.place_id
        }));

        // Transformer les polygons
        const transformedPolygons = mapData.regions.map(region => ({
          id: region.id,
          name: region.name,
          positions: region.geometry.coordinates.map(coord =>
            pixelToLeaflet(coord[0], coord[1])
          ),
          placeId: region.place_id
        }));

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
      <div className="map2-error-container">
        <div className="map2-error-box">
          <p className="map2-error-text">❌ Erreur: {error}</p>
        </div>
        <button onClick={chargerDonneesCarte} className="map2-retry-button">
          🔄 Réessayer
        </button>
      </div>
    );
  }

  return (
    <MapContainer
      center={[MAP_HEIGHT / 2, MAP_WIDTH / 2]}
      zoom={-3}
      crs={L.CRS.Simple}
      className="map2-container"
      minZoom={-2.5}
      maxZoom={-2.5}
      zoomControl={false}
      dragging={false}
      scrollWheelZoom={false}
      doubleClickZoom={false}
      touchZoom={false}
      boxZoom={false}
      keyboard={false}
      maxBounds={bounds}
      maxBoundsViscosity={1.0}
    >
      <ImageOverlay
        url={terre_du_milieu}
        bounds={bounds}
      />

      {polygons.map((polygon) => (
        <Polygon
          key={polygon.id}
          positions={polygon.positions}
          pathOptions={{
            color: '#ff6b6b',
            fillColor: '#ff6b6b',
            fillOpacity: 0.3,
            weight: 2
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
  );
};

export default Map2;
