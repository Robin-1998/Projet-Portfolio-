/**
 * Composant de formulaire d'inscription utilisateur
 * @module FormulaireRegister
 */
import React, { useState } from 'react';
import axios from 'axios';
import '../../styles/login.css';

/**
 * Affiche un formulaire d'inscription permettant de créer un nouveau compte utilisateur
 * Collecte les informations (nom, prénom, email, mot de passe) et les envoie à l'API
 *
 * @component
 * @returns {JSX.Element} Formulaire d'inscription
 */
function FormulaireRegister() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  /**
   * Gère la soumission du formulaire d'inscription
   * Crée un nouveau compte utilisateur via l'API et réinitialise le formulaire en cas de succès
   *
   * @async
   * @param {Event} e - Événement de soumission du formulaire
   */
  const handleRegisterSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/api/v1/users/', {
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password,
      });

      setMessage('Hobbit créé avec succès ! Vous pouvez maintenant vous connecter.');
      // Tu peux aussi vider le formulaire si tu veux
      setFirstName('');
      setLastName('');
      setEmail('');
      setPassword('');
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        setMessage(error.response.data.error);
      } else {
        setMessage('Erreur lors de la création du compte');
      }
    }
  };

  return (
    <form className="form-box2" onSubmit={handleRegisterSubmit}>
      <h2 className="login-h2">Créer un Hobbit</h2>
      <div className="bouton-text2">
        <input
          type="text"
          placeholder="Nom"
          className="input-field"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Prénom"
          className="input-field"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          required
        />
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

      {/* Affichage du message d'erreur/succès */}
      {message && (
        <p className="login-message">{message}</p>
      )}

      <button type="submit" className="btn">
        Créer le compte
      </button>
    </form>
  );
}

export default FormulaireRegister;
