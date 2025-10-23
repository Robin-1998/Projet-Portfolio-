import { Link } from 'react-router-dom';
import carteImage from '../../assets/logo_carte.png';
import characterImage from '../../assets/logo_personnage.png';
import histoireImage from '../../assets/logo_livre.png';
import artImage from '../../assets/logo_creation.png';
import racesImage from '../../assets/logo_races.png';

function Navigation({ menuOpen, setMenuOpen }) {
  return (
    <nav className={`menu-gauche ${menuOpen ? 'open' : ''}`}>
      {/* Bouton hamburger */}
      <div className="hamburger-menu" onClick={() => setMenuOpen(!menuOpen)}>
        <span></span>
        <span></span>
        <span></span>
      </div>

      {/* Icônes + texte */}
      <ul className={`icone_barre ${menuOpen ? 'visible' : ''}`}>
        <li>
          <Link to="/home_map" className="nav-item">
            <img
              src={carteImage}
              alt="carte interactive"
              className="image_nav"
            />
            {menuOpen && <span className="nav-text">Carte</span>}
          </Link>
        </li>
        <li>
          <Link to="/characters" className="nav-item">
            <img src={characterImage} alt="personnages" className="image_nav" />
            {menuOpen && <span className="nav-text">Personnages</span>}
          </Link>
        </li>
        <li>
          <Link to="/races" className="nav-item">
            <img src={racesImage} alt="races" className="image_nav" />
            {menuOpen && <span className="nav-text">Races</span>}
          </Link>
        </li>
        <li>
          <Link to="/histoires" className="nav-item">
            <img src={histoireImage} alt="histoires" className="image_nav" />
            {menuOpen && <span className="nav-text">Histoires</span>}
          </Link>
        </li>
        <li>
          <Link to="/creations" className="nav-item">
            <img
              src={artImage}
              alt="création artistique"
              className="image_nav"
            />
            {menuOpen && <span className="nav-text">Gallerie d'Art</span>}
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navigation;
