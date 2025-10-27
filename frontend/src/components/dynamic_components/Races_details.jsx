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
			<h2>{race.name}</h2>
			<p>"{race.citation}"</p>
			<p>{race.description}</p>
			<p className='para_justify'></p>
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
