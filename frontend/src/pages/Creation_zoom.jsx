/**
 * Page affichant le détail d’une création dans un corps de page.
 */

import BodyPage from '../components/static_components/Body_page';
import CreationDetail from '../components/dynamic_components/Creation_detail';

function CreationZoom() {
  return (
    <>
      <BodyPage>
        <CreationDetail />
      </BodyPage>
    </>
  );
}

export default CreationZoom
