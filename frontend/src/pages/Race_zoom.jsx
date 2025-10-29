/**
 * @module RaceZoom
 * Page affichant le détail d’une race dans un corps de page.
 */

import BodyPage from '../components/static_components/Body_page';
import RaceDetail from '../components/dynamic_components/Races_details';

/**
 * Composant de page pour le zoom sur une race.
 * @returns {JSX.Element} Conteneur affichant le détail d’une race.
 */
function RaceZoom() {
  return (
    <>
      <BodyPage>
        <RaceDetail />
      </BodyPage>
    </>
  );
}

export default RaceZoom
