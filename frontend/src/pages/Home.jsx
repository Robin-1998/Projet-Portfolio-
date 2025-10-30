/**
 * @module Home
 * Page d’accueil affichant le contenu principal.
 */

import BodyPage from '../components/static_components/Body_page';

/**
 * Composant de la page d’accueil.
 * @returns {JSX.Element} Conteneur affichant le contenu principal de la page d’accueil.
 */
function Home() {
  return (
    <BodyPage>
      <div className="block-principal">
        <h2>Bienvenue</h2>
        <p>Voici le contenu principal de la page d'accueil</p>
      </div>
    </BodyPage>
  );
}

export default Home;
