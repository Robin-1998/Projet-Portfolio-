/**
 * @module getImagePath
 * Génère le chemin d’une image locale à partir d’un nom et d’un dossier.
 */

/**
 * Crée un chemin d’image à partir du nom fourni.
 * @param {string} name - Nom de base du fichier (avec ou sans accents/espaces).
 * @param {string} folder - Nom du dossier dans "public".
 * @returns {string} Chemin relatif de l’image (ex. /images/nom_image.png).
 */
const getImagePath = (name, folder) => {
  // Nettoie le nom : enlève les accents, remplace les espaces et met en minuscule
  const fileName = name
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // Supprime les accents
    .replace(/\s+/g, "_") // Remplace les espaces par des underscores
    .toLowerCase() + ".png";

  return `/${folder}/${fileName}`;
};
export default getImagePath;
