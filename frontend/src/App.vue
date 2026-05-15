<!-- frontend/src/App.vue -->
<!-- Composant racine : barre de nav + emplacement des pages + footer -->

<script setup>
// Liens externes
const lienGithub = 'https://github.com/khalilbh2005'
const lienPortfolio = 'https://khalilbh2005.github.io/portfolio/'
</script>

<template>
  <v-app>

    <!-- ============================================================ -->
    <!-- BARRE DE NAVIGATION                                          -->
    <!-- ============================================================ -->
    <v-app-bar color="primary" elevation="2">
      <v-app-bar-title>
        <v-icon icon="mdi-earth" class="me-2" />
        LiPD Explorer
      </v-app-bar-title>

      <v-spacer />

      <!-- Lien vers le portfolio personnel -->
      <v-btn
        icon="mdi-account-circle"
        :href="lienPortfolio"
        target="_blank"
        rel="noopener"
        title="Mon portfolio"
      />

      <!-- Lien vers GitHub -->
      <v-btn
        icon="mdi-github"
        :href="lienGithub"
        target="_blank"
        rel="noopener"
        title="Mon profil GitHub"
      />
    </v-app-bar>

    <!-- ============================================================ -->
    <!-- CONTENU PRINCIPAL (pages du router)                          -->
    <!-- ============================================================ -->
    <v-main>
      <router-view />
    </v-main>

    <!-- ============================================================ -->
    <!-- FOOTER                                                       -->
    <!-- ============================================================ -->
    <v-footer color="grey-lighten-4" class="d-flex flex-column align-center pa-6">
      <p class="text-body-2 text-grey-darken-2 mb-2 text-center">
        Projet d'entraînement sur la manipulation du format de données
        <strong>LiPD</strong> (Linked Paleo Data)
      </p>
      <p class="text-caption text-grey-darken-1">
        © 2026 ·
        <a
          :href="lienPortfolio"
          target="_blank"
          rel="noopener"
          class="text-primary text-decoration-none"
        >
          Khalil Ben Hamza
        </a>
      </p>
    </v-footer>

  </v-app>
</template>