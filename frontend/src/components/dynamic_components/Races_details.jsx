/**
 * Composant d'affichage détaillé d'une race de l'univers du Seigneur des Anneaux
 * @module RaceDetail
 */

import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import getImagePath from '../../services/getImage';
import '../../styles/detail_RPH.css';

/**
 * Affiche les détails complets d'une race (Elfes, Hobbits, Nains, etc.)
 * Récupère les informations depuis l'API et affiche nom, description, forces et faiblesses
 *
 * @component
 * @returns {JSX.Element} Page de détail de la race
 */
function RaceDetail() {
  const { id } = useParams();
  const [race, setRace] = useState(null);
  const [loading, setLoading] = useState(true);

  /**
   * Effet pour récupérer les détails de la race au montage du composant
   * Utilise l'ID récupéré depuis les paramètres d'URL
   */
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

  if (loading) return <p className="loading-message">Chargement...</p>;
  if (!race) return <p className="error-message">Race non trouvée</p>;

  return (
    <div className="bloc-info">
      <div className='bloc_info_zoom_left'>
        <h2>{race.name}</h2>
        <p>{race.description}</p>
        <p className='para_justify'></p>
      </div>
      <div className='bloc_info_zoom_right'>
        <img src={getImagePath(race.name, 'races')} alt={race.name} className="image_info"/>
        <p><b>Points forts :</b> {race.strength}</p>
        <p><b>Faiblesses :</b> {race.weakness}</p>
      </div>
    </div>
  );
}

export default RaceDetail;
