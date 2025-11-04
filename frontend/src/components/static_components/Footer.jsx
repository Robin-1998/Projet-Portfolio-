/**
 * Composant de pied de page avec liens et informations
 * @module Footer
 */

/**
 * Affiche le pied de page avec liens vers mentions légales et sources
 *
 * @component
 * @returns {JSX.Element} Pied de page du site
 */

import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer>
      <nav>
        <ul>
          <li>
            <Link to="/mentions">Mentions légales</Link>
          </li>
          <li>
            <Link to="/sources">Sources</Link>
          </li>
        </ul>
      </nav>
    </footer>
  );
}

export default Footer;
