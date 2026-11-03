/**
 * Sélection de l'accueil, décidée à part de la publication : un article ancien peut y être remis en lumière.
 * Slugs à mettre en avant, dans l'ordre. Un slug absent du corpus est ignoré.
 * Liste vide → sélection automatique (le plus récent de chaque format).
 */
export const SELECTION_ACCUEIL: { actualite: string[]; connaissance: string[] } = {
  actualite: [],
  connaissance: [],
};
