/**
 * Composant conteneur pour le contenu principal des pages
 * @module Body_page
 */

/**
 * Wrapper pour le contenu principal avec layout responsive
 *
 * @component
 * @param {Object} props
 * @param {React.ReactNode} props.children - Contenu à afficher
 * @returns {JSX.Element} Conteneur du contenu principal
 */

import { useState } from 'react';
import Navigation from './Navigation';
import Header from './Header';
import Footer from './Footer';

function BodyPage({ children, mainClassName }) {
  const [menuOpen, setMenuOpen] = useState('icons');

  return (
    <div className={`layout ${menuOpen}`}>
      <Navigation menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
      <div className="content-area">
        <Header menuOpen={menuOpen} />
        <main className={`contenu-principal ${mainClassName || ''}`}>
          {children ? children : <p>Voici le contenu principal</p>}
        </main>
        <Footer />
      </div>
    </div>
  );
}

export default BodyPage;
