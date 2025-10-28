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

const terre_du_milieu = '/public/terre_du_milieu.jpg';

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
  const [markers, setMarkers] = useState([]);
  const [polygons, setPolygons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [iconSize, setIconSize] = useState(30);

  const [selectedPlace, setSelectedPlace] = useState(null);
  const [detailedInfo, setDetailedInfo] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);

  const MAP_WIDTH = 5658;
  const MAP_HEIGHT = 3633;

  const bounds = [
    [0, 0],
    [MAP_HEIGHT, MAP_WIDTH],
  ];

  const pixelToLeaflet = (x, y) => {
    return [MAP_HEIGHT - y, x];
  };



  // Fonction pour charger les descriptions d'un lieu
  const fetchDescriptions = async (entityType, entityId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/descriptions/${entityType}/${entityId}`);
      const data = await response.json();
	  if (!data.success) return [];
      return data.data;
    } catch (err) {
      console.error('Erreur lors du chargement des descriptions:', err);
      return [];
    }
  };

const loadPlaceDetails = async (placeId, placeName, placeDescription, placeDetails, placeType) => {
  setLoadingDetails(true);
  try {
    // Normaliser le type pour enlever les accents
    const typeNormalized = placeType.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

    // Charger les descriptions avec le type normalisé
    const descriptions = await fetchDescriptions(typeNormalized, placeId);

    // Charger les détails complets depuis l'API
    const response = await fetch(`http://localhost:5000/api/v1/map/places/${placeId}/details`);
    const result = await response.json();

    if (result.success) {
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

  const closeDetailedView = () => {
    setDetailedInfo(null);
  };

  // Fonction pour charger les données depuis l'API backend
const chargerDonneesCarte = async () => {
  try {
    setLoading(true);
    setError(null);

    const response = await fetch('http://localhost:5000/api/v1/map/data');
    if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

    const result = await response.json();

    if (result.success) {
      const mapData = result.data;

      const transformedMarkers = await Promise.all(
        mapData.markers.map(async (marker) => {
          // Normalisation du type pour enlever les accents
          const normalizedType = (marker.type || 'default').normalize("NFD").replace(/[\u0300-\u036f]/g, "");
          const descriptions = await fetchDescriptions(normalizedType, marker.place_id);

          return {
            id: marker.id,
            name: marker.name,
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

      const transformedPolygons = await Promise.all(
        mapData.regions.map(async (region) => {
          // Normaliser le type "région" pour enlever les accents
          const normalizedType = 'région'.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
          const descriptions = await fetchDescriptions(normalizedType, region.place_id);

          return {
            id: region.id,
            name: region.name,
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

  function computeIconSize(zoom) {
    const minSize = 30;
    const maxSize = 96;
    const baseSize = 30;
    const factor = 8;

    let size = baseSize + (zoom + 3) * factor;
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

        {polygons.map((polygon) => (
          <Polygon
            key={polygon.id}
            positions={polygon.positions}
            pathOptions={{
              className: 'polygon-style',
              color: 'black',
              fillColor: '#403221',
              fillOpacity: 0,
              weight: 0,
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

        {markers.map((marker) => {
          const iconType = marker.type || "default";
          const icon = CATEGORY_ICONS[iconType]?.(iconSize) || CATEGORY_ICONS.default(iconSize);

          return (
            <Marker key={marker.id} position={marker.position} icon={icon}>
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
