import React from 'react';
import '../../styles/detail_place.css';

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
