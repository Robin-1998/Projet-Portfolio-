/**
 * Point d'entrée de l'application React
 * @module Main
 */

/**
 * Initialise et monte l'application React dans le DOM
 * Configure le StrictMode pour détecter les problèmes potentiels
 *
 * @returns {void}
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app.jsx';
import './styles/static.css';
import './styles/map.css';
import './styles/Tooltip.css';


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
