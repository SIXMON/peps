import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store/index'
import FormsContainer from '@/views/FormsContainer.vue'
import Results from '@/views/Results.vue'
import PolitiqueConfidentialite from '@/views/PolitiqueConfidentialite.vue'
import Landing from '@/views/Landing.vue'
import Category from '@/views/Category.vue'
import Practice from '@/views/Practice.vue'
import About from '@/views/About.vue'
import Contact from '@/views/Contact.vue'
import Map from '@/views/Map.vue'
import Farmer from '@/views/Farmer.vue'
import Experiment from '@/views/Experiment.vue'
import Contribution from '@/views/Contribution.vue'
import Profile from '@/views/Profile.vue'
import ExperimentEditor from '@/views/ExperimentEditor.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Landing,
    name: 'Landing',
  },
  {
    path: '/resultats',
    name: 'Results',
    component: Results,
  },
  {
    path: '/formulaire',
    name: 'FormsContainer',
    component: FormsContainer,
  },
  {
    path: '/contribution',
    name: 'Contribution',
    component: Contribution,
  },
  {
    path: '/categorie/:categoryTitle',
    name: 'Category',
    component: Category,
    props: (route) => ({
      category: store.state.categories.find(x => x.title === route.params.categoryTitle)
    }),
    beforeEnter: (route, _, next) => {
      if (!store.state.categories.find(x => x.title === route.params.categoryTitle))
        next({ name: 'Landing' })
      else
        next()
    }
  },
  {
    path: '/pratique/:practiceShortTitle',
    name: 'Practice',
    component: Practice,
    props: (route) => ({
      practice: store.getters.practiceWithShortTitle(route.params.practiceShortTitle)
    }),
    beforeEnter: (route, _, next) => {
      if (!store.getters.practiceWithShortTitle(route.params.practiceShortTitle))
        next({ name: 'Landing' })
      else
        next()
    }
  },
  {
    path: '/agriculteur/:farmerName',
    name: 'Farmer',
    component: Farmer,
    props: (route) => ({
      farmerName: route.params.farmerName
    }),
  },
  {
    path: '/agriculteur/:farmerName/experimentation/:expName',
    name: 'Experiment',
    component: Experiment,
    props: (route) => {
      return {
        farmerName: route.params.farmerName,
        experimentName: route.params.expName
      }
    }
  },
  {
    path: '/editeurXP/',
    name: 'ExperimentEditor',
    component: ExperimentEditor,
    props: (route) => {
      return {
        experimentName: route.query.xp
      }
    },
    beforeEnter: (route, _, next) => {
      console.log(store.state.loggedUser)
      // This view is not accessible to unlogged users
      if (!store.state.loggedUser) {
        next({ name: 'Landing' })

      // This view is always accessible to superusers
      } else if (store.state.loggedUser.is_superuser) {
        next()

      // This view is not accessible to users without a farmer profile
      } else if (!store.state.loggedUser.farmer_external_id) {
        next({ name: 'Landing' })

      // If we are creating a new XP, we an access the view
      } else if (!route.query.xp){
        next()

      // If we are editing an existing XP, it must belong to the logged farmer
      } else {
        const farmer = store.getters.farmerWithExternalId(
          store.state.loggedUser.farmer_external_id
        )
        if (farmer.experiments.find(x => x.name === route.query.xp)) {
          next()
        } else {
          next({ name: 'Landing' })
        }
      }
    }
  },
  {
    path: '/politique-de-confidentialite',
    name: 'PolitiqueConfidentialite',
    component: PolitiqueConfidentialite,
  },
  {
    path: '/qui-sommes-nous',
    name: 'QuiSommesNous',
    component: About,
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact,
  },
  {
    path: '/pratiques',
    name: 'Practices',
    component: Landing,
  },
  {
    path: '/map',
    component: Map,
    name: 'Map',
  },
  {
    path: '/compte',
    component: Profile,
    name: 'Profile',
  },
  {
    path: '*',
    redirect: {
      name: 'Landing'
    },
  },
]

const router = new VueRouter({
  routes,
  previousRoute: null,
  scrollBehavior() {
    return new Promise((resolve) => {
      const fadeTransitionTime = 250
      setTimeout(() => {
        resolve({ x: 0, y: 0 })
      }, fadeTransitionTime / 2)
    })
  }
})
router.beforeEach((to, from, next) => {
  router.previousRoute = from
  next()
})
router.afterEach((route, previousRoute) => {
  window.sendPageView ? window.sendPageView(route, previousRoute) : undefined
})

export default router
