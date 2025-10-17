const API_URL = 'http://localhost:5000/api';

export const mapAPI = {
  // Récupérer tous les markers
  getMarkers: async () => {
    const response = await fetch(`${API_URL}/markers`);
    if (!response.ok) throw new Error('Erreur chargement markers');
    return response.json();
  },

  // Récupérer tous les polygones
  getPolygons: async () => {
    const response = await fetch(`${API_URL}/polygons`);
    if (!response.ok) throw new Error('Erreur chargement polygones');
    return response.json();
  }
};
