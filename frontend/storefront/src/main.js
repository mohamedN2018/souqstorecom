import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import { i18n } from "./i18n";
import { useSiteStore } from "./stores/site";
import "./style.css";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(i18n);

// Load the admin-defined global site theme before/at first paint.
useSiteStore(pinia).load();

app.mount("#app");
