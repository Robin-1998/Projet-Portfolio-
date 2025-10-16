import logoArbre from '../../assets/logo_arbre.png';
import { Link } from 'react-router-dom';

function Header() {
    return (
        <header className="header">
            <div className="left-side">
                <Link to="/"> {/* lien vers la page d'accueil */}
                    <img
                        src={logoArbre}
                        alt="Logo du site, représentant l'arbre blanc du Gondor"
                        className="logo"
                    />
                </Link>
                <h1 className='titre-site'>Le Seigneur des Anneaux</h1>
            </div>

            <div className="right-side">
                <div className="search-bar">
                    <input type="text" placeholder="Rechercher un lieu, un personnage..." />
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
