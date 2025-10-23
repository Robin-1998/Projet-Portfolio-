import React from 'react';
import FormulaireLogin from './Formulaire_connexion';
import FormulaireRegister from './Formulaire_register';

function LoginRegister() {
  return (
    <div className="login-container">
      <FormulaireLogin />
      <FormulaireRegister />
    </div>
  );
}

export default LoginRegister;
