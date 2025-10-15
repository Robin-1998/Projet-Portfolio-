import { Link } from 'react-router-dom';
import Navigation from './navigation';

function BodyAllPage({ children }) {
  return (
    <div className="app-layout">
        <Navigation />

      <main className="contenu-principal">
        {children ? children : <p>Voici le contenu principal</p>}
      </main>
    </div>
  );
}

export default BodyAllPage;
