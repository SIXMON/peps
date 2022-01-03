<template>
  <div>
    <ContributionOverlay
      :visible="showContributionOverlay"
      @done="showContributionOverlay = false"
    />
    <div style="position: absolute; width:100%;">
      <v-app-bar app absolute white>
        <v-toolbar-title>
          <a
            href="https://agroecologie.org/"
          ><img src="/static/logo-padv.svg" id="logo" alt="logo pour une agriculture du vivant"></a>


        </v-toolbar-title>

        <template>
          <v-tabs align-with-title>
            <v-tab> <a href="https://agroecologie.org/indice-de-regeneration">Mesurez votre IR</a></v-tab>
            <v-tab><a href="https://agroecologie.org/reseau">Le réseau</a></v-tab>
            <v-tab><a href="https://agroecologie.org/pole-connaissances">Pôle de connaissances</a></v-tab>
            <v-tab><a href="https://agroecologie.org/adhesion#target">Rejoindre le mouvement</a></v-tab>
          </v-tabs>
         </template>


        <v-badge
          bottom
          left
          v-if="blacklist && blacklist.length > 0"
          color="accent"
          :overlap="true"
          class="align-self-center"
        >
          <template v-slot:badge>
            <span>{{ blacklist.length }}</span>
          </template>
          <v-btn icon outlined @click="blacklistDialog = true">
            <v-icon>mdi-cancel</v-icon>
          </v-btn>
        </v-badge>



        <v-btn color="primary" outlined @click="onShareXPClick">
          <v-icon color="white" class="d-flex d-sm-none">mdi-beaker-plus-outline</v-icon>
          <span
            class="caption text-none d-none d-sm-flex"
          >Partager une expérience</span>
        </v-btn>

        <v-btn text elevation="0" v-if="!loggedUser" href="/login">
          <v-icon class="d-flex d-sm-none">mdi-account</v-icon>
          <span class="caption text-none d-none d-sm-flex btn-white">S'identifier</span>
        </v-btn>

        <v-menu v-if="loggedUser" left bottom>
          <template v-slot:activator="{ on }">
            <v-btn style="margin-left: 10px; margin-right: 0px;" icon v-on="on">

              <v-badge dot color="amber" :value="profilePending || hasUnreadMessages">
                <v-avatar size="40" v-if="profileImage">
                  <v-img :src="profileImage"></v-img>
                </v-avatar>
                <v-icon v-else>mdi-account</v-icon>
              </v-badge>

            </v-btn>
          </template>

          <AccountList />
        </v-menu>
      </v-app-bar>
      <v-overlay :value="blacklistDialog" :dark="false">
        <v-btn
          @click="blacklistDialog = false"
          class="close-overlay"
          fab
          dark
          small
          color="grey lighten-5"
        >
          <v-icon color="red darken-3">mdi-close</v-icon>
        </v-btn>
        <Blacklist style="max-height: 80vh;" class="overflow-y-auto"></Blacklist>
      </v-overlay>
    </div>
  </div>
</template>

<script>
import Blacklist from "@/components/Blacklist.vue"
import AccountList from "@/components/AccountList.vue"
import ContributionOverlay from "@/components/ContributionOverlay.vue"

export default {
  name: "Header",
  components: { Blacklist, AccountList, ContributionOverlay },
  data: () => {
    return {
      blacklistDialog: false,
      showContributionOverlay: false
    }
  },
  computed: {
    blacklist() {
      return this.$store.state.blacklist
    },
    loggedUser() {
      return this.$store.state.loggedUser
    },
    farmer() {
      if (!this.loggedUser || !this.loggedUser.farmer_id) return null
      return this.$store.getters.farmerWithId(this.loggedUser.farmer_id)
    },
    profileImage() {
      if (!this.farmer) return null
      return this.farmer.profile_image
    },
    profilePending() {
      return this.farmer && !this.farmer.approved
    },
    hasUnreadMessages() {
      return this.$store.getters.hasUnreadMessages
    }
  },
  methods: {
    onShareXPClick() {
      window.sendTrackingEvent("Header", "shareXP", "Partager une expérience")
      if (this.loggedUser && this.loggedUser.farmer_id)
        this.$router.push({ name: "ExperimentEditor" })
      else if (this.loggedUser)
        window.alert("Vous n'avez pas un profil agriculteur sur notre site")
      else this.showContributionOverlay = true
    }
  },
  watch: {
    blacklist() {
      this.blacklistDialog = false
    }
  }
}
</script>

<style lang="scss">

  v-app-bar {
    .v-sheet.v-app-bar.v-toolbar:not(.v-sheet--outlined) {
     box-shadow: none !important; 
}
  .v-sheet .theme--light .v-toolbar .v-toolbar--absolute .v-app-bar {
    height: 70px !important;
    }
  }

  #logo {
    /*color:white; 
    text-decoration:none;
    font-weight: bold;
    outline: none;*/
    width: 50px;
    margin-top: 8px;
  }


  .v-toolbar__content {
    margin: 0 20px !important;
    .v-toolbar__title {
      width: 67px !important;
    }
    .v-tab {
        margin-right: 20px !important;
        &:hover {
          background-color: transparent !important;
        }
      a {
        text-decoration: none !important;
        color: #4b565e !important;
        font-weight: bold !important;
        text-transform: initial !important;
        font-family: 'DM Sans',sans-serif !important;
        letter-spacing: 0ch !important;
        font-size: 15px !important;
        &:hover {
          color: #ea5403 !important;
          &::after {
          content: "";
          display: block;
          position: absolute;
          bottom: 0;
          width: 86%;
          height: 4px;
          border-radius: 20px;
          background-color: #ea5403;
        }
        }

      }
    }
  }


.theme--light.v-tabs > .v-tabs-bar .v-tab:not(.v-tab--active), .theme--light.v-tabs > .v-tabs-bar .v-tab:not(.v-tab--active) > .v-icon, .theme--light.v-tabs > .v-tabs-bar .v-tab:not(.v-tab--active) > .v-btn, .theme--light.v-tabs > .v-tabs-bar .v-tab--disabled {
  color: transparent !important;
}

.v-tabs-slider-wrapper {
   display: none !important;
   height: 4px !important;
 .v-tabs-slider {
    border-radius: 20px !important ;
 }
}

.theme--light.v-tabs .v-tab--active:hover::before, .theme--light.v-tabs .v-tab--active::before {
  opacity: 0 !important;
}

@media screen and (max-width:1125px) {
  .v-tabs {
    display: none;
  }
}



</style> 