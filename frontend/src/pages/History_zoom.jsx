/**
 * @module HistoryZoom
 * Page affichant le détail d’une histoire dans un corps de page.
 */

import BodyPage from '../components/static_components/Body_page';
import HistoryDetail from '../components/dynamic_components/History_details';

/**
 * Composant de page pour le zoom sur une histoire.
 * @returns {JSX.Element} Conteneur affichant le détail d’une histoire.
 */
function HistoryZoom() {
  return (
    <>
      <BodyPage>
        <HistoryDetail />
      </BodyPage>
    </>
  );
}

export default HistoryZoom
