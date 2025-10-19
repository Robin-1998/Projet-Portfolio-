import React from 'react';
import ornement from '../../assets/ornement.PNG';

function FormulaireLogin() {
  return (
    <div className="login-container">
      {/* FORMULAIRE LOGIN */}
      <form className="form-box1">
        <h2 className='login-h2'>Connexion</h2>
        <div className='bouton-text1'>
          <input type="email" placeholder="Email" className="input-field" />
          <input type="password" placeholder="Mot de passe" className="input-field" />
        </div>
        <img className='ornement' src={ornement} alt="Ornement" />
        <button type="submit" className="btn">Se connecter</button>
      </form>

      {/* FORMULAIRE REGISTER */}
      <form className="form-box2">
        <h2 className='login-h2'>Créer un Hobbit</h2>
        <div className='bouton-text2'>
          <input type="text" placeholder="Nom" className="input-field" />
          <input type="text" placeholder="Prénom" className="input-field" />
          <input type="email" placeholder="Email" className="input-field" />
          <input type="password" placeholder="Mot de passe" className="input-field" />
        </div>
        <button type="submit" className="btn">Créer le compte</button>
      </form>
    </div>
  );
}

export default FormulaireLogin
