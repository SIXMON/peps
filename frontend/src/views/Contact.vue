<template>
  <div>
    <Loader v-if="loading" :title="loadingTitle" :loading="loading" />
    <OverlayMessage 
      :visible="showErrorMessage"
      ctaText="Recharger la page"
      title="Oups ! Une erreur est survenue"
      @done="closeErrorMessage()"
    />
    <OverlayMessage
      :visible="showSuccessMessage"
      ctaText="D'accord"
      title="Message envoyé !"
      @done="closeSuccessMessage()"
    />
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <div class="title">Si vous souhaitez en savoir plus</div>
      <div class="body-2">Laissez nous vos coordonnées, nous vous recontacterons sous peu.</div>

      <div style="max-width: 500px; margin: 15px 0 15px 0;">
        <div style="display: flex;">
          <v-text-field prepend-inner-icon="mdi-account" style="margin-right: 10px" v-model="name" label="Nom"></v-text-field>
          <v-text-field prepend-inner-icon="mdi-email" v-model="email" label="Adresse e-mail"></v-text-field>
        </div>
        <v-textarea
          prepend-inner-icon="mdi-message"
          v-model="message"
          label="Message"
        ></v-textarea>
      </div>
      <v-btn
        class="text-none"
        style="margin-bottom: 15px;"
        @click="sendContactData()"
        color="primary"
        dark
      >Contactez-moi !</v-btn>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import Loader from "@/components/Loader.vue"
import OverlayMessage from "@/components/OverlayMessage.vue"
import Constants from "@/constants"

export default {
  name: "Contact",
  components: { Title, Loader, OverlayMessage },
  metaInfo() {
    return {
      title: "Pour une Agriculture du Vivant - Questions ou suggestions, contactez nous",
      meta: [{ description: 'Si vous souhaitez en savoir plus sur la démarche ou le produit, laissez nous vos coordonnées, nous vous contacterons dans les plus bref délais' }]
    }
  },
  data() {
    return {
      title: "Nous contacter",
      name: '',
      email: '',
      message: '',
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" }
        },
        {
          text: "Contact",
          disabled: true
        }
      ],
      loadingTitle: "Nous envoyons votre information...",
    }
  },
  computed: {
    loading() {
      return (
        this.$store.state.contactLoadingStatus ===
        Constants.LoadingStatus.LOADING
      )
    },
    showErrorMessage() {
      return (
        this.$store.state.contactLoadingStatus ===
        Constants.LoadingStatus.ERROR
      )
    },
    showSuccessMessage() {
      return (
        this.$store.state.contactLoadingStatus ===
        Constants.LoadingStatus.SUCCESS
      )
    },
    loggedUser() {
      return this.$store.state.loggedUser
    }
  },
  methods: {
    sendContactData() {
      this.$store.dispatch("sendContactMessage", {
        name: this.name,
        email: this.email,
        message: this.message
      })
    },
    closeErrorMessage() {
      this.$store.dispatch("resetContactLoadingStatus")
    },
    closeSuccessMessage() {
      this.$store.dispatch("resetContactLoadingStatus")
    },
    getInitialName() {
      if (this.loggedUser && this.loggedUser.farmer_id)
        return this.$store.getters.farmerWithId(this.loggedUser.farmer_id).name
      if (this.$store.state.lastContactInfo && this.$store.state.lastContactInfo.name)
        return this.$store.state.lastContactInfo.name
      return null
    },
    getInitialEmail() {
      if (this.loggedUser)
        return this.loggedUser.email
      if (this.$store.state.lastContactInfo && this.$store.state.lastContactInfo.email)
        return this.$store.state.lastContactInfo.email
      return null
    }
  },
  mounted() {
    this.name = this.getInitialName()
    this.email = this.getInitialEmail()
  }
}
</script>

<style scoped>
.title {
  margin-top: 20px;
  margin-bottom: 5px;
}
.body-2 {
  line-height: 1.375rem;
}
</style>
