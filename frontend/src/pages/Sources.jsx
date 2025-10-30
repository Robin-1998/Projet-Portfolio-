/**
 * @module Sources
 * Page affichant les sources et références.
 */

import BodyPage from '../components/static_components/Body_page';
import MentionsSource from '../components/dynamic_components/Footer_sources';

/**
 * Composant de la page des sources.
 * @returns {JSX.Element} Conteneur affichant les sources et références.
 */
function Sources() {
  return (
    <>
      <BodyPage>
        <MentionsSource />
      </BodyPage>
    </>
  );
}

export default Sources;
