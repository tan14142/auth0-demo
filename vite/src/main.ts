import { createApp } from "vue";
import { createAuth0 } from "@auth0/auth0-vue";
import { audience, domain, clientId } from "../env.json";
import App from "./App.vue";

const app = createApp(App);
const auth0 = createAuth0({
    domain: domain,
    client_id: clientId,
    redirect_uri: window.location.origin,
    audience: audience,
})

app.use(auth0);
app.mount("#app");