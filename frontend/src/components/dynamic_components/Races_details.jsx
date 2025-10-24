import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import getImagePath from '../../services/getImage';
import '../../styles/page_information.css';

function RaceDetail() {
  const { id } = useParams();
  const [race, setRace] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://127.0.0.1:5000/api/v1/races/${id}`)
      .then(res => {
        setRace(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Erreur lors de la récupération :", err);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <p>Chargement...</p>;
  if (!race) return <p>Race non trouvée</p>;

  return (
    <div className="bloc-info">
		<div className='bloc_info_zoom_left'>
			<h1>{race.name}</h1>
			<p>"{race.description}"</p>
			<h3>Dénominations</h3>
			<p className='para_justify'>
			Dans les écrits de Tolkien, Homme avec une majuscule se réfère à n'importe quel être humain (atan en quenya) 
			alors qu'homme avec une minuscule fait référence à un mâle adulte de n'importe quelle race (nér). Legolas, 
			par exemple, peut être appelé un homme mais non pas un Homme.
			Les Elfes appellent la race des Hommes Atani en langue quenyarine, signifiant littéralement le Deuxième Peuple
			(les Elfes étant les Premiers), mais aussi Hildor (les Suivants), Apanónar (les Cadets) et Fírimar ou Firyar 
			(les Mortels). Moins charitablement ils ont été appelés Engwar (les Maladifs ), à cause de leur sensibilité 
			à la maladie et à la vieillesse, et de leur apparence généralement disgracieuse aux yeux des Elfes. Le nom Atani 
			devient Edain en langue sindarin, mais ce terme est plus tard appliqué uniquement aux Hommes amicaux avec les 
			Elfes. D'autres noms apparaissent en sindarin, comme Aphadrim, Eboennin et Firebrim ou Firiath. Étant la seconde 
			race née sur la Terre du Milieu, les Hommes sont généralement plus faibles que des Elfes et ont une coordination 
			et des réflexes moins bons
			</p>
		</div>
		<div className='bloc_info_zoom_right'>
			<img src={getImagePath(race.name, 'races')} alt={race.name} className="image_info"/>
			<p><b>Point forts :</b> {race.strength}</p>			
			<p><b>Faiblesses :</b> {race.weakness}</p>
		</div>
    </div>
  );
}

export default RaceDetail;
