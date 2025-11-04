/**
 * Composant de détail d'une création artistique avec système de commentaires
 * @module CreationDetail
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import '../../styles/creation_detail.css';

/**
 * Affiche le détail d'une création artistique avec son image, informations et commentaires
 * Permet aux utilisateurs authentifiés de laisser des commentaires
 *
 * @component
 * @returns {JSX.Element} Page de détail de la création
 */
function CreationDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [creation, setCreation] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [submitting, setSubmitting] = useState(false);

  /**
   * Effet pour charger la création et ses commentaires au montage
   * Vérifie également l'état d'authentification de l'utilisateur
   */
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);

    const fetchData = async () => {
      try {
        // Récupérer la création (accessible à tous)
        const creationRes = await axios.get(`http://127.0.0.1:5000/api/v1/images/${id}`);
        setCreation(creationRes.data);

        // Récupérer les reviews (PUBLIC après modification backend)
        try {
          const reviewsRes = await axios.get(`http://127.0.0.1:5000/api/v1/reviews/image/${id}`);

          // Votre API retourne { reviews: [...] }
          if (reviewsRes.data && reviewsRes.data.reviews) {
            setReviews(reviewsRes.data.reviews);
          }
        } catch (err) {
          if (err.response?.status === 404) {
            console.log("Aucune review pour cette image");
            setReviews([]);
          } else {
            console.error("Erreur lors de la récupération des reviews:", err);
            setReviews([]);
          }
        }
      } catch (err) {
        console.error("Erreur lors de la récupération :", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  /**
   * Soumet un nouveau commentaire sur la création
   * Nécessite une authentification valide
   *
   * @async
   * @param {Event} e - Événement de soumission du formulaire
   */
  const handleSubmitComment = async (e) => {
    e.preventDefault();

    if (!newComment.trim()) {
      alert('Le commentaire ne peut pas être vide');
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
      alert('Vous devez être connecté pour commenter');
      navigate('/login');
      return;
    }

    setSubmitting(true);

    try {
      // POST selon votre API reviews
      await axios.post(
        `http://127.0.0.1:5000/api/v1/reviews/`,
        {
          comment: newComment,
          image_post_id: parseInt(id)
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      // Recharger les reviews
      const reviewsRes = await axios.get(`http://127.0.0.1:5000/api/v1/reviews/image/${id}`);

      if (reviewsRes.data && reviewsRes.data.reviews) {
        setReviews(reviewsRes.data.reviews);
      }

      // Réinitialiser le formulaire
      setNewComment('');
      alert('Commentaire publié avec succès !');

    } catch (err) {
      console.error("Erreur lors de l'envoi du commentaire:", err);
      if (err.response?.status === 401) {
        alert('Session expirée. Veuillez vous reconnecter.');
        navigate('/login');
      } else if (err.response?.status === 400) {
        alert(err.response.data.error || "Erreur lors de l'envoi du commentaire");
      } else {
        alert("Erreur lors de l'envoi du commentaire");
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="contenu-principal">
        <div className="creation-detail-loading">
          <p>Chargement de la création...</p>
        </div>
      </div>
    );
  }

  if (!creation) {
    return (
      <div className="contenu-principal">
        <div className="creation-detail-error">
          <p>Création introuvable.</p>
          <button onClick={() => navigate('/creations')} className="button_creation">
            Retour aux créations
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="contenu-principal">
      <div className="creation-detail-container">

        {/* Layout principal : Image à gauche, Commentaires à droite */}
        <div className="creation-detail-layout">

          {/* à gauche - IMAGE (visible pour tous)  */}
          <div className="creation-detail-left">
            <div className="creation-image-container">
              <img
                src={creation.image_data}
                alt={creation.title}
                className="creation-detail-image"
              />
            </div>

            <div className="creation-info">
              <h1>{creation.title}</h1>
              {creation.description && (
                <p className="creation-description">{creation.description}</p>
              )}
              <div className="creation-meta">
                <p><strong>Publié le :</strong> {new Date(creation.created_at).toLocaleDateString('fr-FR')}</p>
                {creation.user && (
                  <p><strong>Par :</strong> {creation.user.first_name || creation.user.email}</p>
                )}
              </div>
            </div>
          </div>

          {/* à droite - COMMENTAIRES (visible pour tous) */}
          <div className="creation-detail-right">

            {/*  formulaire d'ajout uniquement si authentifié  */}
            {isAuthenticated ? (
              <div className="comment-form-container">
                <h3>Laisser un commentaire</h3>
                <form onSubmit={handleSubmitComment} className="comment-form">
                  <textarea
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    placeholder="Partagez votre avis sur cette création..."
                    rows={1}
                    className="input_creations textarea"
                    required
                    disabled={submitting}
                  />

                  <button
                    type="submit"
                    className="button_creation2"
                    disabled={submitting}
                  >
                    {submitting ? 'Envoi...' : 'Publier'}
                  </button>
                </form>
              </div>
            ) : (
              // Message pour les non-authentifiés
              <div className="comment-login-prompt">
                <p>Connectez-vous pour laisser un commentaire</p>
                <button
                  onClick={() => navigate('/login')}
                  className="button_creation2"
                >
                  Se connecter
                </button>
              </div>
            )}

            {/*  Liste des commentaires - visible pour TOUS */}
            <div className="comments-list">
              <h3>Tous les commentaires</h3>

              {reviews.length > 0 ? (
                reviews.map((review) => (
                  <div key={review.id} className="comment-card">
                    <div className="comment-header">
                      <span className="comment-author">
                        👤 {review.author || `Utilisateur #${review.user_id}`}
                      </span>
                      <span className="comment-date">
                        {review.created_at && new Date(review.created_at).toLocaleDateString('fr-FR', {
                          day: 'numeric',
                          month: 'short',
                          year: 'numeric'
                        })}
                      </span>
                    </div>
                    <p className="comment-text">{review.comment}</p>
                  </div>
                ))
              ) : (
                <div className="no-comments">
                  <p>Aucun commentaire pour le moment.</p>
                  <p>Soyez le premier à donner votre avis !</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
        {/* Bouton retour */}
        <button
          onClick={() => navigate('/creations')}
          className="creation-detail-back-btn"
        >
          ← Retour à la galerie
        </button>
    </div>
  );
}

export default CreationDetail;
