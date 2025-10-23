import React, { useState } from 'react';
import axios from 'axios';
import ornement from '../../assets/ornement.PNG';

function FormulaireLogin() {
  // On stocke les valeurs des inputs dans l'état local
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  // Pour afficher un message d'erreur ou succès
  const [message, setMessage] = useState('');

  // Fonction appelée à la soumission du formulaire
  const handleLoginSubmit = async (e) => {
    e.preventDefault(); // Empêche le rechargement de la page

    try {
      // On appelle le backend en POST avec email et password
      const response = await axios.post('http://localhost:5000/api/v1/auth/login', {
        email,
        password,
      });

      const { access_token } = response.data;

      // Tu peux stocker le token pour les futures requêtes
      localStorage.setItem('token', access_token);
      setMessage('Connexion réussie !');

    } catch (error) {
      // En cas d'erreur on affiche un message adapté
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
        <button type="submit" className="btn">
          Se connecter
        </button>
        {/* Affichage du message d'erreur ou succès */}
        {message && <p>{message}</p>}
      </form>
    </div>
  );
}

export default FormulaireLogin;
