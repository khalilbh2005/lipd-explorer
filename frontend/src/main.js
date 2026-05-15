// frontend/src/main.js
// Point d'entrée de l'application Vue

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// ============================================================
// CONFIGURATION VUETIFY
// ============================================================
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Icônes Material Design
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',      // Bleu IPSL
          secondary: '#26A69A',    // Turquoise (climat/océan)
          accent: '#FF6F00',       // Orange (chaleur/géologie)
          background: '#F5F7FA',
        }
      }
    }
  }
})

// ============================================================
// CRÉATION DE L'APPLICATION
// ============================================================
const app = createApp(App)

app.use(router)
app.use(vuetify)

app.mount('#app')