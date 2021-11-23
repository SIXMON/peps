<template>
  <v-footer class="footer">
    <p>agroecologie.org</p>
    <ul>
      <li>
        <a href="https://transition.agricultureduvivant.org/mentions-legales"
          >Mentions légales et conditions générales d'utilisation</a
        >
      </li>
      <li>
        <a href="https://transition.agricultureduvivant.org/politique-confidentialite"
          >Politique de confidentialité et de cookies</a
        >
      </li>
    </ul>
  </v-footer>
</template>



<script>
export default {
  name: "Footer",
  computed: {
    listPadding() {
      if (this.$vuetify.breakpoint.name === "xs") {
        return "10px";
      }
      return "10px 0 0 0";
    },
    imageMaxHeight() {
      if (this.$vuetify.breakpoint.name === "xs") {
        return "120px";
      }
      return undefined;
    },
    minAgriPadding() {
      if (this.$vuetify.breakpoint.name === "xs") {
        return "12px";
      }
      return "12px 0px 12px 12px";
    },
    minEcoPadding() {
      if (this.$vuetify.breakpoint.name === "xs") {
        return "12px 12px 12px 0";
      }
      return "12px";
    },
  },
};
</script> 

<style scoped>
.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  background-color: white;
  padding: 24px 50px;
  font-size: 14px;
}

p {
  color: #ea5403;
  font-weight: 600;
  margin: 0;
}

ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  margin-left: 40px;
  list-style: none;
}

 li > a {
  color: #4b565e;
  text-decoration: none;
}

a:hover {
  color: #ea5403;
}

.theme--light.v-footer {
  background-color: #fff;
}
</style>