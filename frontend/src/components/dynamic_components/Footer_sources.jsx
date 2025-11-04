/**
 * Composant d'affichage des sources et crédits du site
 * @module MentionsSource
 */

/**
 * Affiche la page des sources listant les images, polices, bibliothèques
 * et ressources utilisées pour la création du site
 *
 * @component
 * @returns {JSX.Element} Page des sources et crédits
 */
function MentionsSource() {
  return (
    <div className="mention">
      <h1 className="titre-mention">Sources</h1>
      <p>Voici les sources utilisées pour la création de ce portfolio :</p>

      <ul>
        <li>
          Images et illustrations : Microsoft Copilot, ou images libres de
          droits mentionnées individuellement.
        </li>
        <li>
          Polices : <a href="https://fonts.google.com/">Google Fonts</a> ou
          police personnalisée.
        </li>
        <li>
          Bibliothèques et frameworks : React, React Router, Leaflet, etc.
        </li>
        <li>
          Documentation et tutoriels : Sites officiels des technologies
          utilisées.
        </li>
		<li>Intelligence artificielle : Claude et ChatGPT.</li>
		<li>Aide d'autres étudiants d'holberton : Merci Mr VANDEVILLE.</li>
		<li> Générération de diagramme : Drawio et dbdiagram</li>
		<li>Visual Studio Code: Editeur de code.</li>
		<li>Réalisation des tests : Postman.</li>
		<li>Base de donnée : PostgreSQL.</li>
      </ul>

      <p>
        Lorsque les images ou contenus proviennent d’auteurs spécifiques, leur
        nom est mentionné à côté de l’œuvre.
      </p>
    </div>
  );
}

export default MentionsSource;
