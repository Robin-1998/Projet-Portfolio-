/**
 * @module Home_map
 * Page principale affichant la carte interactive.
 */

import 'leaflet/dist/leaflet.css';
import BodyPage from '../components/static_components/Body_page';
import Map2 from '../components/dynamic_components/Map2';

/**
 * Composant de page pour l’affichage de la carte.
 * @returns {JSX.Element} Conteneur plein écran avec la carte interactive.
 */
function Home_map() {
  return (
    <BodyPage mainClassName="map-fullscreen">
      <Map2 />
    </BodyPage>
  );
}

export default Home_map;
