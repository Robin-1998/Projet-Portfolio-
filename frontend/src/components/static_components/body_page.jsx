import { Link } from 'react-router-dom';
import Navigation from './navigation';
import Header from './header';
import Footer from './footer';

function BodyPage({ children }) {
  return (
    <>
      <Header />
      <Navigation />
      <main className="contenu-principal">
        {children ? children : <p>Voici le contenu principal</p>}
      </main>
      <Footer />
    </>
  );
}

export default BodyPage;
