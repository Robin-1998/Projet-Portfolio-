import React from 'react';

/**
 * Composant Tooltip
 * Affiche un texte d'info-bulle lorsque l'utilisateur survole son enfant
 *
 * @param {Object} props
 * @param {string} props.text - Le texte à afficher dans la bulle
 * @param {React.ReactNode} props.children - L'élément autour duquel la bulle apparaît
 */
function Tooltip({ text, children }) {
  return (
    // Conteneur principal : position relative pour permettre l'affichage de la bulle au-dessus
    <span className="tooltip-container">
      {children}
      <span className="tooltip-text">{text}</span>
    </span>
  );
}

export default Tooltip;
