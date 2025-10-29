import { useEffect, useState } from 'react';
import axios from 'axios';
import '../../styles/perso-race-liste.css';
import { Link } from 'react-router-dom';
import getImagePath from '../../services/getImage';

/**
 * Composant CharactersListe
 * Affiche une grille de tous les personnages avec image, nom et citation
 * Les données sont récupérées depuis l'API backend
 *
 * @component
 * @returns {JSX.Element} Liste de personnages
 */
function CharactersListe() {
  const [characters, setCharacters] = useState([]); // Liste des personnages
  const [descriptions, setDescriptions] = useState({}); // Potentiel stockage des descriptions (non utilisé ici)
  const [loading, setLoading] = useState(true); // Indique si les données sont en cours de chargement

  useEffect(() => {
    const fetchCharactersWithDescriptions = async () => {
      try {
        // Requête vers l'API pour récupérer tous les personnages
        const res = await axios.get('http://127.0.0.1:5000/api/v1/characters');
        const chars = res.data;
        setCharacters(chars); // Met à jour l'état characters
        setLoading(false);    // Fin du chargement
      } catch (err) {
        console.error("Erreur lors de la récupération des personnages :", err);
        setLoading(false); // Fin du chargement même en cas d'erreur
      }
    };

    fetchCharactersWithDescriptions();
  }, []); // [] : s'exécute une seule fois au montage du composant

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
            <div className='paragraphe_center'>
            <div className='paragraphe_hide'>
              <p>{char.citation}</p>
            </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CharactersListe;
