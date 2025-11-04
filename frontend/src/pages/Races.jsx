/**
 * @module Races
 * Page affichant la liste des races dans un corps de page.
 */

import BodyPage from '../components/static_components/Body_page';
import RacesList from '../components/dynamic_components/Races_list';

/**
 * Composant de page pour la section "Races".
 * @returns {JSX.Element} Conteneur affichant la liste des races.
 */
function Races() {
  return (
    <>
      <BodyPage>
        <RacesList />
      </BodyPage>
    </>
  );
}

export default Races
