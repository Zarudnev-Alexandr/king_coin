import {createApp} from 'vue'
import './assets/css/style.css'
import App from './app/App.vue'
import router from "./app/router.ts";
import {createPinia} from "pinia";
import setScreenHeight from "@/app/set-screen-height.ts";
import Vue3Lottie from "vue3-lottie";
import {i18n} from "@/app/i18n.ts";

const pinia = createPinia()
const app = createApp(App)
app.use(router)
app.use(Vue3Lottie, { name: "Vue3Lottie" })

app.directive('set-screen-height', setScreenHeight);

app.use(i18n);
app.use(pinia);
Telegram.WebApp.disableVerticalSwipes();
app.mount('#app')
