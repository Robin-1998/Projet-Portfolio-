import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './app.jsx'
import { BrowserRouter } from 'react-router-dom';
import './styles/layout.css'
import './styles/index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
        <App />
    </BrowserRouter>
  </React.StrictMode>
)

/* ajout favicon */
const link = document.createElement('link');
link.rel = 'icon';
link.href = favicon;
document.head.appendChild(link);

/*
React.StrictMode : active des alertes pour t’aider à écrire un meilleur code React (en mode dev seulement).
BrowserRouter : gère la navigation sans rechargement, indispensable pour React Router.
*/
