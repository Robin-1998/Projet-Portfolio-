import React, { useState } from 'react';

const DetailedPlaceModal = ({ place, onClose }) => {
  if (!place) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>

        <div className="modal-header">
          <h2>{place.name}</h2>
        </div>

        {place.image_url && (
          <div className="modal-image-container">
            <img
              src={place.image_url}
              alt={place.name}
              className="modal-main-image"
            />
          </div>
        )}

        <div className="modal-body">
          {/* Description principale */}
          <div className="modal-section">
            <p className="modal-main-description">{place.description}</p>
          </div>

          {/* Sections détaillées */}
          {place.detailed_sections && place.detailed_sections.length > 0 && (
            <div className="modal-sections">
              {place.detailed_sections.map((section, index) => (
                <div key={index} className="modal-section">
                  <h3>{section.title}</h3>
                  {section.image_url && (
                    <img
                      src={section.image_url}
                      alt={section.title}
                      className="modal-section-image"
                    />
                  )}
                  <p>{section.content}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DetailedPlaceModal;
