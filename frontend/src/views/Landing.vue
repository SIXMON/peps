<template>
  <div>
    <ContributionOverlay
      :visible="showContributionOverlay"
      @done="showContributionOverlay = false"
    />
    <v-container class="constrained">
      <!-- Intro top -->
      <v-row>
        <v-col cols="12">
          <div class="display-1">
            REX Agri : le partage d'expérience entre agriculteurs
          </div>
          <v-card-text
            class="subtitle-2"
            style="padding: 16px 16px 0px 0;"
          >Découvrez les essais et les pratiques innovantes mises en place par des agriculteurs près de chez vous. <br> Partagez les vôtres et faites avancer la transition.</v-card-text>
          <v-card-text
            class="subtitle-2"
            style="padding: 16px 16px 0px 0;"
          >Tous les retours d'expérience présents sur REX Agri ont été sélectionnées et respectent la <a target="_blank" href="https://cellar-c2.services.clever-cloud.com/peps-cellar/Charte_REX_Agri.pdf">charte de référencement</a> pour assurer la pertinence de leur contenu.</v-card-text>
        </v-col>
      </v-row>

      <!-- Experiment filters -->
      <h2
        class="title pa-0"
        id="explore-xp"
        style="margin: 30px 0px 10px 0px;"
      >Explorez les retours d'expérience</h2>
      <ExperimentFilter v-if="experimentsFetched" />

      
      <!-- Newsletter -->
      <div
        style="background-color: white; margin: 10px -16px 30px -16px;padding: 16px;border-radius: 5px; box-shadow: 0 4px 8px rgb(0 0 0 / 15%);"
      >
      <p
        class="body-1 pa-0"
        style="margin: 5px 0px; color:#ea5403; font-weight: bold;"
      >Pour recevoir les nouveaux retours d'expérience, abonnez-nous : </p>
      <MailChimpForm />
      </div>

      <!-- Experiments by location -->
      <h2
        class="title pa-0"
        style="margin: 16px 0px 5px 0px;"
        id="location"
      >Découvrez les fermes sur tout le territoire</h2>
      <MapBlock />

      <!-- Stats -->
      <div
        style="margin: 30px -16px 0 -16px;padding: 16px;border-radius: 5px; background:white; border-radius: 5px;"
      >
        <h2
          class="title pa-0"
          style="margin: 0px 0px 5px 0px;"
          id="stats"
        >Quelques chiffres...</h2>
        <StatsCards />
      </div>

      <!-- About us cards -->
      <h2
        class="title pa-0"
        style="margin: 20px 0px 5px 0px;"
        id="about"
      >REX Agri, qu'est-ce que c'est ?</h2>
      <AboutUsCards />

      <!-- Contribution proposal -->
      <div style="margin: 20px 0 0px 15px;">
        Vous souhaitez partager votre expérience ?
        <v-btn
          @click="onShareXPClick"
          outlined
          color="primary"
          class="text-none primary--text"
          style="margin-left: 10px; margin-top: -2px;"
        >Partager une expérience</v-btn>
      </div>
    </v-container>
  </div>
</template>

<script>
import Vue from "vue"
import Constants from "@/constants"
import ExperimentFilter from "@/components/ExperimentFilter.vue"
import ContributionOverlay from "@/components/ContributionOverlay.vue"
import AboutUsCards from "@/components/AboutUsCards.vue"
import StatsCards from "@/components/StatsCards.vue"
import MapBlock from "@/components/MapBlock.vue"
import MailChimpForm from "@/components/MailChimpForm.vue"

export default {
  name: "Landing",
  metaInfo() {
    return {
      title:
        "Plateforme de l’agroécologie - Retours d’Expériences d’Agriculteurs",
      meta: [
        {
          description:
            "REX-Agri : apprenez grâce aux retours d’expérience sur les techniques régénératrices. Partagez les vôtres. Entrez en contact avec des agriculteurs partout en France.",
        },
      ],
    }
  },
  components: {
    ExperimentFilter,
    ContributionOverlay,
    AboutUsCards,
    StatsCards,
    MapBlock,
    MailChimpForm
  },
  data() {
    return {
      showContributionOverlay: false,
      experimentsFetched: false
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
  methods: {
    onShareXPClick() {
      window.sendTrackingEvent("Header", "shareXP", "Partager une expérience")
      if (this.loggedUser && this.loggedUser.farmer_id)
        this.$router.push({ name: "ExperimentEditor" })
      else if (this.loggedUser)
        window.alert("Vous n'avez pas un profil agriculteur sur notre site")
      else this.showContributionOverlay = true
    },
  },
  mounted() {
    const experimentBriefs = this.$store.state.experimentBriefs
    if (experimentBriefs && experimentBriefs.length > 0) {
      this.experimentsFetched = true
      return
    }

    this.$store.commit('SET_EXPERIMENT_BRIEFS_LOADING', Constants.LoadingStatus.LOADING)
    Vue.http.get('/api/v1/experimentBriefs').then(response => {
      const body = response.body
      this.$store.commit('SET_EXPERIMENT_BRIEFS', body)
      this.$store.commit('SET_EXPERIMENT_BRIEFS_LOADING', Constants.LoadingStatus.SUCCESS)
      this.experimentsFetched = true
    }).catch(() => {
      this.$store.commit('SET_EXPERIMENT_BRIEFS_LOADING', Constants.LoadingStatus.ERROR)
      this.experimentsFetched = false
    })
  }
}
</script>

<style scoped>
.leaflet-container {
  background: #f5f5f5;
  border-radius: 5px;
}
#landing-image {
  background: #fff;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  padding-bottom: 10px;
}
</style>
