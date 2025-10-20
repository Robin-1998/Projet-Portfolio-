import 'leaflet/dist/leaflet.css';
import BodyPage from '../components/static_components/Body_page';
import Map2 from '../components/dynamic_components/Map2';

function Home_map() {
  return (
    <BodyPage mainClassName="map-fullscreen">
      <Map2 />
    </BodyPage>
  );
}

export default Home_map;
