import '../../styles/creations.css';

function CreationsList (){
	return (
    <article className='Blocks_creations'>
      <div className="block_creations_left">
        <h2>Créations artistiques</h2>
        <p>Bienvenue dans la section dédié aux créations artistiques.
          <br/>Pour pouvoir poster vos créations artistiques, vous devez être inscrit et connecté.</p>
        <section>
          <p>
            Merci de respecter les règles suivantes :
          </p>
          <ol>
            <li>Pas de photo en dehors de l'univers de tolkien.</li>
            <li>Uniquement des créations artistiques (pas de photos tirées des films ou des livres).</li>
            <li>Aucun commentaires à caractère sexuel, raciste, homophobe, religieux ou politique ne sera toléré — tout manquement entraînera la suppression du compte.</li>
          </ol>
        </section>
      </div>
      <div className="block_creations_right">
        <p>HAHAHAHAHA</p>
      </div>
    </article>
  );
}

export default CreationsList
