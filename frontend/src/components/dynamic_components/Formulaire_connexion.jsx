import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ornement from '../../assets/ornement.PNG';
import {useNavigate} from 'react-router-dom';
import '../../styles/login.css';


function FormulaireLogin() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // 🔹 Vérifie si un token est déjà présent au chargement
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  const navigate = useNavigate();

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
