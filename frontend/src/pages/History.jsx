/**
 * Page affichant la liste des histoires dans un corps de page.
 */

import BodyPage from '../components/static_components/Body_page';
import HistoryList from '../components/dynamic_components/History_list';

function history() {
  return (
    <>
      <BodyPage>
        <HistoryList />
      </BodyPage>
    </>
  );
}

export default history
