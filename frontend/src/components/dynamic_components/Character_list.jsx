import { useEffect, useState } from 'react';
import axios from 'axios';
// Import de la bibliothèque axios pour faire les requêtes HTTP
import '../../styles/liste.css';

function CharactersListe() {
  const [characters, setCharacters] = useState([]);
  // Déclaration de l'état local "characters" . permetttra de stocker les personnages
  const [loading, setLoading] = useState(true);
  // loading permet d’afficher quelque chose à l’utilisateur pendant que la page est en train de charger les données

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/v1/characters')
      .then(res => {
        setCharacters(res.data);
        setLoading(false);
      })
	  // Cas d'erreur si jamais il y a un problème avec la récupération du personnage
      .catch(err => {
        console.error("Erreur lors de la récupération :", err);
        setLoading(false);
      });
  }, []);

  // Si c'est toujours en chargement alors on retourne le message pour en informer l'utilisateur
  if (loading) return <p>Chargement des personnages...</p>;

  return (
	<div className='container-vitrine'>
		<div className="head-filter">
			<h1>Personnages</h1>
		</div>
		<div className="character-grid">
			{characters.map(char => (
				<div key={char.id} className="card">
				<h2>{char.name}</h2>
				<p><strong>Profession:</strong> {char.profession}</p>
				<p><strong>Genre:</strong> {char.gender}</p>
				<p><strong>Ere :</strong> {char.era_birth}</p>
				</div>
			))}
		</div>
	</ div>
  );
}

export default CharactersListe;


/* import { useEffect, useState } from "react";
import Filtre from "./Filtre";

function CharacterList() {
  const [characters, setCharacters] = useState([]);
  const [selectedRaceIds, setSelectedRaceIds] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/v1/characters")
      .then(res => res.json())
      .then(data => setCharacters(data));
  }, []);

  // Extraire les races distinctes
  const races = [];
  const seen = new Set();
  characters.forEach(char => {
    if (!seen.has(char.race.id)) {
      seen.add(char.race.id);
      races.push(char.race); // {id, name, icon}
    }
  });

  const filteredCharacters = selectedRaceIds.length === 0
    ? characters
    : characters.filter(char => selectedRaceIds.includes(char.race.id));

  return (
    <div>
      <h2>Filtrer par race</h2>
      <Filtre
        items={races}
        selectedIds={selectedRaceIds}
        onChange={setSelectedRaceIds}
      />

      <h3>Personnages</h3>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        {filteredCharacters.map(char => (
          <div key={char.id}>
            <img src={char.avatar} alt={char.name} width="100" />
            <p>{char.name}</p>
            <p style={{ fontSize: "0.8em", color: "#666" }}>
              Race : {char.race.name}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CharacterList; */
