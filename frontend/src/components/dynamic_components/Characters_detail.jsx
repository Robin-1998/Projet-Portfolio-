import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import '../../styles/creation_detail.css';
import getImagePath from '../../services/getImage'


function CharacterDetail() {
  const { id } = useParams();
  const [character, setCharacter] = useState(null);
  const [descriptions, setDescriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  // 🔹 Récupère les données du personnage
  useEffect(() => {
    const fetchCharacter = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/v1/characters/${id}`);
        setCharacter(res.data);
      } catch (err) {
        console.error("Erreur lors de la récupération du personnage :", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCharacter();
  }, [id]);

  // 🔹 Récupère les descriptions du personnage
  useEffect(() => {
    const fetchDescriptions = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/v1/descriptions/character/${id}`);
        setDescriptions(res.data.data || []);
      } catch (err) {
        console.error("Erreur lors de la récupération des descriptions :", err);
      }
    };

    if (id) fetchDescriptions();
  }, [id]);

  if (loading) return <p>Chargement...</p>;
  if (!character) return <p>Personnage non trouvé</p>;

  return (
    <div className="bloc-info">
      <div className='bloc_info_zoom_left'>
        <h2>{character.name}</h2>
        <p className='para_justify'>{character.description}</p>
				{/* Descriptions */}
		{descriptions.map(d => (
			<div key={d.id}>
			{d.title && <h3>{d.title}</h3>}
			<p>{d.content}</p>
			</div>
            ))}
      </div>

      <div className='bloc_info_zoom_right'>
        <img
          src={getImagePath(character.name, 'characters')}
          alt={character.name}
          className="image_info"
        />
        <p><b>Naissance :</b> {character.birth_date} {character.era_birth}</p>
        <p><b>Mort :</b> {character.death_date} {character.era_death}</p>
		<p><b>Genre :</b> {character.gender}</p>
		<p><b>Profession:</b> {character.profession}</p>
      </div>
    </div>
  );
}

export default CharacterDetail;
