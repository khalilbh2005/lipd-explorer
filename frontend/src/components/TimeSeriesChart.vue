<!-- frontend/src/components/TimeSeriesChart.vue -->
<!-- Composant réutilisable : affiche une série temporelle avec Chart.js -->

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale
} from 'chart.js'

// ============================================================
// ENREGISTREMENT DES MODULES CHART.JS
// ============================================================
// Chart.js est modulaire : on n'enregistre que ce qu'on utilise
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale
)

// ============================================================
// PROPS : ce que le parent nous passe
// ============================================================
const props = defineProps({
  dataPoints: {
    type: Array,
    required: true
  },
  variableName: {
    type: String,
    default: 'Valeur'
  },
  variableUnits: {
    type: String,
    default: ''
  },
  timeAxisName: {
    type: String,
    default: 'Temps'
  },
  timeUnits: {
    type: String,
    default: ''
  }
})

// ============================================================
// DONNÉES DU GRAPHIQUE (réactives)
// ============================================================
const chartData = ref({
  labels: [],
  datasets: []
})

const chartOptions = ref({})

// ============================================================
// FONCTION : construit les données pour Chart.js
// ============================================================
function construireGraphique() {
  // Extraction des labels (temps) et valeurs
  const labels = []
  const valeurs = []
  
  for (const point of props.dataPoints) {
    labels.push(point.time)
    valeurs.push(point.value)
  }
  
  // Structure attendue par Chart.js
  chartData.value = {
    labels: labels,
    datasets: [
      {
        label: `${props.variableName} (${props.variableUnits})`,
        data: valeurs,
        borderColor: '#1976D2',
        backgroundColor: 'rgba(25, 118, 210, 0.1)',
        borderWidth: 1.5,
        pointRadius: 0,           // Pas de points (on a 2000+ points, ce serait moche)
        pointHoverRadius: 5,      // Points visibles au survol
        tension: 0.1,             // Légère courbure
      }
    ]
  }
  
  // Options de configuration
  chartOptions.value = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: `${props.variableName} en fonction de ${props.timeAxisName}`,
        font: { size: 16 }
      },
      legend: {
        position: 'top',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          title: function(items) {
            return `${props.timeAxisName} : ${items[0].label} ${props.timeUnits}`
          },
          label: function(item) {
            return `${props.variableName} : ${item.parsed.y.toFixed(3)} ${props.variableUnits}`
          }
        }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: `${props.timeAxisName} (${props.timeUnits})`,
          font: { size: 13 }
        },
        ticks: {
          maxTicksLimit: 15  // limite le nombre de labels affichés
        }
      },
      y: {
        title: {
          display: true,
          text: `${props.variableName} (${props.variableUnits})`,
          font: { size: 13 }
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  }
}

// ============================================================
// CYCLE DE VIE
// ============================================================
onMounted(() => {
  construireGraphique()
})

// Si les props changent (nouvelle variable sélectionnée), on reconstruit
watch(() => props.dataPoints, () => {
  construireGraphique()
})
</script>

<template>
  <div class="chart-container">
    <Line 
      v-if="chartData.datasets.length > 0"
      :data="chartData" 
      :options="chartOptions"
    />
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  height: 450px;
  width: 100%;
}
</style>    