/**
 * @module Creations
 * Page affichant la liste des créations dans un corps de page.
 */

import BodyPage from '../components/static_components/Body_page';
import CreationsList from '../components/dynamic_components/Creations_list';

/**
 * Composant de page pour la section "Créations".
 * @returns {JSX.Element} Conteneur affichant la liste des créations.
 */
function Creations() {
  return (
    <>
      <BodyPage>
        <CreationsList />
      </BodyPage>
    </>
  );
}
/* Ajouter ImagePost */
export default Creations
