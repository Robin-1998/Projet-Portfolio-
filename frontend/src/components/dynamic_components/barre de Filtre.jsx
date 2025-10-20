// components/ImageFilter.jsx
import "../../styles/liste.css";

function Filtre ({ items, selectedIds, onChange }) {
	// items : tableau d'objets représentant les filtres [{ id, name, icon }]
	// selectedIds : tableau des IDs actuellement sélectionnés
	// onChange : fonction à appeler quand la sélection change (ex: mise à jour du state dans le parent)

// Fonction appelée lorsque l'on clique sur une icône de filtre
  function toggle(id) {
	// Si le filtre est déjà sélectionné, on le retire
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter(existingId => existingId !== id));
	// Sinon, on l'ajoute à la liste des filtres sélectionnés
    } else {
      onChange([...selectedIds, id]);
    }
  }

  return (
    <div className="filter-container">
	{/* Boucle sur chaque filtre pour afficher son icône */}
      {items.map(item => (
        <img
          key={item.id} // Clé unique pour chaque élément
          src={item.icon} // URL de l'icône à afficher
          alt={item.name} // Texte alternatif (accessibilité)
          title={item.name} // Titre au survol de l'image
          className={
            selectedIds.includes(item.id)
              ? "filter-icon selected"
              : "filter-icon"
          }
          onClick={() => toggle(item.id)} // Gère le clic pour sélectionner/désélectionner
        />
      ))}
    </div>
  );
}

export default Filtre;

/* import React, { useState, useEffect } from 'react';

const races = [
  { id: 1, name: 'Nain', imageUrl: '/images/nain.png' },
  { id: 2, name: 'Elfe', imageUrl: '/images/elfe.png' },
  { id: 3, name: 'Humain', imageUrl: '/images/humain.png' },
  // ajoute d'autres races ici si besoin
];

function Characters() {
  const [selectedRace, setSelectedRace] = useState(null);
  const [characters, setCharacters] = useState([]);

  useEffect(() => {
	const url = selectedRace 
	  ? `/characters?race_id=${selectedRace}` 
	  : '/characters';

	fetch(url)
	  .then(res => res.json())
	  .then(data => setCharacters(data))
	  .catch(err => console.error(err));
  }, [selectedRace]);

  return (
	<div>*/
	  {/* Carré filtre */}
	/*  <div 
		style={{
		  width: 300,
		  height: 300,
		  border: '2px solid #333',
		  borderRadius: 8,
		  padding: 10,
		  display: 'grid',
		  gridTemplateColumns: 'repeat(3, 1fr)',
		  gap: 10,
		  marginBottom: 20,
		  backgroundColor: '#f9f9f9',
		}}
	  >
		{races.map(race => (
		  <img
			key={race.id}
			src={race.imageUrl}
			alt={race.name}
			title={race.name}
			style={{
			  cursor: 'pointer',
			  border: selectedRace === race.id ? '3px solid blue' : '2px solid transparent',
			  borderRadius: 6,
			  width: '100%',
			  height: 'auto',
			  objectFit: 'contain',
			  transition: 'border-color 0.3s',
			}}
			onClick={() => setSelectedRace(race.id)}
		  />
		))}*/
		{/* Bouton pour remettre le filtre à "Tous" */}
		/*<button
		  style={{
			gridColumn: 'span 3',
			padding: '8px 12px',
			cursor: 'pointer',
			borderRadius: 6,
			border: '1px solid #333',
			backgroundColor: selectedRace === null ? '#ddd' : '#fff',
		  }}
		  onClick={() => setSelectedRace(null)}
		>
		  Tous
		</button>
	  </div>    */

	  {/* Liste des personnages */}
/*	  <div>
		{characters.length === 0 ? (
		  <p>Aucun personnage trouvé</p>
		) : (
		  <ul>
			{characters.map(character => (
			  <li key={character.id}>
				{character.name} - {character.race_name}
			  </li>
			))}
		  </ul>
		)}
	  </div>
	</div>
  );
}

export default Characters; */
