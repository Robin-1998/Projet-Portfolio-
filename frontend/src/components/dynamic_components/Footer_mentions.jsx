/**
 * Composant d'affichage des mentions légales du site
 * @module MentionsLegales
 */

/**
 * Affiche la page des mentions légales incluant les informations sur l'éditeur,
 * l'hébergeur, la propriété intellectuelle, les règles de publication et le RGPD
 *
 * @component
 * @returns {JSX.Element} Page des mentions légales
 */
function MentionsLegales() {
  return (
    <div className="mention">
      <h1 className="titre-mention">Mentions légales</h1>

	  <p>
		Ce site est un projet personnel à but non lucratif.
		Il a pour objectif de regrouper et partager des informations sur l’univers du Seigneur des Anneaux à des fins de documentation et de passion.
	  </p>

      <h2 className="titre2-mention">Éditeur du site</h2>
      <p>
        Thérèse-Marie Lefoulon et Robin David
        <br />
      </p>

      <h2>Propriété intellectuelle</h2>
      <p>
        Tous les contenus originaux du site (textes, images, design) sont la
        propriété de Thérèse-Marie Lefoulon et Robin David. Toute reproduction
        totale ou partielle est interdite sans autorisation.
      </p>

      <p>
        Les contenus publiés par les utilisateurs (images, commentaires) restent
        leur propriété. En publiant sur ce site, l’utilisateur accorde au site
        une licence non exclusive et gratuite pour afficher, partager et
        héberger ces contenus dans le cadre du site.
      </p>

	<h2>Génération d'image à l'aide de l'intelligence artificielle</h2>
	  <p>
		Les images utilisées sont générées par intelligence artificielle à l’aide de Microsoft Copilot.
		<ul>
			<li>Les prompts sont conçus pour s’inspirer de l’univers de Tolkien, sans reproduire directement les œuvres sous copyright.</li>
			<li>Seul l'image de la carte interactive n'est pas une génération de Copilot</li>
		</ul>
		L’univers du Seigneur des Anneaux et ses personnages sont la propriété de la Tolkien Estate,
		Middle-earth Enterprises, HarperCollins et Warner Bros. Ce site ne revendique aucun droit sur ces œuvres.
	  </p>

      <h2>Règles de publication des contenus</h2>
      <p>
        Les utilisateurs peuvent poster des commentaires et des images sur le
        site. Les contenus publiés doivent respecter les règles suivantes :
      </p>
      <ul>
        <li>Pas de contenus à caractère pornographique ou sexuel explicite.</li>
        <li>Pas de contenus violents, racistes, diffamatoires ou illégaux.</li>
        <li>Pas de publicité non autorisée.</li>
        <li>
          Les contenus doivent respecter les droits d’auteur et la propriété
          intellectuelle.
        </li>
      </ul>

      <p>
        Tout contenu enfreignant ces règles pourra être supprimé par
        l’administrateur du site. En publiant un contenu, l’utilisateur certifie
        qu’il en est l’auteur ou qu’il dispose des droits nécessaires pour le
        partager.
      </p>

      <h2>Données personnelles</h2>
      <p>
        Les informations fournies lors de la création d’un compte (nom, email,
        mot de passe) sont utilisées uniquement pour permettre l’accès au site
        et poster des commentaires ou des images. Ces données ne sont pas
        partagées avec des tiers.
      </p>
      <p>
        Conformément au RGPD, vous disposez d’un droit d’accès, de modification
        et de suppression de vos données personnelles. Vous pouvez exercer ces
        droits en vous connectant à votre compte ou en contactant
        l’administrateur du site.
      </p>

      <h2>Cookies</h2>
      <p>
        Ce site n’utilise pas de cookies à des fins publicitaires. Si des
        cookies techniques sont utilisés, vous pouvez les refuser via les
        paramètres de votre navigateur.
      </p>
    </div>
  );
}

export default MentionsLegales;
