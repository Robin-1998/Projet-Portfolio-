/*
  Fonction utilitaire pour générer le chemin d'une image locale stockée
  dans le dossier "public"
*/
const getImagePath = (name, folder) => {
  const fileName = name.toLowerCase() + '.png';
  // retourne une chaîne de caractères qui représente le chemin relatif à
  // la racine du site
  return `/${folder}/${fileName}`; 
  // Chemin relatif à la racine du site car public avec vite est 
  // servi automatiquement à la racine du site quand le serveur est démarré
};

export default getImagePath;

