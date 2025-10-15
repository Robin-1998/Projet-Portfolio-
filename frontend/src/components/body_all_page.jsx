import { Link } from 'react-router-dom';
import Navigation from './navigation';

function BodyAllPage() {
  return (
    <div className="app-layout">
      <nav className="menu-gauche">
		  <div className="hamburger-menu">
			<span></span>
			<span></span>
			<span></span>
		  </div>
        <Navigation />
      </nav>

      <main className="contenu-principal">
        <p>Voici le contenu principal</p>
      </main>
    </div>
  );
}

export default BodyAllPage;
