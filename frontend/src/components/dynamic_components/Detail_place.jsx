/**
 * Composant modal d'affichage du détail d'un lieu de la Terre du Milieu
 * @module DetailPlace
 */

import React from 'react';
import '../../styles/detail_place.css';

/**
 * Affiche une modale avec les informations détaillées d'un lieu
 * (nom, description, image et sections descriptives)
 *
 * @component
 * @param {Object} props - Propriétés du composant
 * @param {Object|null} props.place - Données du lieu à afficher
 * @param {string} props.place.name - Nom du lieu
 * @param {string} props.place.description - Description principale
 * @param {string} [props.place.image_url] - URL de l'image principale
 * @param {Array} [props.place.descriptions] - Sections descriptives additionnelles
 * @param {Function} props.onClose - Callback pour fermer la modale
 * @returns {JSX.Element|null} Modale ou null si pas de lieu
 */
const DetailPlace = ({ place, onClose }) => {
  if (!place) return null;

  // Cherche l'image principale
  const imageUrl = place.image_url ||
    place.detailed_sections?.find(s => s.image_url && !s.image_url.includes('ornement'))?.image_url;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>
        <div className="modal-body">
          {/* Flex container : description à gauche, image à droite */}
          <div className="modal-body-flex">
            {/* Bloc texte à gauche */}
            <div className="modal-text-container">
              <div className="modal-header">
                <h2 className='titre2'>{place.name}</h2>
              </div>

              <div className="modal-description">
                <p className="modal-main-description">{place.description}</p>
              </div>
            </div>

            {/* Image à droite */}
            {imageUrl && (
              <div className="modal-image-container">
                <img
                  src={imageUrl}
                  alt={place.name}
                  className="modal-main-image"
                />
              </div>
            )}
          </div>

          {/* ✅ AJOUT : Affichage des descriptions */}
          {place.descriptions && place.descriptions.length > 0 && (
            <div className="modal-descriptions">
              {place.descriptions.map((desc) => (
                <div key={desc.id} className="modal-description-item">
                  <h4 className='titre4'>{desc.title}</h4>
                  <p className='p-place'>{desc.content}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DetailPlace;
