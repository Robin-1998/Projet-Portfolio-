/**
 * @module mapAPI
 * Fournit les fonctions d’accès à l’API (markers et polygones).
 */

const API_URL = 'http://localhost:5000/api';

export const mapAPI = {
  /**
   * Obtenir tous les marqueurs.
   * @returns {Promise<Object>} Données des marqueurs.
   */
  getMarkers: async () => {
    // Requête API pour récupérer les marqueurs
    const response = await fetch(`${API_URL}/markers`);
    if (!response.ok) throw new Error('Erreur chargement markers');
    return response.json();
  },

  /**
   * Obtenir tous les polygones.
   * @returns {Promise<Object>} Données des polygones.
   */
  getPolygons: async () => {
    // Requête API pour récupérer les polygones
    const response = await fetch(`${API_URL}/polygons`);
    if (!response.ok) throw new Error('Erreur chargement polygones');
    return response.json();
  },
};
