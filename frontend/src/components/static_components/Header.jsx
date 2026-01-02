/**
 * Composant d'en-tête avec logo, titre et authentification
 * Affiche l'en-tête du site avec logo, titre et bouton de connexion/déconnexion
 * Gère l'état de connexion et la déconnexion de l'utilisateur
 * @module Header
 */

import React, { useEffect, useState } from 'react';
import logoArbre from '../../assets/logo_arbre.png';
import { Link, useNavigate} from 'react-router-dom';
import Tooltip from './Tooltip';

function Header({ menuOpen }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  // Vérifie au chargement si un token existe déjà
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  // Fonction de déconnexion
  const handleLogout = () => {
    localStorage.removeItem('token'); // Supprime le token du stockage local
    setIsLoggedIn(false);             // Met à jour l'état
    navigate('/');                    // Redirige vers la page d'accueil
  };

  return (
    <header className={`header header-${menuOpen}`}>
      <div className="left-side">
        <Tooltip text="Retour à la page d'accueil">
          <Link to="/" style={{ display: 'inline-block' }}>
            <img
              src={logoArbre}
              alt="Logo du site, représentant l'arbre blanc du Gondor"
              className="logo"
            />
          </Link>
        </Tooltip>
        <h1 className="titre-site">Voyage en Terre du Milieu</h1>
      </div>

      {/* Si connecté → bouton Déconnexion, sinon → lien vers /login */}
      {isLoggedIn ? (
      <button className="login-bouton" onClick={handleLogout}>
        Déconnexion
      </button>
      ) : (
      <Link to="/login">
        <button className="login-bouton">Connexion</button>
      </Link>
      )}
      {/*</div>*/}
    </header>
  );
}

export default Header;
