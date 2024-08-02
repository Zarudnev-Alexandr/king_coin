import {createApp} from 'vue'
import './assets/css/style.css'
import App from './app/App.vue'
import router from "./app/router.ts";
import {createPinia} from "pinia";
import setScreenHeight from "@/app/set-screen-height.ts";

const pinia = createPinia()
const app = createApp(App)
app.use(router)

app.directive('set-screen-height', setScreenHeight);

app.use(pinia)
app.mount('#app')
