/**
 * @module HistoryList
 * Page affichant la liste des personnages dans un corps de page.
 */

import BodyPage from '../components/static_components/Body_page';
import CharacterList from '../components/dynamic_components/Character_list';

/**
 * Composant de page pour la section "Histoire".
 * @returns {JSX.Element} Conteneur affichant la liste des personnages.
 */
function HistoryList() {
	return (
		<>
			<BodyPage>
				<CharacterList />
			</BodyPage>
		</>
	);
}

export default HistoryList
