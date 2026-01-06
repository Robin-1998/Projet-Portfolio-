/**
 * Page d’authentification affichant le formulaire de connexion/inscription.
 */

import BodyPage from '../components/static_components/Body_page';
import LoginRegister from '../components/dynamic_components/Login_register';

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
