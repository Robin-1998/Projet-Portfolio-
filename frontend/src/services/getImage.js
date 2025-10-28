/*
  Fonction utilitaire pour générer le chemin d'une image locale stockée
  dans le dossier "public"
*/
const getImagePath = (name, folder) => {
  const fileName = name
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // enlève accents
    .replace(/\s+/g, "_") // remplace espaces par _
    .toLowerCase() + ".png";

  return `/${folder}/${fileName}`;
};
export default getImagePath;
