import { useEffect, useState } from 'react';
import axios from 'axios';
import '../../styles/liste.css';
import { Link } from 'react-router-dom';
import getImagePath from '../../services/getImage';

function CharactersListe() {
  const [characters, setCharacters] = useState([]);
  const [descriptions, setDescriptions] = useState({});
  const [loading, setLoading] = useState(true);

  // Récupération des descriptions d'un personnage
  const fetchDescriptions = async (characterId) => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/api/v1/descriptions/character/${characterId}`);
      return res.data.data || []; // un data en plus car rajout d'un tableau en plus à cause de région
    } catch (err) {
      console.error(`Erreur lors de la récupération des descriptions pour character ${characterId}:`, err);
      return [];
    }
  };

  useEffect(() => {
    const fetchCharactersWithDescriptions = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/v1/characters');
        const chars = res.data;
        setCharacters(chars);

        // Récupération des descriptions pour chaque personnage
        const descs = {};
        for (let char of chars) {
          descs[char.id] = await fetchDescriptions(char.id);
        }
        setDescriptions(descs);

        setLoading(false);
      } catch (err) {
        console.error("Erreur lors de la récupération des personnages :", err);
        setLoading(false);
      }
    };

    fetchCharactersWithDescriptions();
  }, []);

  if (loading) return <p>Chargement des personnages...</p>;

  return (
    <div className='container-histoire'>
      <div className="head-filter">
        <h1 className='titre-histoire'>Personnages</h1>
      </div>
      <div className="character-grid">
        {characters.map(char => (
          <div key={char.id} className="card">
          <Link to={`/characters/${char.id}`}>
            <img src={getImagePath(char.name, 'characters')} alt={char.name} className="image_card" />
          </ Link>
            <h2>{char.name}</h2>
            <p>{char.citation}</p>

            {/* Descriptions - maintenant simplifié ✅ */}
            {descriptions[char.id]?.map(d => (
              <div key={d.id}>
                {d.title && <h3>{d.title}</h3>}
                <p>{d.content}</p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default CharactersListe;
