import { Link } from 'react-router-dom';


function Footer() {
  return (
    <footer>
		<nav>
			<ul>
				<li><Link to="/mentions-legales">Mentions légales</Link></li>
				<li><Link to="/sources">Sources</Link></li>
			</ul>
		</nav>
    </footer>
  );
};

export default Footer;
