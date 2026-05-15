// frontend/src/services/api.js
// Service centralisé pour communiquer avec le backend Django

import axios from 'axios'

// ============================================================
// CONFIGURATION DE BASE
// ============================================================

// On crée une instance Axios pré-configurée
// → toutes les URLs seront préfixées par http://localhost:8000
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,  // 30 secondes max (PyLiPD peut être lent au premier chargement)
  headers: {
    'Content-Type': 'application/json',
  },
})

// ============================================================
// FONCTIONS API (une par endpoint Django)
// ============================================================

/**
 * Récupère la liste de tous les datasets disponibles.
 * Appelle : GET /api/datasets/
 */
export async function getDatasets() {
  try {
    const response = await apiClient.get('/api/datasets/')
    return response.data
  } catch (erreur) {
    console.error('❌ Erreur getDatasets :', erreur)
    throw erreur
  }
}

/**
 * Récupère les métadonnées + liste des variables d'un dataset.
 * Appelle : GET /api/datasets/<nom>/
 */
export async function getDatasetDetail(nomDataset) {
  try {
    const response = await apiClient.get(`/api/datasets/${nomDataset}/`)
    return response.data
  } catch (erreur) {
    console.error(`❌ Erreur getDatasetDetail(${nomDataset}) :`, erreur)
    throw erreur
  }
}

/**
 * Récupère les data points d'une variable spécifique.
 * Appelle : GET /api/datasets/<nom>/variables/<id>/
 */
export async function getVariableDataPoints(nomDataset, idVariable) {
  try {
    const response = await apiClient.get(
      `/api/datasets/${nomDataset}/variables/${idVariable}/`
    )
    return response.data
  } catch (erreur) {
    console.error(
      `❌ Erreur getVariableDataPoints(${nomDataset}, ${idVariable}) :`,
      erreur
    )
    throw erreur
  }
}

// On exporte aussi le client pour les cas particuliers
export default apiClient