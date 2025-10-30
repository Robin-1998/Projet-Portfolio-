/**
 * Composant d'affichage de la liste des races
 * @module RacesList
 */

import { useEffect, useState } from 'react';
import axios from 'axios';
import getImagePath from '../../services/getImage'
import { Link } from 'react-router-dom';
// Import de la bibliothèque axios pour faire les requêtes HTTP
import '../../styles/perso-race-liste.css';

/**
 * Affiche une grille de cartes des différentes races de l'univers du Seigneur des Anneaux
 * Récupère les données depuis l'API et gère le chargement asynchrone
 *
 * @component
 * @returns {JSX.Element} Grille des races
 */
function RacesList() {
  const [Races, setRaces] = useState([]);
  // Déclaration de l'état local "characters" . permetttra de stocker les histoires
  const [loading, setLoading] = useState(true);
  // loading permet d’afficher quelque chose à l’utilisateur pendant que la page est en train de charger les données

  /**
   * Effet pour charger la liste des races au montage du composant
   * Récupère les données depuis l'API et met à jour l'état
   */
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/v1/races')
      .then(res => {
        setRaces(res.data);
        setLoading(false);
      })
	  // Cas d'erreur si jamais il y a un problème avec la récupération des évènements
      .catch(err => {
        console.error("Erreur lors de la récupération :", err);
        setLoading(false);
      });
  }, []);

  // Si c'est toujours en chargement alors on retourne le message pour en informer l'utilisateur
  if (loading) return <p>Chargement des différentes Races...</p>;

  return (
    <div className='container-histoire'>
      <h1 className='titre-histoire'>Les Espèces</h1>
      <div className="character-grid">
        {Races.map(char => (
          <div key={char.id} className="card">
            <Link to={`/races/${char.id}`}>
              <img src={getImagePath(char.name, 'races')} alt={char.name} className="image_card" />
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
    </ div>
  );
}

export default RacesList;
