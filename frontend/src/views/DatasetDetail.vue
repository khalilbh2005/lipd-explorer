<!-- frontend/src/views/DatasetDetail.vue -->
<!-- Page de detail d'un dataset : metadonnees + variables + graphique -->

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getDatasetDetail, getVariableDataPoints } from '../services/api'
import TimeSeriesChart from '../components/TimeSeriesChart.vue'

const route = useRoute()
const router = useRouter()
const datasetId = route.params.id

const data = ref(null)
const chargement = ref(false)
const erreur = ref(null)

const variableActive = ref(null)
const chargementGraphique = ref(false)
const erreurGraphique = ref(null)

async function chargerDetail() {
  chargement.value = true
  erreur.value = null
  try {
    const reponse = await getDatasetDetail(datasetId)
    data.value = reponse
    console.log('Detail charge :', reponse)
  } catch (e) {
    erreur.value = "Impossible de charger le dataset " + datasetId
    console.error(e)
  } finally {
    chargement.value = false
  }
}

async function visualiserVariable(idVariable) {
  chargementGraphique.value = true
  erreurGraphique.value = null
  variableActive.value = null
  try {
    const reponse = await getVariableDataPoints(datasetId, idVariable)
    variableActive.value = reponse
    console.log('Data points charges :', reponse)
    setTimeout(() => {
      const element = document.getElementById('graphique-section')
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    }, 200)
  } catch (e) {
    erreurGraphique.value = "Impossible de charger les data points"
    console.error(e)
  } finally {
    chargementGraphique.value = false
  }
}

function retourAccueil() {
  router.push('/')
}

function couleurStatut(statut) {
  if (statut === 'complete') return 'success'
  if (statut === 'non-numeric') return 'warning'
  return 'grey'
}

onMounted(() => {
  chargerDetail()
})
</script>

<template>
  <v-container>

    <v-btn
      prepend-icon="mdi-arrow-left"
      variant="text"
      class="mt-4 mb-2"
      @click="retourAccueil"
    >
      Retour aux datasets
    </v-btn>

    <v-row v-if="chargement" justify="center" class="mt-8">
      <v-progress-circular indeterminate color="primary" size="64" />
    </v-row>

    <v-alert v-if="erreur" type="error" variant="tonal" class="mt-4">
      {{ erreur }}
    </v-alert>

    <div v-if="data && !chargement">

      <v-card class="mt-4" elevation="3">
        <v-card-item>
          <template v-slot:prepend>
            <v-icon icon="mdi-database" color="primary" size="x-large" />
          </template>
          <v-card-title class="text-h4">
            {{ data.metadata.dataSetName }}
          </v-card-title>
          <v-card-subtitle>
            <v-chip size="small" color="secondary" prepend-icon="mdi-layers">
              {{ data.metadata.archiveType }}
            </v-chip>
          </v-card-subtitle>
        </v-card-item>

        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <h3 class="text-h6 mb-2">
                <v-icon icon="mdi-map-marker" color="accent" />
                Geolocalisation
              </h3>
              <v-table density="compact">
                <tbody>
                  <tr>
                    <td><strong>Site</strong></td>
                    <td>{{ data.metadata.location.siteName || 'N/A' }}</td>
                  </tr>
                  <tr>
                    <td><strong>Latitude</strong></td>
                    <td>{{ data.metadata.location.latitude || 'N/A' }}</td>
                  </tr>
                  <tr>
                    <td><strong>Longitude</strong></td>
                    <td>{{ data.metadata.location.longitude || 'N/A' }}</td>
                  </tr>
                  <tr v-if="data.metadata.location.elevation">
                    <td><strong>Elevation</strong></td>
                    <td>{{ data.metadata.location.elevation }} m</td>
                  </tr>
                </tbody>
              </v-table>
            </v-col>

            <v-col cols="12" md="6" v-if="data.metadata.publication">
              <h3 class="text-h6 mb-2">
                <v-icon icon="mdi-book-open-page-variant" color="accent" />
                Publication source
              </h3>
              <v-table density="compact">
                <tbody>
                  <tr>
                    <td><strong>Auteurs</strong></td>
                    <td>{{ data.metadata.publication.authors.join(', ') }}</td>
                  </tr>
                  <tr>
                    <td><strong>Annee</strong></td>
                    <td>{{ data.metadata.publication.year }}</td>
                  </tr>
                  <tr v-if="data.metadata.publication.journal">
                    <td><strong>Journal</strong></td>
                    <td>{{ data.metadata.publication.journal }}</td>
                  </tr>
                  <tr v-if="data.metadata.publication.title">
                    <td><strong>Titre</strong></td>
                    <td>{{ data.metadata.publication.title }}</td>
                  </tr>
                </tbody>
              </v-table>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <v-card class="mt-4" elevation="3">
        <v-card-title class="text-h5">
          <v-icon icon="mdi-chart-timeline-variant" color="primary" class="me-2" />
          Variables disponibles ({{ data.variables.length }})
        </v-card-title>

        <v-card-text>
          <v-table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nom</th>
                <th>Unite</th>
                <th>Statut</th>
                <th>Points</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="variable in data.variables" :key="variable.id">
                <td>{{ variable.id }}</td>
                <td>{{ variable.name || 'N/A' }}</td>
                <td>{{ variable.units || 'N/A' }}</td>
                <td>
                  <v-chip
                    size="small"
                    :color="couleurStatut(variable.status)"
                    variant="tonal"
                  >
                    {{ variable.status }}
                  </v-chip>
                </td>
                <td>{{ variable.numberOfPoints }}</td>
                <td>
                  <v-btn
                    v-if="variable.status === 'complete'"
                    size="small"
                    color="primary"
                    variant="elevated"
                    prepend-icon="mdi-chart-line"
                    @click="visualiserVariable(variable.id)"
                  >
                    Visualiser
                  </v-btn>
                  <span v-else class="text-grey-darken-1">-</span>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>

      <v-card
        v-if="variableActive || chargementGraphique"
        id="graphique-section"
        class="mt-4 mb-8"
        elevation="3"
      >
        <v-card-title class="text-h5">
          <v-icon icon="mdi-chart-line" color="primary" class="me-2" />
          Visualisation de la serie temporelle
        </v-card-title>

        <v-card-text v-if="chargementGraphique" class="text-center pa-8">
          <v-progress-circular indeterminate color="primary" size="48" />
          <p class="mt-4 text-grey-darken-1">Chargement des data points...</p>
        </v-card-text>

        <v-alert
          v-if="erreurGraphique"
          type="error"
          variant="tonal"
          class="ma-4"
        >
          {{ erreurGraphique }}
        </v-alert>

        <div v-if="variableActive && !chargementGraphique">
          <v-card-text>
            <v-row>
              <v-col cols="6" sm="3">
                <strong>Variable :</strong><br>
                {{ variableActive.variable.name }}
              </v-col>
              <v-col cols="6" sm="3">
                <strong>Unite :</strong><br>
                {{ variableActive.variable.units }}
              </v-col>
              <v-col cols="6" sm="3">
                <strong>Nombre de points :</strong><br>
                {{ variableActive.stats.totalPoints }}
              </v-col>
              <v-col cols="6" sm="3">
                <strong>Periode :</strong><br>
                {{ variableActive.stats.timeMin }} -> {{ variableActive.stats.timeMax }} {{ variableActive.timeAxis.units }}
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-text>
            <TimeSeriesChart
              :data-points="variableActive.dataPoints"
              :variable-name="variableActive.variable.name"
              :variable-units="variableActive.variable.units"
              :time-axis-name="variableActive.timeAxis.name"
              :time-units="variableActive.timeAxis.units"
            />
          </v-card-text>
        </div>
      </v-card>

    </div>

  </v-container>
</template>
