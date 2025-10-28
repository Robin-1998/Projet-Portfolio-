import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import getImagePath from '../../services/getImage';
import '../../styles/detail_RPH.css';

function HistoryZoom() {
  const { id } = useParams();
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/v1/histories/${id}`);
        setHistory(res.data);
      } catch (err) {
        console.error("Erreur lors de la récupération :", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) return <p>Chargement de l’histoire...</p>;
  if (!history) return <p>Histoire introuvable.</p>;

  return (
    <div className="bloc-info">
      <div className="bloc_info_zoom_left">
        <h1>{history.name}</h1>

        {history.citation && (
          <p className="citation">
            <i>"{history.citation}"</i>
          </p>
        )}

        {history.description && (
          <p className="para_justify" style={{ whiteSpace: 'pre-line' }}>
            {history.description}
          </p>
        )}
      </div>

      <div className="bloc_info_zoom_right">
        <img
          src={getImagePath(history.name, 'history')}
          alt={history.name}
          className="image_info"
          onError={(e) => console.warn("❌ Image introuvable :", e.target.src)}
        />
        {history.date && <p><b>Date :</b> {history.date}</p>}
        {history.location && <p><b>Lieu :</b> {history.location}</p>}
      </div>
    </div>
  );
}

export default HistoryZoom;
