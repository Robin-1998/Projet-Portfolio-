import {
  MapContainer,
  ImageOverlay,
  Marker,
  Popup,
  Polygon,
  Tooltip
} from 'react-leaflet'; 

/* MapContainer est le composant qui contient toute la carte, il permet de définir :
	- la taille de la carte
	- le système de coordonnées pour image
	ex : <MapContainer zoom={0} center={[500, 500]} />
	*/

/* ImageOverlay sert à afficher une image personnalisée comme fond de carte Il faut lui donner :
	- une URL de l'image
	- des coordonnées de placements
	exemple : <ImageOverlay url="/images/carte.jpg" bounds={[[0, 0], [1000, 2000]]} />
*/

/* Marker sert à afficher un marqueur sur la carte. Il faut lui donner
	x, y ou lat ou lng
	il peut contenir le popup
	exemple : <Marker position={[800, 1000]} />
*/

/* Popup est une bulle d'information qui s'affiche quand on clique sur un marqueur ou un élément. Il faut :
	- l'imbriquer dans un marker ou un polygon
	- il s'ouvre quand on clique
	exemple : <Marker position={[800, 1000]}>
				<Popup>Voici la Comté</Popup>
			  </Marker>
 */
/* Polygon -> pour dessiner des régions */
/* Tooltip -> info bulle visible sans clic */
