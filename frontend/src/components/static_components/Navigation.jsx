import { Link, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import carteImage from '../../assets/logo_carte.png';
import characterImage from '../../assets/logo_personnage.png';
import histoireImage from '../../assets/logo_livre.png';
import artImage from '../../assets/logo_creation.png';
import racesImage from '../../assets/logo_races.png';

function Navigation({ menuOpen, setMenuOpen }) {
  const location = useLocation();

  // Fermer le menu automatiquement sur mobile après navigation
  useEffect(() => {
    if (window.innerWidth <= 768 && menuOpen === 'full') {
      setMenuOpen('icons');
    }
  }, [location, menuOpen, setMenuOpen]);

  // Fermer le menu si on clique en dehors (sur mobile)
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (window.innerWidth <= 768 && menuOpen === 'full') {
        const nav = document.querySelector('.menu-gauche');
        if (nav && !nav.contains(e.target)) {
          setMenuOpen('icons');
        }
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [menuOpen, setMenuOpen]);

  // Toggle entre 2 modes : icons <-> full
  const toggleMenu = (e) => {
    e.stopPropagation();
    setMenuOpen(menuOpen === 'icons' ? 'full' : 'icons');
  };

  return (
    <nav
      className={`menu-gauche ${menuOpen === 'icons' ? 'icons-only' : 'open'}`}
    >
      {/* Bouton hamburger */}
      <div
        className="hamburger-menu"
        onClick={toggleMenu}
        aria-label={menuOpen === 'icons' ? 'Afficher les descriptions' : 'Masquer les descriptions'}
        aria-expanded={menuOpen === 'full'}
      >
        <span></span>
        <span></span>
        <span></span>
      </div>

      {/* Icônes + texte */}
      <ul className="icone_barre">
        <li>
          <Link
            to="/home_map"
            className="nav-item"
            aria-label="Carte interactive"
          >
            <img
              src={carteImage}
              alt="carte interactive"
              className="image_nav"
            />
            {menuOpen === 'full' && <span className="nav-text">Carte</span>}
          </Link>
        </li>
        <li>
          <Link
            to="/characters"
            className="nav-item"
            aria-label="Personnages"
          >
            <img
              src={characterImage}
              alt="personnages"
              className="image_nav"
            />
            {menuOpen === 'full' && <span className="nav-text">Personnages</span>}
          </Link>
        </li>
        <li>
          <Link
            to="/races"
            className="nav-item"
            aria-label="Races"
          >
            <img
              src={racesImage}
              alt="races"
              className="image_nav"
            />
            {menuOpen === 'full' && <span className="nav-text">Races</span>}
          </Link>
        </li>
        <li>
          <Link
            to="/histoires"
            className="nav-item"
            aria-label="Histoires"
          >
            <img
              src={histoireImage}
              alt="histoires"
              className="image_nav"
            />
            {menuOpen === 'full' && <span className="nav-text">Histoires</span>}
          </Link>
        </li>
        <li>
          <Link
            to="/creations"
            className="nav-item"
            aria-label="Galerie d'Art"
          >
            <img
              src={artImage}
              alt="création artistique"
              className="image_nav"
            />
            {menuOpen === 'full' && <span className="nav-text">Galerie d'Art</span>}
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navigation;
