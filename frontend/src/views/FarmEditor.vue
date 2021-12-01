<template>
  <div id="farmer-edit">
    <Loader v-if="updateInProgress" title="Juste un instant..." :loading="updateInProgress" />
    <Title :breadcrumbs="breadcrumbs" />

    <v-container class="constrained">
      <v-app-bar
        style="margin-left: auto; margin-right: auto;"
        max-width="1000"
        color="white"
        :elevation="toolbarOnTop ? 2 : 0"
        :fixed="toolbarOnTop"
        id="button-toolbar"
      >
        <v-toolbar-title class="primary--text"></v-toolbar-title>
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
          :small="$vuetify.breakpoint.name === 'xs'"
          class="text-none"
          :disabled="!hasChanged"
          color="primary"
          @click="updateFarmer"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-content-save</v-icon>Sauvegarder
        </v-btn>
      </v-app-bar>

      <v-form ref="form" v-model="formIsValid">
        <!-- FARM NAME -->
        <div class="field">
          <div class="field-title title">
            Le nom de votre exploitation
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-text-field
            hide-details="auto"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.farm_name"
            :rules="[validators.notEmpty]"
          ></v-text-field>
        </div>

        <!-- PRODUCTIONS -->
        <div class="field">
          <div class="field-title title">
            Quelles productions sont présentes sur votre exploitation ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <div class="field-helper">Vous pouvez en sélectionner plusieurs</div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Grandes cultures"
            value="Grandes cultures"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Cultures d'industries" 
            value="Cultures d'industries"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Légumes de plein champs"
            value="Légumes de plein champs"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage ruminant"
            value="Élevage ruminant"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage monogastrique"
            value="Élevage monogastrique"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Arboriculture"
            value="Arboriculture"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Viticulture"
            value="Viticulture"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Maraîchage diversifié"
            value="Maraîchage diversifié"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Apiculture"
            value="Apiculture"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="PPAM"
            value="PPAM"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Cultures spécialisées"
            value="Cultures spécialisées"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
        </div>

        <!-- INSTALLATION DATE -->

        <div class="field">
          <div class="field-title title">
            Quand vous êtes-vous installé sur l'exploitation ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <div class="field-helper">Renseignez l'année (par exemple, 2001)</div>

          <v-text-field
            hide-details="auto"
            @input="onInstallationYearChange"
            :rules="[validators.isYear, validators.notEmpty]"
            outlined
            dense
            :value="installationYear"
          ></v-text-field>
        </div>

        <!-- POSTAL CODE -->

        <div class="field">
          <div class="field-title title">
            Le code postal de votre exploitation
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-text-field
            hide-details="auto"
            :rules="[validators.notEmpty]"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.postal_code"
          ></v-text-field>
        </div>

        <!-- PERSONNEL -->

        <div class="field">
          <div class="field-title title">
            Combien de personnes travaillent sur l'exploitation à temps plein ?
            <span
              class="mandatory"
            >- obligatoire</span>
          </div>
          <div class="field-helper">Comptez-vous et vos associés, salariés et alternants</div>
          <v-text-field
            hide-details="auto"
            :rules="[validators.notEmpty]"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.personnel"
          ></v-text-field>
        </div>

        <!-- SURFACE -->
        <div>
          <div class="field parent-field">
            <div class="field-title title">
              La surface de votre exploitation (en ha.)
              <span class="mandatory">- obligatoire</span>
            </div>
            <v-text-field
              hide-details="auto"
              :rules="[validators.notEmpty]"
              @input="hasChanged = true"
              outlined
              dense
              v-model="dummyFarmer.surface"
            ></v-text-field>
          </div>

          <!-- SURFACE CULTURES -->

          <div class="field child-field">
            <div class="field-title subtitle-2">La surface en cultures (en ha.)</div>
            <v-text-field
              hide-details="auto"
              @input="hasChanged = true"
              outlined
              dense
              v-model="dummyFarmer.surface_cultures"
            ></v-text-field>
          </div>

          <!-- SURFACE MEADOWS -->

          <div class="field child-field">
            <div
              class="field-title subtitle-2"
            >La surface en prairie permanente (en ha.)</div>
            <v-text-field
              hide-details="auto"
              @input="hasChanged = true"
              outlined
              dense
              v-model="dummyFarmer.surface_meadows"
            ></v-text-field>
          </div>
        </div>
        <!-- LIVESTOCK TYPES -->

        <div class="field">
          <div class="field-title title">Si vous avez de l'élevage, quel type d'élevage avez-vous ?</div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Bovin lait"
            value="Bovin lait"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Bovin allaitant"
            value="Bovin allaitant"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Ovin"
            value="Ovin"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Caprin"
            value="Caprin"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Avicole"
            value="Avicole"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Porcin"
            value="Porcin"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Autre"
            value="Autre"
          ></v-checkbox>
        </div>

        <!-- LIVESTOCK NUMBER -->

        <div class="field">
          <div class="field-title title">Si vous avez de l'élevage, combien de bêtes avez-vous ?</div>
          <div class="field-helper">Indiquer le nombre de tête par élevage, les races et particularités de l'élevage s'il y en a</div>
          <v-textarea
            hide-details="auto"
            rows="3"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyFarmer.livestock_number"
          ></v-textarea>
        </div>

        <!-- CULTURES -->

        <div class="field">
          <div class="field-title title">
            Quelles cultures avez-vous sur l'exploitation ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <div class="field-helper">Lister les cultures et les espèces fourragères</div>
          <v-select
            :items="cultures"
            outlined
            @input="hasChanged = true"
            dense
            multiple
            v-model="dummyFarmer.cultures"
            :rules="[validators.notEmpty]">
          </v-select>
          <!--<v-textarea
            hide-details="auto"
            rows="3"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyFarmer.cultures"
            :rules="[validators.notEmpty]"
          ></v-textarea>-->
        </div>

        <!-- SOIL TYPE -->

        <div class="field">
          <div class="field-title title">
            Quels types de sols sont présents sur l'exploitation ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-textarea
            hide-details="auto"
            rows="3"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            :rules="[validators.notEmpty]"
            v-model="dummyFarmer.soil_type"
          ></v-textarea>
        </div>

        <!-- OUTPUT -->

        <!-- <div class="field">
          <div
            class="field-title title"
          >Quel est rendement moyen en blé tendre de l'exploitation (en quintaux / ha)</div>
          <v-text-field
            hide-details="auto"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.output"
          ></v-text-field>
        </div> -->

        <!-- DESCRIPTION -->

        <div class="field">
          <div class="field-title title">
            Description de la ferme
            <span class="mandatory">- obligatoire</span>
          </div>
          <div
            class="field-helper"
          >Pouvez-vous décrire l'histoire et le fonctionnement de votre exploitation ainsi que votre démarche et le type d'agriculture pratiquée</div>
          <v-textarea
            hide-details="auto"
            rows="5"
            @input="hasChanged = true"
            auto-grow
            outlined
            :rules="[validators.notEmpty]"
            dense
            v-model="dummyFarmer.description"
          ></v-textarea>
        </div>

        <!-- SPECIFICITIES -->

        <div class="field">
          <div
            class="field-title title"
          >Si il y en a, quelles sont les spécificités de l'exploitation ?</div>
          <div
            class="field-helper"
          >Irrigation, drainage, zone protégée, captage d'eau, parcellaire...</div>
          <v-textarea
            hide-details="auto"
            rows="5"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyFarmer.specificities"
          ></v-textarea>
        </div>

        <!-- AGRICULTURE TYPES -->

        <div class="field">
          <div
            class="field-title title"
          >Choisissez les termes qui correspondent à l'agriculture que vous pratiquez</div>
          <div class="field-helper">Vous pouvez en sélectionner plusieurs</div>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Agriculture Biologique"
            value="Agriculture Biologique"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Agriculture de Conservation des sols (couvert végétaux généralisés, semis direct ou très simplifié, travail du sol réduit, etc.)"
            value="Agriculture de Conservation des sols (couvert végétaux généralisés, semis direct ou très simplifié, travail du sol réduit, etc.)"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Techniques Culturales Simplifiées (couverts végétaux occasionnels, semis simplifié, labour occasionnel, etc.)"
            value="Techniques Culturales Simplifiées (couverts végétaux occasionnels, semis simplifié, labour occasionnel, etc.)"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Agroforesterie"
            value="Agroforesterie"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Conventionnel"
            value="Conventionnel"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Cahier des charges industriel"
            value="Cahier des charges industriel"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Label qualité (Label Rouge, AOP, IGP, etc...)"
            value="Label qualité (Label Rouge, AOP, IGP, etc...)"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Certification environnementale (HVE, etc...)"
            value="Certification environnementale (HVE, etc...)"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Autre"
            value="Autre"
          ></v-checkbox>
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
            v-for="(link, index) in dummyFarmer.links"
            :key="index"
            outlined
            dense
            placeholder="https://..."
            style="max-width: 600px;"
            v-model="dummyFarmer.links[index]"
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

        <!-- PHOTOS -->

        <div class="field">
          <div class="field-title title">Photos de votre exploitation</div>
          <div class="field-helper">Vous pouvez en ajouter plusieurs</div>
          <ImagesField :imageArray.sync="dummyFarmer.images" @change="hasChanged = true" />
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
              <span v-if="farmerUrlComponent">Votre profil a bien été mis à jour !</span>
              <span v-else>Votre profil a bien été créé ! Notre équipe la mettra en ligne bientôt.</span>
            </span>
            <span v-else>
              <v-icon style="margin-top: -3px; margin-right: 5px;">mdi-emoticon-sad-outline</v-icon>Oops ! On n'a pas pu mettre à jour votre profil. Veuillez essayer plus tard.
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

export default {
  name: "FarmEditor",
  components: { Title, Loader, ImagesField },
  metaInfo() {
    return {
      title: "Pour une Agriculture du Vivant - Mettez à jour les données de votre exploitation",
      meta: [
        {
          description:
            "Modifiez le descriptif de votre exploitation, les données associées et la philosophie",
        },
      ],
    }
  },
  props: {
    farmerUrlComponent: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      dummyFarmer: {
        production: [],
        surface_meadows: [],
        groups: [],
        agriculture_types: [],
        images: [],
        links: [],
        cultures: [],
      },
      toolbarOnTop: false,
      initialToolbarTop: 0,
      hasChanged: false,
      formIsValid: true,
      showDateModal: false,
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
        {text: "Raisin de table", value: "Raisin de table"},
        {text: "Vigne (vignification)", value: "Vigne (vignification)"},
        {
          header: "Autre",
        },
        {text: "Pas de culture",value: "Pas de culture",},
        {text: "Toutes les cultures",value: "Toutes les cultures",},
      ],
    }
  },
  computed: {
    updateInProgress() {
      return (
        this.$store.state.farmerEditLoadingStatus ==
        Constants.LoadingStatus.LOADING
      )
    },
    updateSucceeded() {
      return (
        this.$store.state.farmerEditLoadingStatus ===
        Constants.LoadingStatus.SUCCESS
      )
    },
    updateFailed() {
      return (
        this.$store.state.farmerEditLoadingStatus ===
        Constants.LoadingStatus.ERROR
      )
    },
    validators() {
      return validators
    },
    farmer() {
      if (!this.farmerUrlComponent) return undefined
      return this.$store.getters.farmerWithUrlComponent(this.farmerUrlComponent)
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
          text: this.farmer ? this.farmer.name : "Nouveau profil",
          disabled: true,
        },
      ]
    },
    installationYear() {
      if (!this.dummyFarmer.installation_date) return ""

      const dateElements = this.dummyFarmer.installation_date.split("-")
      if (dateElements.length != 3) return ""

      return dateElements[0]
    },
    hasProductions() {
      const errorMessage = "Vous devez en selectionner au moins une production"
      if (!this.dummyFarmer || !this.dummyFarmer.production) return errorMessage
      return this.dummyFarmer.production.length > 0 || errorMessage
    },
  },
  methods: {
    updateFarmer() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        window.scrollTo(0, 0)
        window.alert("Merci de vérifier les champs en rouge et réessayer")
        return
      }

      if (this.farmer) {
        const payload = utils.getObjectDiff(this.farmer, this.dummyFarmer)

        this.$store.dispatch("patchFarmer", {
          farmer: this.farmer,
          changes: payload,
        })
      }
    },
    closeOverlay() {
      const success = this.updateSucceeded
      this.$store.dispatch("resetFarmerEditLoadingStatus")
      if (success)
        this.$router.push({
          name: "Profile",
        })
    },
    cancelEdit() {
      this.$router.go(-1)
    },
    resetdummyFarmer() {
      if (this.farmer) {
        this.dummyFarmer = JSON.parse(JSON.stringify(this.farmer))
        this.dummyFarmer.images = this.dummyFarmer.images || []
      }
    },
    changeProfileImage(file) {
      this.hasChanged = true
      if (!file) {
        this.dummyFarmer.profile_image = undefined
        return
      }
      utils.toBase64(file, (base64) => {
        this.dummyFarmer.profile_image = base64
      })
    },
    deleteImage(index) {
      this.dummyFarmer.images.splice(index, 1)
      this.hasChanged = true
    },
    addLink() {
      this.dummyFarmer.links = this.dummyFarmer.links || []
      this.dummyFarmer.links.push("")
      this.hasChanged = true
    },
    appendHttp(index) {
      if (!this.dummyFarmer.links[index]) return
      if (this.dummyFarmer.links[index].indexOf("http") !== 0)
        this.dummyFarmer.links.splice(
          index,
          1,
          `http://${this.dummyFarmer.links[index]}`
        )
    },
    deleteLink(index) {
      this.dummyFarmer.links.splice(index, 1)
      this.hasChanged = true
    },
    onDatePickerChange(date) {
      this.dummyFarmer.installation_date = date
      this.hasChanged = true
    },
    onInstallationYearChange(year) {
      year = year.trim()
      this.dummyFarmer.installation_date = `${year}-01-01`
      this.hasChanged = true
    },
    handleUnload(e) {
      if (this.hasChanged) {
        e.preventDefault()
        e.returnValue = ""
      } else {
        delete e["returnValue"]
      }
    },
    onScroll() {
      this.toolbarOnTop = window.scrollY > this.initialToolbarTop
    },
  },
  watch: {
    updateSucceeded(newValue) {
      if (newValue) this.hasChanged = false
    },
  },
  beforeMount() {
    this.resetdummyFarmer()
  },
  mounted() {
    this.initialToolbarTop =
      this.$el.querySelector("#button-toolbar").offsetTop || 0
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
    window.addEventListener("scroll", this.onScroll)
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
    window.removeEventListener("scroll", this.onScroll)
  },
  beforeRouteLeave(to, from, next) {
    if (!this.hasChanged) {
      next()
      return
    }

    const answer = window.confirm(
      "Êtes-vous sûr de vouloir quitter cette page ? Vous avez des changements non-sauvegardés"
    )
    if (answer) {
      next()
    } else {
      next(false)
    }
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
