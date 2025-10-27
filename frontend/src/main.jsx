import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app.jsx';
import './styles/static.css';
import './styles/login.css';
import './styles/map.css';
import './styles/Tooltip.css';
import './styles/detail_place.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

/*
React.StrictMode : active des alertes pour t’aider à écrire un meilleur code React (en mode dev seulement).
BrowserRouter : gère la navigation sans rechargement, indispensable pour React Router.
*/
