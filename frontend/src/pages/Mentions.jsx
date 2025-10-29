/**
 * @module Mentions
 * Page affichant les mentions légales.
 */

import BodyPage from '../components/static_components/Body_page';
import MentionsLegales from '../components/dynamic_components/Footer_mentions';

/**
 * Composant de la page des mentions légales.
 * @returns {JSX.Element} Conteneur affichant le contenu des mentions légales.
 */
function Mentions() {
  return (
    <>
      <BodyPage>
        <MentionsLegales />
      </BodyPage>
    </>
  );
}

export default Mentions;
