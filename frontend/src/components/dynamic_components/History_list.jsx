import { useEffect, useState } from 'react';
import axios from 'axios';
// Import de la bibliothèque axios pour faire les requêtes HTTP
import '../../styles/liste.css';

function HistoryList() {
  const [History, setHistory] = useState([]);
  // Déclaration de l'état local "characters" . permetttra de stocker les histoires
  const [loading, setLoading] = useState(true);
  // loading permet d’afficher quelque chose à l’utilisateur pendant que la page est en train de charger les données

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/v1/histories')
      .then(res => {
        setHistory(res.data);
        setLoading(false);
      })
	  // Cas d'erreur si jamais il y a un problème avec la récupération des évènements
      .catch(err => {
        console.error("Erreur lors de la récupération :", err);
        setLoading(false);
      });
  }, []);

  // Si c'est toujours en chargement alors on retourne le message pour en informer l'utilisateur
  if (loading) return <p>Chargement des évènements de l'histoire...</p>;

  return (
	<div className='container-vitrine'>
		<div className="head-filter">
			<h1>Histoires</h1>
		</div>
		<div className="character-grid">
			{History.map(char => (
				<div key={char.id} className="card">
				<h2>{char.name}</h2>
				</div>
			))}
		</div>
	</ div>
  );
}

export default HistoryList;
