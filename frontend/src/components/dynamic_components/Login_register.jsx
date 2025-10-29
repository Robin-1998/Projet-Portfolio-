/**
 * Composant de page d'authentification regroupant connexion et inscription
 * @module LoginRegister
 */

import React from 'react';
import FormulaireLogin from './Formulaire_connexion';
import FormulaireRegister from './Formulaire_register';
import '../../styles/login.css';

/**
 * Affiche côte à côte le formulaire de connexion et le formulaire d'inscription
 *
 * @component
 * @returns {JSX.Element} Page d'authentification complète
 */
function LoginRegister() {
  return (
    <div className="login-container">
      <FormulaireLogin />
      <FormulaireRegister />
    </div>
  );
}

export default LoginRegister;
