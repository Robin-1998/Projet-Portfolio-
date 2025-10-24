import React from 'react';

const DetailPlace = ({ place, onClose }) => {
  if (!place) return null;

  // Cherche l'image principale, sinon prend la première image d'une section
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

          {/* Sections détaillées */}
          {place.detailed_sections && place.detailed_sections.length > 0 && (
            <div className="modal-sections">
              {place.detailed_sections.map((section, index) => (
                <div key={index} className="modal-section">
                  <h3 className='titre3'>{section.title}</h3>
                  {section.image_url && (
                    <img
                      src={section.image_url}
                      alt={section.title}
                      className="modal-section-image"
                    />
                  )}
                  <p className='p-place'>{section.content}</p>
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
