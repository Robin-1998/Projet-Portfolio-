import logoArbre from '../../assets/logo_arbre.png';
import { Link } from 'react-router-dom';
import Tooltip from './Tooltip';

function Header() {
  return (
    <header className="header">
      <div className="left-side">
        <Tooltip text="Retour à la page d'accueil">
          <Link to="/" style={{ display: 'inline-block' }}>
            <img
              src={logoArbre}
              alt="Logo du site, représentant l'arbre blanc du Gondor"
              className="logo"
            />
          </Link>
        </Tooltip>
        <h1 className="titre-site">Le Seigneur des Anneaux</h1>
      </div>

      <div className="right-side">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Rechercher un lieu, un personnage..."
          />
          <button>🔍</button>
        </div>
        <Link to="/login">
          <button className="login-bouton">Connexion</button>
        </Link>
      </div>
    </header>
  );
}

export default Header;
