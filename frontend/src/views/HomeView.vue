<!-- frontend/src/views/HomeView.vue -->
<!-- Page d'accueil : liste des datasets disponibles -->

<script setup>
// ============================================================
// IMPORTS
// ============================================================
import { ref, onMounted } from 'vue'
import { getDatasets } from '../services/api'

// ============================================================
// ÉTAT RÉACTIF (reactive state)
// ============================================================

// La liste des datasets (commence vide)
const datasets = ref([])

// Indicateur de chargement (true quand on attend la réponse de l'API)
const chargement = ref(false)

// Message d'erreur (null si pas d'erreur)
const erreur = ref(null)

// ============================================================
// FONCTIONS
// ============================================================

/**
 * Charge la liste des datasets depuis l'API Django.
 */
async function chargerDatasets() {
  chargement.value = true
  erreur.value = null
  
  try {
    const reponse = await getDatasets()
    datasets.value = reponse.results || []
    console.log('✅ Datasets chargés :', datasets.value)
  } catch (e) {
    erreur.value = "Impossible de charger les datasets. Vérifie que le backend Django tourne sur le port 8000."
    console.error(e)
  } finally {
    chargement.value = false
  }
}

// ============================================================
// CYCLE DE VIE : appelé quand le composant est monté dans le DOM
// ============================================================
onMounted(() => {
  chargerDatasets()
})
</script>

<template>
  <v-container>
    <!-- En-tête de la page -->
    <v-row class="mt-4">
      <v-col cols="12">
        <h1 class="text-h3 mb-2">
          <v-icon icon="mdi-earth" class="me-2" color="primary" />
          Datasets paléoclimatiques
        </h1>
        <p class="text-body-1 text-grey-darken-1">
          Explorez les datasets au format LiPD (Linked Paleo Data)
        </p>
      </v-col>
    </v-row>

    <!-- État : chargement -->
    <v-row v-if="chargement" justify="center" class="mt-8">
      <v-progress-circular 
        indeterminate 
        color="primary" 
        size="64"
      />
    </v-row>

    <!-- État : erreur -->
    <v-alert 
      v-if="erreur" 
      type="error" 
      variant="tonal"
      class="mt-4"
    >
      {{ erreur }}
    </v-alert>

    <!-- État : succès, liste des datasets -->
    <v-row v-if="!chargement && !erreur" class="mt-4">
      <v-col 
        v-for="dataset in datasets" 
        :key="dataset.id"
        cols="12" 
        md="6" 
        lg="4"
      >
        <v-card elevation="3" hover>
          <v-card-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-database" color="primary" size="large" />
            </template>
            <v-card-title>{{ dataset.id }}</v-card-title>
            <v-card-subtitle>{{ dataset.archiveType }}</v-card-subtitle>
          </v-card-item>
          
          <v-card-text>
            <p class="text-body-2">{{ dataset.description }}</p>
            <v-chip 
              size="small" 
              color="secondary" 
              variant="tonal"
              class="mt-2"
            >
              {{ dataset.name }}
            </v-chip>
          </v-card-text>
          
          <v-card-actions>
            <v-btn 
                color="primary" 
                variant="elevated"
                prepend-icon="mdi-magnify"
                block
                :to="`/datasets/${dataset.id}`"`
            >
            Explorer
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- État : aucun dataset -->
    <v-alert 
      v-if="!chargement && !erreur && datasets.length === 0" 
      type="info"
      variant="tonal"
      class="mt-4"
    >
      Aucun dataset disponible pour le moment.
    </v-alert>
  </v-container>
</template>