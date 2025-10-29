/**
 * Composant de formulaire de connexion utilisateur
 * @module FormulaireLogin
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ornement from '../../assets/ornement.PNG';
import {useNavigate} from 'react-router-dom';
import '../../styles/login.css';

/**
 * Affiche un formulaire de connexion avec gestion de l'authentification JWT
 * Vérifie l'état de connexion au chargement et redirige après succès
 *
 * @component
 * @returns {JSX.Element} Formulaire de connexion
 */
function FormulaireLogin() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  /**
   * Vérifie si un token JWT est déjà présent dans le localStorage au montage
   * Si présent, marque l'utilisateur comme déjà connecté
   */
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  /**
   * Gère la soumission du formulaire de connexion
   * Envoie les identifiants à l'API et stocke le token JWT en cas de succès
   *
   * @async
   * @param {Event} e - Événement de soumission du formulaire
   */
  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/api/v1/auth/login', {
        email,
        password,
      });

      const { access_token } = response.data;

      localStorage.setItem('token', access_token);
      setIsLoggedIn(true);
      setMessage('Connexion réussie !');
      navigate('/');

    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        setMessage(error.response.data.error);
      } else {
        setMessage('Erreur lors de la connexion');
      }
    }
  };

  return (
    <div className="login-container">
      <form className="form-box1" onSubmit={handleLoginSubmit}>
        <h2 className="login-h2">Connexion</h2>

        <div className="bouton-text1">
          <input
            type="email"
            placeholder="Email"
            className="input-field"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Mot de passe"
            className="input-field"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <img className="ornement" src={ornement} alt="Ornement" />

        {/* 🔹 Affiche le bouton seulement si non connecté */}
        {!isLoggedIn && (
          <button type="submit" className="btn">
            Se connecter
          </button>
        )}

        {message && <p>{message}</p>}
      </form>
    </div>
  );
}

export default FormulaireLogin;
