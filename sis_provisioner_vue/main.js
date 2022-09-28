import { createApp } from "vue";
import App from "./app.vue";
import router from "./router";
import store from "./store";

import VueGtag from "vue-gtag-next";
import { Vue3Mq, MqResponsive } from "vue3-mq";

// bootstrap js
import "bootstrap";

// custom bootstrap theming
import "./css/custom.scss";

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

app.use(router);
app.use(store);

app.mount("#app");
