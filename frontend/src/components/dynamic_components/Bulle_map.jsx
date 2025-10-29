/**
 * Module de gestion des icônes de marqueurs pour la carte interactive
 * @module Bulle_map
 */

import React, { useEffect, useState } from "react";
import { MapContainer, Marker, Popup, useMapEvents } from "react-leaflet";
import L from "leaflet";
import 'leaflet/dist/leaflet.css';

/**
 * Crée une icône de marqueur personnalisée avec bulle colorée et image
 *
 * @param {string} imageUrl - Chemin vers l'image de l'icône
 * @param {string} [color="#3b7a2f"] - Couleur de fond (hex)
 * @param {number} [size=48] - Taille en pixels
 * @returns {L.DivIcon} Icône Leaflet
 */
export const createStickerIcon = (imageUrl, color = "#3b7a2f", size = 48) => {
  const svg = `
    <svg width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
      <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2 - 2}" fill="${color}" stroke="black" stroke-width="1.5"/>
      <image href="${imageUrl}" x="${size * 0.166}" y="${size * 0.166}" height="${size * 0.666}" width="${size * 0.666}" />
    </svg>
  `;
  return L.divIcon({
    html: svg,
    className: "custom-sticker-icon",
    iconSize: [size, size],
    iconAnchor: [size / 2, size],
    popupAnchor: [0, -size],
  });
};

/**
 * Dictionnaire des icônes par type de lieu
 * Chaque fonction retourne une icône Leaflet avec couleur et image appropriées
 *
 * @constant {Object.<string, Function>}
 */
export const CATEGORY_ICONS = {
  montagne: (size = 48) => createStickerIcon("/bulle_map/montagne.png", "#8b5e3b81", size),
  forteresse: (size = 48) => createStickerIcon("/bulle_map/fortresse.png", "#7978777c", size),
  ville: (size = 48) => createStickerIcon("/bulle_map/ville.png", "#c2b05880", size),
  capitale: (size = 48) => createStickerIcon("/bulle_map/capitale.png", "#da616186", size),
  eau: (size = 48) => createStickerIcon("/bulle_map/eau.png", "#619edb94", size),
  ruine: (size = 48) => createStickerIcon("/bulle_map/ruine.png", "#a7a4a49a", size),
  dark: (size = 48) => createStickerIcon("/bulle_map/dark.png", "#ff00007a", size),
  mine: (size = 48) => createStickerIcon("/bulle_map/mine.png", "#a1887f91", size),
  port: (size = 48) => createStickerIcon("/bulle_map/port.png", "#b6dff596", size),
  pont: (size = 48) => createStickerIcon("/bulle_map/pont.png", "#6d4c418e", size),
  plaine: (size = 48) => createStickerIcon("/bulle_map/plaine.png", "#c5e1a591", size),
  chemin: (size = 48) => createStickerIcon("/bulle_map/chemin.png", "#fbc12d8f", size),
  monument: (size = 48) => createStickerIcon("/bulle_map/monument.png", "#ff881098", size),
  special: (size = 48) => createStickerIcon("/bulle_map/special.png", "#cdb3eb9a", size),
  foret: (size = 48) => createStickerIcon("/bulle_map/foret.png", "#66a55a81", size),
  default: (size = 48) => createStickerIcon("/bulle_map/default.png", "#6d0808ff", size),
};
