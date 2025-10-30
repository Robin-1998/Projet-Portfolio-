/**
 * Composant de galerie et publication de créations artistiques
 * @module CreationsList
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import '../../styles/creations.css';

/**
 * Affiche la galerie de créations artistiques et permet aux utilisateurs authentifiés
 * de publier leurs propres créations
 *
 * @component
 * @returns {JSX.Element} Page de galerie avec formulaire de publication
 */
function CreationsList() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);
  const [base64Image, setBase64Image] = useState('');
  const [mimeType, setMimeType] = useState('');
  const [message, setMessage] = useState('');
  const [images, setImages] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  /**
   * Effet pour vérifier l'authentification et charger les images au montage
   */
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);

    // Récupérer les images (accessible à tous)
    axios.get('http://127.0.0.1:5000/api/v1/images')
      .then(res => setImages(res.data))
      .catch(err => {
        console.error("Erreur en récupérant les images", err);
        setImages([]);
      });
  }, []);

  /**
   * Gère la sélection d'un fichier image et sa conversion en base64
   *
   * @param {Event} e - Événement de changement de fichier
   */
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    setMimeType(selectedFile.type);
    setFile(selectedFile);

    const reader = new FileReader();
    reader.onloadend = () => {
      const base64String = reader.result.split(',')[1];
      setBase64Image(base64String);
    };
    reader.readAsDataURL(selectedFile);
  };

  /**
   * Soumet une nouvelle création artistique à l'API
   * Nécessite une authentification valide
   *
   * @async
   * @param {Event} e - Événement de soumission du formulaire
   */
  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('token');
    if (!token) {
      setMessage('Vous devez être connecté pour poster une image');
      return;
    }

    if (!title || !base64Image || !mimeType) {
      setMessage('Titre et image sont obligatoires');
      return;
    }

    try {
      const payload = {
        title,
        description,
        image_data: base64Image,
        image_mime_type: mimeType,
      };

      const response = await axios.post('http://127.0.0.1:5000/api/v1/images', payload, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      });

      setMessage('Image postée avec succès !');
      setTitle('');
      setDescription('');
      setFile(null);
      setBase64Image('');
      setMimeType('');

      // Recharger les images
      const res = await axios.get('http://127.0.0.1:5000/api/v1/images');
      setImages(res.data);

    } catch (error) {
      if (error.response?.status === 401) {
        setMessage('Session expirée. Veuillez vous reconnecter.');
        navigate('/login');
      } else {
        setMessage(`Erreur lors de l'envoi : ${error.response?.data?.error || error.message}`);
      }
    }
  };

  return (
    <div className="contenu-principal">
      <article className='Blocks_creations'>
        <div className="block_creations_left">
          <p>Bienvenue dans la section dédié aux créations artistiques.
            <br/>Pour pouvoir poster vos créations artistiques, vous devez être inscrit et connecté.</p>
          <section>
            <p>
              Merci de respecter les règles suivantes :
            </p>
            <ol>
              <li>Pas de photo en dehors de l'univers de tolkien.</li>
              <li>Uniquement des créations artistiques (pas de photos tirées des films ou des livres).</li>
              <li>Aucun commentaires à caractère sexuel, raciste, homophobe, religieux ou politique ne sera toléré — tout manquement entraînera la suppression du compte.</li>
            </ol>
          </section>
          <section className='block_post_image'>
            <h3>Poster une image :</h3>
            {isAuthenticated ? (
              <form onSubmit={handleSubmit} className='post_conected'>
                <label>
                  <input
                    placeholder="Titre de l'image"
                    type="text"
                    value={title}
                    onChange={e => setTitle(e.target.value)}
                    required
                    className='input_creations'
                  />
                </label>

              <label>
                <input
                    placeholder="Description de l'image"
                  value={description}
                  onChange={e => setDescription(e.target.value)}
                  className='input_creations'
                />
              </label>

              <label className="file-label">
                Choisir une image
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  required
                />
              </label>

              {file && (
                <p className="file-name-display">
                  Fichier sélectionné : {file.name}
                </p>
              )}

              <button type="submit" className='button_creation'>Envoyer</button>

              {message && <p>{message}</p>}
              </form>
            ) : (
              <div className='post_disconected'>
                <button onClick={() => navigate('/login')} className='button_creation'>Se connecter</button>
                <p>Vous devez être connecté pour poster une image.</p>
              </div>
            )}
          </section>
        </div>
        <div className='block_creations_right'>
        <h2>Gallerie d'images</h2>
        {images.map(img => (
          <Link
            to={`/creations/${img.id}`}
            key={img.id}
            className='block_img_p'
          >
            <img
              src={img.image_data}
              alt={img.title}
              className='image_gallerie_art'
            />
            <p><strong>{img.title}</strong></p>
          </Link>
        ))}
        </div>
      </article>
    </div>
  );
}

export default CreationsList;
