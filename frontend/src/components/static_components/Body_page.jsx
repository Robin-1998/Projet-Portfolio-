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
        <Header menuOpen={menuOpen} /> {/* Ajoutez la prop ici */}
        <main className={`contenu-principal ${mainClassName || ''}`}>
          {children ? children : <p>Voici le contenu principal</p>}
        </main>
        <Footer />
      </div>
    </div>
  );
}

export default BodyPage;
