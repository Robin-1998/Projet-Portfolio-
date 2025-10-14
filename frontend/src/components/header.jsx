import '../styles/layout.css'; // extension .css obligatoire
import logoArbre from '../assets/logo_arbre.png';

function Header() {
    return (
        <header className="header">
            <div className="left-side">
                <img
                    src={logoArbre}
                    alt="Logo du site, représentant l'arbre blanc du Gondor"
                    className="logo"
                />
                <h1>Le Seigneur des Anneaux</h1>
            </div>

            <div className="right-side">
                <div className="search-bar">
                    <input type="text" placeholder="Rechercher un lieu, un personnage..." />
                    <button>🔍</button>
                </div>
                <button className="login-bouton">Connexion</button>
            </div>
        </header>
    );
}


export default Header;
