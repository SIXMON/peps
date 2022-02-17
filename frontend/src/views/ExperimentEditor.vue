<template>
  <div id="xp-edit">
    <Loader v-if="updateInProgress" title="Juste un instant..." :loading="updateInProgress" />
    <Title :breadcrumbs="breadcrumbs" />

    <v-container class="constrained">
      <v-sheet
        rounded
        class="pa-2 caption"
        v-if="bannerText"
        color="blue-grey lighten-5"
      >{{bannerText}}</v-sheet>
      <v-app-bar
        style="margin-left: auto; margin-right: auto;"
        max-width="1000"
        color="white"
        :elevation="toolbarOnTop ? 2 : 0"
        :fixed="toolbarOnTop"
        id="button-toolbar"
      >
        <v-toolbar-title style="flex-flow: wrap;" class="primary--text"></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn
          :small="$vuetify.breakpoint.name === 'xs'"
          style="margin-right: 10px;"
          @click="cancelEdit"
          class="text-none"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-arrow-left</v-icon>
          <span v-if="$vuetify.breakpoint.name !== 'xs'">Annuler</span>
        </v-btn>

        <v-btn
          class="text-none"
          :small="$vuetify.breakpoint.name === 'xs'"
          v-if="dummyExperiment.state === 'Brouillon'"
          @click="updateDraftExperiment(false)"
          style="margin-right: 10px;"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-content-save</v-icon>
          <span v-if="$vuetify.breakpoint.name === 'xs'">Sauvegarder</span>
          <span v-else>Sauvegarder le brouillon</span>
        </v-btn>

        <v-btn
          class="text-none"
          :small="$vuetify.breakpoint.name === 'xs'"
          v-if="dummyExperiment.state === 'Brouillon'"
          color="primary"
          @click="submitExperiment(true)"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-check-decagram</v-icon>Valider
        </v-btn>

        <v-btn
          class="text-none"
          :small="$vuetify.breakpoint.name === 'xs'"
          color="primary"
          v-if="dummyExperiment.state !== 'Brouillon'"
          @click="updateExperiment(false)"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-content-save</v-icon>Sauvegarder
        </v-btn>
      </v-app-bar>

      <v-form ref="form" v-model="formIsValid">
        <!-- NAME -->
        <div class="field">
          <div class="field-title title">
            Titre de l'expérience
            <span class="mandatory">- obligatoire</span>
          </div>
          <div class="field-helper">Court et explicite, il doit donner l'idée générale</div>
          <v-text-field
            hide-details="auto"
            :rules="[validators.notEmpty, validators.maxCharsXPName]"
            @input="hasChanged = true"
            outlined
            dense
            counter
            maxlength="70"
            v-model="dummyExperiment.name"
          ></v-text-field>
        </div>

        <!-- RESULTS -->
        <div class="field">
          <div class="field-title title">
            Votre expérience est : 
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-radio-group
            :rules="[validators.notEmpty]"
            @change="hasChanged = true"
            v-model="dummyExperiment.results"
            :mandatory="false"
          >
            <v-radio
              label="Maîtrisée & intégrée en routine à l'exploitation"
              value="Maîtrisée & intégrée en routine à l'exploitation"
            ></v-radio>
            <v-radio
              label="Prometteuse & en cours d'amélioration pour être maîtrisée"
              value="Prometteuse & en cours d'amélioration pour être maîtrisée"
            ></v-radio>
            <v-radio
              label="Un premier essai, à renouveler pour mieux juger de son potentiel"
              value="Un premier essai, à renouveler pour mieux juger de son potentiel"
            ></v-radio>
            <v-radio
              label="Abandonnée car non satisfaisante"
              value="Abandonnée car non satisfaisante"
            ></v-radio>
          </v-radio-group>
        </div>

        <!-- WORKSHOP -->
        <div class="field">
          <div class="field-title title">
            Quel atelier de production est concerné par cette expérience ? 
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-radio-group
            @change="hasChanged = true"
            v-model="dummyExperiment.workshop"
            :mandatory="false"
            :rules="[validators.notEmpty]"
          >
            <v-radio
              label="Grandes cultures"
              value="Grandes cultures"
            ></v-radio>
            <v-radio 
              label="Cultures d'industries" 
              value="Cultures d'industries"
            ></v-radio>
            <v-radio
              label="Légumes de plein champs"
              value="Légumes de plein champs"
            ></v-radio>
            <v-radio 
              label="Élevage ruminant" 
              value="Élevage ruminant"
            ></v-radio>
            <v-radio 
              label="Élevage monogastrique" 
              value="Élevage monogastrique"
            ></v-radio>
            <v-radio 
              label="Arboriculture" 
              value="Arboriculture"
            ></v-radio>
            <v-radio 
              label="Viticulture" 
              value="Viticulture"
            ></v-radio>
            <v-radio 
              label="Maraîchage diversifié" 
              value="Maraîchage diversifié"
            ></v-radio>
            <v-radio 
              label="Apiculture" 
              value="Apiculture"
            ></v-radio>
            <v-radio 
              label="PPAM" 
              value="PPAM"
            ></v-radio>
            <v-radio 
              label="Cultures spécialisées" 
              value="Cultures spécialisées"
            ></v-radio>
          </v-radio-group>
        </div>

        <!-- CULTURES -->
        <div class="field">
          <div class="field-title title">Quelles sont les principales cultures concernées par l'expérience ?</div>
          <div
            class="field-helper"
          >Elles permettent de catégoriser par cultures les retours d'expérience</div>
          <v-autocomplete
            @input="hasChanged = true"
            v-model="dummyExperiment.cultures"
            :items="cultures"
            outlined
            chips
            multiple
            deletable-chips
            small-chips
            hide-details="auto"
            dense
          ></v-autocomplete>
        </div>

        <!-- TAGS -->
        <div class="field">
          <div
            class="field-title title"
          >A quelles thématiques cette expérience est-elle rattachée ?</div>
          <div
            class="field-helper"
          >Sélectionnez 3 thématiques maximum
          <br />Elles permettent de catégoriser par thèmes les retours d'expérience</div>
          <v-radio-group
            v-model="dummyExperiment.tags"
            :rules="[validators.maxSelected(3)]"
            hide-details="auto"
            style="margin-top: 5px; margin-bottom: 5px;"
          ></v-radio-group>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Maladies"
            value="Maladies"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Insectes et ravageurs"
            value="Insectes et ravageurs"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Adventices"
            value="Adventices"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Environnement & biodiversité"
            value="Environnement & biodiversité"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Diversification"
            value="Diversification"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Autonomie"
            value="Autonomie"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Productivité"
            value="Productivité"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Organisation du travail"
            value="Organisation du travail"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Réduction des charges"
            value="Réduction des charges"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox 
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Équipement et outils"
            value="Équipement et outils"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Autre"
            value="Autre"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
        </div>

        <!-- OBJECTIVES -->
        <div class="field">
          <div class="field-title title">
            Quels sont les objectifs spécifiques de l’essai/de la pratique ? 
            <span
              class="mandatory"
            >- obligatoire</span>
          </div>
          <div
            class="field-helper"
          >Par exemple : Améliorer la gestion du vulpin sur des parcelles de blé, augmenter la production fourragère utile, diversifier les sources de revenus.</div>
          <v-textarea
            hide-details="auto"
            :rules="[validators.notEmpty]"
            rows="4"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.objectives"
          ></v-textarea>
        </div>

        <!-- SURFACE TYPE -->
        <div class="field">
          <div class="field-title title">
            Sur quelle surface porte l'expérience ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Toutes les surfaces potentiellement adaptées à la mise en place de la pratique"
            value="Toutes les surfaces potentiellement adaptées à la mise en place de la pratique"
            hide-details
            :rules="[hasSurfaceType,validators.maxSelected(1)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Plusieurs parcelles"
            value="Plusieurs parcelles"
            hide-details
            :rules="[hasSurfaceType,validators.maxSelected(1)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Une parcelle"
            value="Une parcelle"
            hide-details
            :rules="[hasSurfaceType,validators.maxSelected(1)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Une bande"
            value="Une bande"
            hide-details
            :rules="[hasSurfaceType,validators.maxSelected(1)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Des micro-parcelles"
            value="Des micro-parcelles"
            :rules="[hasSurfaceType,validators.maxSelected(1)]"
          ></v-checkbox>
        </div>

        <!-- SURFACE -->
        <div class="field">
          <div class="field-title title">Combien d’hectares cela représente au total ? </div>
          <div>
            <v-text-field
              hide-details="auto"
              @change="hasChanged = true"
              rows="1"
              auto-grow
              outlined
              dense
              v-model="dummyExperiment.surface"
              suffix="hectare(s)"
            ></v-text-field>
          </div>
        </div>

        <!-- EQUIPMENT -->
        <div class="field">
          <div
            class="field-title title"
          >Quel matériel utilisez-vous pour mener cette expérience ?</div>
          <div class="field-helper">ex : type d’outil, équipements spécifiques, type de dents, réglages spécifiques, etc...</div>
          <v-textarea
            hide-details="auto"
            rows="1"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.equipment"
          ></v-textarea>
        </div>

        <!-- INVESTMENT -->
        <div class="field">
          <div
            class="field-title title"
          >Quels investissements l'expérience a requis ? </div>
          <!-- <div class="field-helper">En temps, en argent, en machines...</div> -->
          <v-textarea
            hide-details="auto"
            rows="1"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.investment"
          ></v-textarea>
        </div>

        <!-- DESCRIPTION -->
        <div class="field">
          <div class="field-title title">
            Description de l'expérience
            <span class="mandatory">- obligatoire</span>
          </div>
          <div
            class="field-helper"
          >
            Veuillez décrire ci-dessous votre expérience de manière à faire ressortir les points clés (techniques, socio-économiques) et la manière dont elle s'intègre dans votre démarche. <br />
            <br />
            Ci-dessous, quelques exemples d'informations recherchées : <br />
            <ul>
              <li>Contexte spécifique et le niveau d'avancement dans la transition agroécologique</li>
              <li>Dates, densités et conditions de semis</li>
              <li>Type de travail du sol</li>
              <li>Observations sur : structure du sol (compact, souple, porosités, galeries, etc...), le type de sol, les conditions de sol (sec, humide, etc...), le développement des plantes,...</li>
              <li>Mise en place de témoin (si oui, veuillez indiquer les différences observées entre les témoins)</li>
              <li>Conseils clés</li>
            </ul>
          </div>
          <v-textarea
            hide-details="auto"
            :rules="[validators.notEmpty]"
            rows="4"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.description"
          ></v-textarea>
        </div>

        <!-- RESULTS DETAILS -->
        <div class="field">
          <div class="field-title title">
            Commentaires des résultats au regard des objectifs visés
            <span class="mandatory">- obligatoire</span>
          </div>
          <div
            class="field-helper"
          >Avec du recul, veuillez commenter les résultats de l'expérience au regard de vos objectifs. <br />
            <br />
            Ci-dessous, quelques exemples d'informations recherchées : 
            <ul>
              <li>Facteurs de réussite/d’échec liés aux conditions de mise en œuvre de l'expérience</li>
              <li>Commentaires face aux rendements obtenus</li>
              <li>Ressenti</li>
              <li>Difficultés rencontrées et pistes d'amélioration</li>
              <li>Perspectives : poursuite/arrêt de l’expérience</li>
            </ul>
          </div>
          <v-textarea
            hide-details="auto"
            rows="4"
            :rules="[validators.notEmpty]"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.results_details"
          ></v-textarea>
        </div>

        <!-- PADV_PROJECT -->
        <div class="field">
          <div class="field-title title">Si cette expérience a été menée dans le cadre d'un projet accompagné par Pour une Agriculture du Vivant, veuillez le sélectionner : </div>
          <v-select
            :items="padv_projects"
            outlined
            dense
            v-model="dummyExperiment.padv_projects"
          >
          </v-select>
        </div>

        <!-- IR_SCORE -->
        <div class="field">
          <div class="field-title title">Si vous avez réalisé un diagnostic de votre ferme avec l'Indice de Régénération, veuillez indiquer le score obtenu : </div>
          <v-text-field
            type="number"
            outlined
            dense
            max="100"
            min="0"
            suffix="/ 100"
            v-model="dummyExperiment.ir_score" />
        </div>

        <!-- LINKS -->
        <div class="field">
          <div class="field-title title">Liens</div>
          <div
            class="field-helper"
            style="margin-bottom: 10px;"
          >Si vous le souhaitez, vous pouvez ajouter des liens vers votre site, vos profils de réseaux sociaux, ou autre</div>
          <v-text-field
            hide-details="auto"
            :rules="[validators.isUrl]"
            @input="hasChanged = true"
            @blur="appendHttp(index)"
            v-for="(link, index) in dummyExperiment.links"
            :key="index"
            outlined
            dense
            placeholder="https://..."
            style="max-width: 600px;"
            v-model="dummyExperiment.links[index]"
          >
            <template v-slot:prepend>
              <v-btn fab x-small style="margin-top: -3px;" @click="deleteLink(index)">
                <v-icon color="red">mdi-trash-can-outline</v-icon>
              </v-btn>
            </template>
          </v-text-field>
          <v-btn class="text-none" @click="addLink()">
            <v-icon small style="margin-right: 5px;">mdi-link-variant-plus</v-icon>Ajoutez un lien
          </v-btn>
        </div>

        <!-- IMAGES  -->
        <div class="field">
          <div class="field-title title">Images</div>
          <div class="field-helper grey--text">Vous pouvez en ajouter plusieurs</div>
          <ImagesField :imageArray.sync="dummyExperiment.images" @change="hasChanged = true" />
        </div>

        <!-- VIDEOS -->
        <div class="field">
          <div class="field-title title">Vidéos</div>
          <div class="field-helper grey--text">Vous pouvez en ajouter plusieurs</div>
          <VideosField :videoArray.sync="dummyExperiment.videos" @change="hasChanged = true" />
        </div>
      </v-form>
    </v-container>
    <v-overlay :value="updateSucceeded || updateFailed" :dark="false">
      <div>
        <v-btn @click="closeOverlay()" class="close-overlay" fab dark small color="grey lighten-5">
          <v-icon color="red darken-3">mdi-close</v-icon>
        </v-btn>
        <v-card :style="'max-width: 600px;'" class="overflow-y-auto">
          <v-card-text style="padding: 30px; color: #333;">
            <span v-if="updateSucceeded">
              <v-icon style="margin-top: -3px; margin-right: 5px;">mdi-check-circle</v-icon>
              {{successPopupText}}
            </span>
            <span v-else>
              <v-icon style="margin-top: -3px; margin-right: 5px;">mdi-emoticon-sad-outline</v-icon>Oops ! On n'a pas pu mettre à jour le retour d'expérience. Veuillez essayer plus tard.
            </span>
          </v-card-text>
          <div style="padding: 10px; text-align: right">
            <v-btn
              class="text-none body-1 practice-buttons"
              color="primary"
              @click="closeOverlay()"
              rounded
            >OK</v-btn>
          </div>
        </v-card>
      </div>
    </v-overlay>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import validators from "@/validators"
import utils from "@/utils"
import Loader from "@/components/Loader.vue"
import Constants from "@/constants"
import ImagesField from "@/components/ImagesField.vue"
import VideosField from "@/components/VideosField.vue"

export default {
  name: "ExperimentEditor",
  components: { Title, Loader, ImagesField, VideosField },
  metaInfo() {
    const title = this.experiment
      ? "Pour une Agriculture du Vivant - Modifier mon retour d'expérience"
      : "Pour une Agriculture du Vivant - Partager un retour d'expérience"
    const description = this.experiment
      ? `Mettez à jour les données du retour d'expérience ${this.experiment.name}`
      : "Remplissez ces informations et partagez un retour d'expérience sur Pour une Agriculture du Vivant"
    return {
      title: title,
      meta: [
        {
          description: description,
        },
      ],
    }
  },
  props: {
    experimentUrlComponent: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      dummyExperiment: {
        tags: [],
        surface_type: [],
        links: [],
        images: [],
        videos: [],
        state: "Brouillon",
      },
      toolbarOnTop: false,
      initialToolbarTop: 0,
      hasChanged: false,
      formIsValid: true,
      padv_projects: [
        {
          text: "Individuel",
          value: "Individuel",
        },
        {
          text: "Pachamama",
          value: "Pachamama",
        },
        {
          text: "Cultures d'Industries sur Sols Vivants (CISV)",
          value: "Cultures d'Industries sur Sols Vivants (CISV)",
        },
        {
          text: "Sol et autonomie en élevage laitier",
          value: "Sol et autonomie en élevage laitier",
        },
        {
          text: "Agrohoublon",
          value: "Agrohoublon",
        },
        {
          text: "Agrognon",
          value: "Agrognon",
        },
        {
          text: "Thèse Une seule santé blé tendre",
          value: "Thèse Une seule santé blé tendre",
        }
      ],
      cultures: [
        {
          header: "Grandes cultures / Cultures d'industries / Maraîchage",
        },
        {text: "Ail", value: "Ail"},
        {text: "Artichaut", value: "Artichaut"},
        {text: "Asperge", value: "Asperge"},
        {text: "Aubergine", value: "Aubergine"},
        {text: "Avoine hiver", value: "Avoine hiver"},
        {text: "Avoine printemps", value: "Avoine printemps"},
        {text: "Basilic", value: "Basilic"},
        {text: "Betterave fourragère", value: "Betterave fourragère"},
        {text: "Betterave rouge", value: "Betterave rouge"},
        {text: "Betterave sucrière", value: "Betterave sucrière"},
        {text: "Blé dur", value: "Blé dur"},
        {text: "Blé tendre hiver", value: "Blé tendre hiver"},
        {text: "Blé tendre printemps", value: "Blé tendre printemps"},
        {text: "Blette", value: "Blette"},
        {text: "Brocoli", value: "Brocoli"},
        {text: "Brome", value: "Brome"},
        {text: "Cameline", value: "Cameline"},
        {text: "Carotte industrielle petite", value: "Carotte industrielle petite"},
        {text: "Carotte légumière", value: "Carotte légumière"},
        {text: "Celeri Branche", value: "Celeri Branche"},
        {text: "Celeri Rave", value: "Celeri Rave"},
        {text: "Chanvre", value: "Chanvre"},
        {text: "Chanvre fibre", value: "Chanvre fibre"},
        {text: "Chicorée", value: "Chicorée"},
        {text: "Chicorée salade", value: "Chicorée salade"},
        {text: "Chou blanc", value: "Chou blanc"},
        {text: "Chou brocoli", value: "Chou brocoli"},
        {text: "Chou Bruxelles", value: "Chou Bruxelles"},
        {text: "Chou fleur", value: "Chou fleur"},
        {text: "Chou fourrager", value: "Chou fourrager"},
        {text: "Chou pommé", value: "Chou pommé"},
        {text: "Chou vert", value: "Chou vert"},
        {text: "Choux-rave", value: "Choux-rave"},
        {text: "Ciboulette", value: "Ciboulette"},
        {text: "Colza", value: "Colza"},
        {text: "Colza associé", value: "Colza associé"},
        {text: "Colza printemps", value: "Colza printemps"},
        {text: "Concombre", value: "Concombre"},
        {text: "Coriandre", value: "Coriandre"},
        {text: "Courge", value: "Courge"},
        {text: "Courgette", value: "Courgette"},
        {text: "Cultures énergétiques", value: "Cultures énergétiques"},
        {text: "Echalote", value: "Echalote"},
        {text: "Endive", value: "Endive"},
        {text: "Epeautre", value: "Epeautre"},
        {text: "Épinard", value: "Épinard"},
        {text: "Épinard colorant", value: "Épinard colorant"},
        {text: "Escourgeon", value: "Escourgeon"},
        {text: "Fenouil", value: "Fenouil"},
        {text: "Fétuque", value: "Fétuque"},
        {text: "Féverole d'hiver", value: "Féverole d'hiver"},
        {text: "Féverole de printemps", value: "Féverole de printemps"},
        {text: "Fraise (plein air)", value: "Fraise (plein air)"},
        {text: "Fraise (sous abri)", value: "Fraise (sous abri)"},
        {text: "Haricot blanc", value: "Haricot blanc"},
        {text: "Haricot Flageolet", value: "Haricot Flageolet"},
        {text: "Haricot rouge", value: "Haricot rouge"},
        {text: "Haricot vert", value: "Haricot vert"},
        {text: "Laitue", value: "Laitue"},
        {text: "Lentille", value: "Lentille"},
        {text: "Lin fibre", value: "Lin fibre"},
        {text: "Lin oléagineux", value: "Lin oléagineux"},
        {text: "Lupin", value: "Lupin"},
        {text: "Luzerne", value: "Luzerne"},
        {text: "Maïs doux", value: "Maïs doux"},
        {text: "Maïs ensilage", value: "Maïs ensilage"},
        {text: "Maïs grain", value: "Maïs grain"},
        {text: "Maïs Pop-corn", value: "Maïs Pop-corn"},
        {text: "Maïs semence", value: "Maïs semence"},
        {text: "Melon (plein air)", value: "Melon (plein air)"},
        {text: "Melon (sous abri)", value: "Melon (sous abri)"},
        {text: "Menthe", value: "Menthe"},
        {text: "Méteil dominante céréales", value: "Méteil dominante céréales"},
        {text: "Méteil dominante légumineuses", value: "Méteil dominante légumineuses"},
        {text: "Millet", value: "Millet"},
        {text: "Miscanthus", value: "Miscanthus"},
        {text: "Moha", value: "Moha"},
        {text: "Moutarde", value: "Moutarde"},
        {text: "Moutarde brune graine", value: "Moutarde brune graine"},
        {text: "Navet", value: "Navet"},
        {text: "Oeillette", value: "Oeillette"},
        {text: "Oignon", value: "Oignon"},
        {text: "Orge hiver", value: "Orge hiver"},
        {text: "Orge printemps", value: "Orge printemps"},
        {text: "Panais", value: "Panais"},
        {text: "Pastèque", value: "Pastèque"},
        {text: "Persil", value: "Persil"},
        {text: "Piment", value: "Piment"},
        {text: "Poireau", value: "Poireau"},
        {text: "Pois carré", value: "Pois carré"},
        {text: "Pois chiche", value: "Pois chiche"},
        {text: "Pois de conserve", value: "Pois de conserve"},
        {text: "Pois fourrager", value: "Pois fourrager"},
        {text: "Pois protéagineux", value: "Pois protéagineux"},
        {text: "Poivron", value: "Poivron"},
        {text: "Pomme de terre conso", value: "Pomme de terre conso"},
        {text: "Pomme de terre fécule", value: "Pomme de terre fécule"},
        {text: "Pomme de terre plant", value: "Pomme de terre plant"},
        {text: "Prairie temporaire (graminées)", value: "Prairie temporaire (graminées)"},
        {text: "Prairie temporaire (légumineuses et graminées)", value: "Prairie temporaire (légumineuses et graminées)"},
        {text: "Prairie temporaire (légumineuses)", value: "Prairie temporaire (légumineuses)"},
        {text: "Quinoa", value: "Quinoa"},
        {text: "Radis", value: "Radis"},
        {text: "Ray grass d'Italie", value: "Ray grass d'Italie"},
        {text: "Ray-grass anglais", value: "Ray-grass anglais"},
        {text: "Roquette", value: "Roquette"},
        {text: "Salade (plein air)", value: "Salade (plein air)"},
        {text: "Salade (sous abri)", value: "Salade (sous abri)"},
        {text: "Salsifi", value: "Salsifi"},
        {text: "Sarrasin", value: "Sarrasin"},
        {text: "Scorsconère", value: "Scorsconère"},
        {text: "Seigle", value: "Seigle"},
        {text: "Soja", value: "Soja"},
        {text: "Sorgho fourrager", value: "Sorgho fourrager"},
        {text: "Sorgho grain", value: "Sorgho grain"},
        {text: "Tabac", value: "Tabac"},
        {text: "Tomate (plein air)", value: "Tomate (plein air)"},
        {text: "Tomate (sous abri)", value: "Tomate (sous abri)"},
        {text: "Topinambour", value: "Topinambour"},
        {text: "Tournesol", value: "Tournesol"},
        {text: "Triticale", value: "Triticale"},
        {text: "Vesce", value: "Vesce"},
        {
          header: "Arboriculture"
        },
        {text: "Abricot", value: "Abricot"},
        {text: "Amande", value: "Amande"},
        {text: "Cassis", value: "Cassis"},
        {text: "Cerise", value: "Cerise"},
        {text: "Citron", value: "Citron"},
        {text: "Clémentine", value: "Clémentine"},
        {text: "Coing", value: "Coing"},
        {text: "Figue", value: "Figue"},
        {text: "Framboise", value: "Framboise"},
        {text: "Groseille", value: "Groseille"},
        {text: "Kiwi", value: "Kiwi"},
        {text: "Mandarine", value: "Mandarine"},
        {text: "Mûre", value: "Mûre"},
        {text: "Myrtille", value: "Myrtille"},
        {text: "Nèfle", value: "Nèfle"},
        {text: "Noisette", value: "Noisette"},
        {text: "Noix", value: "Noix"},
        {text: "Olive", value: "Olive"},
        {text: "Orange", value: "Orange"},
        {text: "Pamplemousse", value: "Pamplemousse"},
        {text: "Pêche", value: "Pêche"},
        {text: "Poire", value: "Poire"},
        {text: "Pomme", value: "Pomme"},
        {text: "Prune", value: "Prune"},
        {text: "Quetsche ", value: "Quetsche"},
        {
          header: "Viticulture"
        },
        {
          text: "Raisin de table",
          value: "Raisin de table"
        },
        {
          text: "Vigne (vignification)",
          value: "Vigne (vignification)"
        },
        {
          header: "Autre",
        },
        {
          text: "Pas de culture",
          value: "Pas de culture",
        },
        {
          text: "Toutes les cultures",
          value: "Toutes les cultures",
        },
      ],
    }
  },
  computed: {
    updateInProgress() {
      return (
        this.$store.state.experimentEditLoadingStatus ==
        Constants.LoadingStatus.LOADING
      )
    },
    updateSucceeded() {
      return (
        this.$store.state.experimentEditLoadingStatus ===
        Constants.LoadingStatus.SUCCESS
      )
    },
    updateFailed() {
      return (
        this.$store.state.experimentEditLoadingStatus ===
        Constants.LoadingStatus.ERROR
      )
    },
    successPopupText() {
      if (this.dummyExperiment.state === 'Brouillon')
        return `Le brouillon de votre retour d'expérience a bien été ${this.experimentUrlComponent ? "mis à jour" : "crée"}. Si vous avez terminé la rédaction, cliquez sur Valider pour que l'équipe Pour une Agriculture du Vivant l'examine avant sa mise en ligne`
      if (this.dummyExperiment.state === 'En attente de validation')
        return "Merci pour votre contribution ! Votre retour d'expérience va être relue par notre équipe avant sa mise en ligne. Cela nous permet de vérifier la pertinence du contenu et de corriger d'éventuelles petites fautes qui auraient échappé à votre vigilance. Nous revenons vers vous rapidement"
      return "Votre retour d'expérience a bien été mis à jour !"
    },
    bannerText() {
      if (this.dummyExperiment.state === 'Brouillon')
        return "Ce retour d'expérience est à l'état de brouillon. Quand vous avez terminé la rédaction, cliquez sur Valider pour que l'équipe Pour une Agriculture du Vivant l'examine avant sa mise en ligne."
      if (this.dummyExperiment.state === 'En attente de validation')
        return "Ce retour d'expérience est en attente de validation par notre équipe avant sa mise en ligne. Nous vérifions la pertinence du contenu et corrigeons d'éventuelles petites fautes qui auraient échappé à votre vigilance."
      return null
    },
    validators() {
      return validators
    },
    loggedFarmer() {
      const farmer = this.$store.getters.farmerWithId(
        this.$store.state.loggedUser.farmer_id
      )
      return farmer
    },
    experiment() {
      if (!this.loggedFarmer || !this.experimentUrlComponent) return undefined
      return this.$store.getters.experimentWithUrlComponent(
        this.loggedFarmer,
        this.experimentUrlComponent
      )
    },
    breadcrumbs() {
      return [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" },
        },
        {
          text: "Mon compte",
          disabled: false,
          to: { name: "Profile" },
        },
        {
          text: this.experiment ? this.experiment.name : "Nouvelle expérience",
          disabled: true,
        },
      ]
    },
    hasSurfaceType() {
      const errorMessage = "Vous devez en selectionner au moins une surface"
      if (!this.dummyExperiment || !this.dummyExperiment.surface_type)
        return errorMessage
      return this.dummyExperiment.surface_type.length > 0 || errorMessage
    },
  },
  methods: {
    validateSubmission() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        window.scrollTo(0, 0)
        window.alert("Merci de vérifier les champs en rouge et réessayer")
      }

      return this.formIsValid
    },
    updateDraftExperiment() {
      if (!this.dummyExperiment.name) {
        window.scrollTo(0, 0)
        window.alert("Merci de renseigner le nom du retour d'expérience")
        return
      }

      this.dummyExperiment.state = "Brouillon"
      this.sendUpdateRequest()
    },
    submitExperiment() {
      if (!this.validateSubmission()) return

      this.dummyExperiment.state = "En attente de validation"
      this.sendUpdateRequest()
    },
    updateExperiment() {
      if (!this.validateSubmission()) return

      this.sendUpdateRequest()
    },
    sendUpdateRequest() {
      if (this.experiment) {
        const payload = utils.getObjectDiff(
          this.experiment,
          this.dummyExperiment
        )

        this.$store.dispatch("patchExperiment", {
          experiment: this.experiment,
          changes: payload,
        })
      } else {
        this.$store.dispatch("createExperiment", {
          payload: this.dummyExperiment,
          farmer: this.loggedFarmer,
        })
        clearInterval(this.saveInterval);
        localStorage.removeItem("draft-experiment");
      }
    },
    closeOverlay() {
      const success = this.updateSucceeded
      this.$store.dispatch("resetExperimentEditLoadingStatus")
      if (success)
        this.$router.push({
          name: "Profile",
        })
    },
    cancelEdit() {
      this.$router.go(-1)
    },
    resetDummyExperiment() {
      if (this.experiment) {
        this.dummyExperiment = JSON.parse(JSON.stringify(this.experiment))
        this.dummyExperiment.images = this.dummyExperiment.images || []
        this.dummyExperiment.videos = this.dummyExperiment.videos || []
        this.dummyExperiment.links = this.dummyExperiment.links || []
        this.dummyExperiment.state = this.dummyExperiment.state || "Brouillon"
      }
    },
    addImages(e) {
      if (!e) return
      const files = e.target.files
      this.hasChanged = true

      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        utils.toBase64(file, (base64) => {
          this.dummyExperiment.images.push({
            image: base64,
            label: "",
          })
        })
      }
    },
    deleteImage(index) {
      this.dummyExperiment.images.splice(index, 1)
      this.hasChanged = true
    },
    deleteVideo(index) {
      this.dummyExperiment.videos.splice(index, 1)
      this.hasChanged = true
    },
    addLink() {
      this.dummyExperiment.links = this.dummyExperiment.links || []
      this.dummyExperiment.links.push("")
      this.hasChanged = true
    },
    appendHttp(index) {
      if (!this.dummyExperiment.links[index]) return
      if (this.dummyExperiment.links[index].indexOf("http") !== 0)
        this.dummyExperiment.links.splice(
          index,
          1,
          `http://${this.dummyExperiment.links[index]}`
        )
    },
    deleteLink(index) {
      this.dummyExperiment.links.splice(index, 1)
      this.hasChanged = true
    },
    onScroll() {
      this.toolbarOnTop = window.scrollY > this.initialToolbarTop
    },
    updateIrScore(value) {
      this.dummyExperiment.ir_score = parseInt(value) || null;
    }
  },
  beforeMount() {
    this.resetDummyExperiment()
  },
  mounted() {
    this.initialToolbarTop =
      this.$el.querySelector("#button-toolbar").offsetTop || 0
  },
  created() {
    window.addEventListener("scroll", this.onScroll);
    if(!this.experiment) {
      this.saveInterval = setInterval(() => {
        localStorage.setItem("draft-experiment", JSON.stringify(this.dummyExperiment));
      }, 1000 * 15);
      if(localStorage.getItem("draft-experiment")) {
        console.log(JSON.parse(localStorage.getItem("draft-experiment")))
        this.dummyExperiment = JSON.parse(localStorage.getItem("draft-experiment"));
      } 
    }
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.onScroll)
  },
}
</script>

<style scoped>
.v-input--checkbox {
  margin-top: 0;
  padding-top: 0;
}
</style>

<style>
.v-input--checkbox .v-input__slot {
  margin-bottom: 0;
}
</style>
