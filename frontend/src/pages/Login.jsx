/**
 * @module Login
 * Page d’authentification affichant le formulaire de connexion/inscription.
 */

import { Link } from 'react-router-dom';
import BodyPage from '../components/static_components/Body_page';
import LoginRegister from '../components/dynamic_components/Login_register';
import React, { useState } from 'react';

/**
 * Composant de la page de connexion.
 * @returns {JSX.Element} Conteneur affichant le formulaire de login/inscription.
 */
function Login() {
  return (
    <>
      <BodyPage>
        <LoginRegister />
      </BodyPage>
    </>
  );
}

export default Login;
