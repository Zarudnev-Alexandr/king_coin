import {createApp} from 'vue'
import './assets/css/style.css'
import App from './app/App.vue'
import router from "./app/router.ts";
import {createPinia} from "pinia";
import setScreenHeight from "@/app/set-screen-height.ts";
import Vue3Lottie from "vue3-lottie";

const pinia = createPinia()
const app = createApp(App)
app.use(router)
app.use(Vue3Lottie, { name: "Vue3Lottie" })

app.directive('set-screen-height', setScreenHeight);

app.use(pinia)
app.mount('#app')
