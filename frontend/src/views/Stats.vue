<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <iframe
          src="https://peps-metabase.cleverapps.io/public/dashboard/2b2701c3-70ea-4851-9f9e-a8771bffecdf"
          style="border: 1px solid rgb(204, 204, 204);box-shadow: 3px 3px 7px -3px #999;"
          width="100%"
          height="1100"
          allowtransparency
      ></iframe>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"

export default {
  name: "Stats",
  components: { Title },
  metaInfo() {
    return {
      title: "Pour une Agriculture du Vivant - Statistiques",
      meta: [{ description: 'Les statistiques de Pour une Agriculture du Vivant' }]
    }
  },
  data() {
    return {
      title: "Statistiques",
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" }
        },
        {
          text: "Statistiques",
          disabled: true
        }
      ],
    }
  }
}
</script>
