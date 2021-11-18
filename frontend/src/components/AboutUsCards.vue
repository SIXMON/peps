<template>
  <v-row>
    <v-col v-for="item in items" :key="item.title" cols="12" sm="6" md="4">
      <v-card elevation="0" class="secondary--text">
        <v-img height="180px" contain :src="item.imageSource" />
        <v-card-title class="title">{{item.title}}</v-card-title>
        <v-card-subtitle>{{item.text}}</v-card-subtitle>
        <v-card-actions>
          <v-btn
            :to="item.ctaTo"
            :href="item.ctaLink"
            :target="item.ctaLink ? '_blank' : undefined"
            text
          >{{item.ctaText}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "AboutUsCards",
  data() {
    return {
      items: [
        {
          imageSource: "/static/images/aidants.jpg",
          title: "Un service pour la transition agroécologique",
          text:
            "C’est un service gratuit qui s'adresse à tous pour accélérer la transition agroécologique des fermes par le partage d’expériences entre agriculteurs. Ce projet est soutenu par le Ministère de l'Agriculture et de l'Alimentation et le Ministère de la Transition Ecologique dans le cadre du plan Ecophyto",
        },
        {
          imageSource: "/static/images/agriculteurs_tracteur.jpg",
          title: "Sur le terrain !",
          text:
            "Des retours d'expérience ciblés pour répondre à des problématiques techniques et vous permettre de progresser dans votre démarche agroécologique",
          ctaText: "Nous contacter",
          ctaTo: { name: "Contact" },
          ctaLink: null,
        },
        {
          imageSource: "/static/images/agriculteurs_echange.jpg",
          title: "Pour une Agriculture du Vivant",
          text:
            "Devenez acteur de la transition agroécologique et connectez-vous avec les acteurs de la transition en rejoignant le mouvement",
          ctaText: "Qui sommes nous ?",
          ctaTo: { name: "QuiSommesNous" },
          ctaLink: null,
        },
      ],
    }
  },
}
</script>

<style scoped>
 
 .title {
   margin-bottom: 20px;
 }
</style>