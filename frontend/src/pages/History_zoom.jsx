/**
 * Page affichant le détail d’une histoire dans un corps de page.
 */

import BodyPage from '../components/static_components/Body_page';
import HistoryDetail from '../components/dynamic_components/History_details';

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
