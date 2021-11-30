<template>
  <v-app>
    <div id="app-wrapper">
      <Header />
      <Loader v-if="initialCallsLoading" :loading="true" />
      <OverlayMessage
        :visible="showErrorMessage"
        ctaText="Recharger la page"
        title="Oups ! Une erreur est survenue"
        body="Veuillez réessayer plus tard"
        :ctaAction="this.reload"
        :showCloseButton="false"
      />
      <v-main
        style="
          background: rgba(108, 170, 200, 0.1)
            url('static/images/bg-footer-wave.svg') no-repeat left 0 bottom 0;
          background-size: contain;
        "
      >
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
      </v-main>
      <Footer v-if="!removeFooter" />
    </div>
  </v-app>
</template>

<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import Constants from "@/constants";
import OverlayMessage from "@/components/OverlayMessage.vue";
import Loader from "@/components/Loader.vue";

export default {
  name: "App",
  components: {
    Header,
    Footer,
    OverlayMessage,
    Loader,
  },
  data() {
    return {
      messageRequestInterval: null,
    };
  },
  mounted() {
    this.$store.dispatch("resetLoaders");
    this.$store.dispatch("fetchLoggedUser");
    this.$store.dispatch("fetchMessages");
    this.$store.dispatch("fetchStats");

    if (!this.$store.state.geojson) this.$store.dispatch("fetchGeojson");
  },
  computed: {
    showErrorMessage() {
      const error = Constants.LoadingStatus.ERROR;
      return this.$store.state.farmersLoadingStatus === error;
    },
    initialCallsLoading() {
      const loading = Constants.LoadingStatus.LOADING;
      return (
        this.$store.state.loggedUserLoadingStatus === loading ||
        this.$store.state.farmersLoadingStatus === loading
      );
    },
    removeFooter() {
      return this.$route.name === "Messages";
    },
    loggedUser() {
      return this.$store.state.loggedUser;
    },
  },
  methods: {
    reload() {
      location.reload();
    },
    createMessageInterval() {
      this.clearMessageInterval();
      this.messageRequestInterval = setInterval(
        () => this.$store.dispatch("fetchNewMessages"),
        30000
      );
    },
    clearMessageInterval() {
      if (!this.messageRequestInterval) return;
      clearInterval(this.messageRequestInterval);
      this.messageRequestInterval = null;
    },
  },
  watch: {
    loggedUser(value) {
      if (value && value.farmer_id) {
        this.createMessageInterval();
      } else {
        this.clearMessageInterval();
      }
    },
  },
};
</script>

<style lang="scss">
$source-sans-pro: "DM Sans", sans-serif;

#app.v-application {
  font-family: "DM Sans", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;

  .display-1,
  .display-2,
  .display-3,
  .display-4,
  .headline,
  .subtitle-1,
  .subtitle-2,
  .title {
    font-family: $source-sans-pro !important;
  }

  .display-1,
  .subtitle-2,
  .title {
    font-weight: bold !important;
  }

  .display-1 {
    color: #ea5403;
    margin-top: 20px;
  }

  .subtitle-2 {
    font-size: 18px !important;
  }
}

body {
  width: 100%;
  background: url("/static/images/bg-blob.svg") no-repeat left 0 top 13px,
    url("/static/images/bg-double-blob.svg") no-repeat right 0 top 25px;
  background-color: 0% 0% / contain rgba(108, 170, 200, 0.1);
}

body .buorg {
  border-bottom: 1px solid #ea5403;
  background-color: #ea5403;
  font-family: "DM Sans", sans-serif;
  color: white;
}

body .buorg .buorg-buttons {
  margin-top: 15px;
  margin-bottom: 15px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease-out;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.v-card__text,
.v-card__title {
  word-break: normal !important;
}

.theme--light.v-application {
  background: transparent !important;
}

.constrained {
  max-width: 1000px;
}

// https://github.com/Leaflet/Leaflet/issues/4686
.leaflet-fade-anim .leaflet-tile,
.leaflet-zoom-anim .leaflet-zoom-animated {
  will-change: auto !important;
}

.v-overlay {
  z-index: 99999 !important;
}

.close-overlay {
  position: absolute;
  right: -10px;
  top: -20px;
  z-index: 99999;
}

.field {
  margin-bottom: 30px;
}
.field-helper {
  margin-bottom: 5px;
  font-family: "Roboto", sans-serif;
  font-weight: normal;
  font-size: 0.9em;
  color: #888;
}
.parent-field {
  margin-bottom: 10px;
}
.child-field {
  padding-left: 30px;
  margin-bottom: 10px;
}
.child-field:last-of-type {
  margin-bottom: 30px;
}
.field .mandatory {
  color: #d74c4c;
  text-transform: uppercase;
  font-size: 0.6em;
  letter-spacing: 2px;
}

// Navbar

.v-sheet.v-app-bar.v-toolbar:not(.v-sheet--outlined) {
  box-shadow: none !important;
  background: white !important;
}

.theme--light.v-chip:not(.v-chip--active) {
  background: #a7ccde !important;
}

// Breadcrumbs
.theme--dark.v-icon {
  color: #4b565e !important ;
}

.theme--dark.v-breadcrumbs .v-breadcrumbs__divider,
.theme--dark.v-breadcrumbs .v-breadcrumbs__item--disabled {
  color: rgba(75, 86, 94, 0.5) !important;
}

// Button

.v-btn:not(.v-btn--round).v-size--default {
  line-height: 2;
  font-weight: 400;
  white-space: nowrap;
  text-align: center;
  box-shadow: 0 3px 8px rgb(234 84 3 / 25%);
  cursor: pointer;
  touch-action: manipulation;
  height: 40px;
  padding: 4px 15px;
  font-size: 14px;
  border-radius: 999px;
  color: #fff !important;
  background: #ea5403;
  border: 1px solid #d9d9d9;
  text-decoration: none;
  text-transform: unset;
}

.mdi-beaker-plus-outline::before {
  content: "\F1230";
  color: white;
}
</style>
