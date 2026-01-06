/**
 * Page affichant le résumé d'un personnage dans un corps de page.
 */

import BodyPage from '../components/static_components/Body_page';
import CharactersDetail from '../components/dynamic_components/Characters_detail';

function CharacterZoom() {
	return (
		<>
			<BodyPage>
				<CharactersDetail />
			</BodyPage>
		</>
	);
}

export default CharacterZoom
