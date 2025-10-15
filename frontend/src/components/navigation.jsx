import { Link } from 'react-router-dom';
import carteImage from '../assets/logo_carte.png';
import characterImage from '../assets/logo_personnage.png';
import histoireImage from '../assets/logo_livre.png';
import artImage from '../assets/logo_creation.png';
import racesImage from '../assets/logo_races.png';

function Navigation() {
  return (
	<ul className='icone_barre'>
		<li><Link to="/onglet-carte-interactive"><img src={carteImage} alt='logo carte interactive' className='image_nav'></img></Link></li>
		<li><Link to="/onglet-Personnages"><img src={characterImage} alt='logo personnages' className='image_nav'></img></Link></li>
		<li><Link to="/onglet-Personnages"><img src={racesImage} alt='logo races' className='image_nav'></img></Link></li>
		<li><Link to="/onglet-Personnages"><img src={histoireImage} alt='logo histoires' className='image_nav'></img></Link></li>
		<li><Link to="/onglet-Personnages"><img src={artImage} alt='logo création artistique' className='image_nav'></img></Link></li>
	</ul>
  );
};

export default Navigation;
