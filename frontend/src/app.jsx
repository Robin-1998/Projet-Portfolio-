/**
 * Composant racine de l'application
 * Utilise React Router pour la navigation entre les pages
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import routes from './routes/routes';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          {routes.map(({ path, element }) => (
            <Route key={path} path={path} element={element} />
          ))}
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
