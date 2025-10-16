import { Link } from 'react-router-dom';
import BodyPage from '../components/static_components/Body_page';
import FormulaireLogin from '../components/dynamic_components/Formulaire_connexion';

function Login() {
	return (
		<>
			<BodyPage>
				<FormulaireLogin />
			</BodyPage>
		</>
	);
}

export default Login
