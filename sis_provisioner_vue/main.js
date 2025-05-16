import { createApp } from "vue";
import { createBootstrap } from "bootstrap-vue-next";
import { createPinia } from "pinia";

// import solstice-vue
import SolsticeVue from "solstice-vue";

import App from "@/app.vue";
import router from "@/router";

import VueGtag from "vue-gtag-next";
import { Vue3Mq, MqResponsive } from "vue3-mq";

// bootstrap js + bootstrap-icons
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";

// solstice bootstrap theme
import "solstice-theme/dist/solstice.scss";

// solstice-vue comps
import "solstice-vue/dist/style.css";

// bootstrap-vue-next css
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";

const app = createApp(App);

// MARK: google analytics data stream measurement_id
const gaCode = document.body.getAttribute("data-google-analytics");
const debugMode = document.body.getAttribute("data-django-debug");

app.config.productionTip = false;

// vue-gtag-next
app.use(VueGtag, {
  isEnabled: debugMode == "false",
  property: {
    id: gaCode,
    params: {
      anonymize_ip: true,
    },
  },
});

// vue-mq (media queries)
app.use(Vue3Mq, {
  preset: "bootstrap5",
});
app.component("mq-responsive", MqResponsive);

// pinia (vuex) state management
const pinia = createPinia();
app.use(pinia);

// bootstrap-vue-next
app.use(createBootstrap());
app.use(SolsticeVue);

app.use(router);

app.mount("#app");
