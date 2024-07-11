import {defineStore} from "pinia";
import {ref} from "vue";

export const useUserStore = defineStore('userStore', () => {
    const isAuth = ref<Boolean>(false);
    const setAuth = (auth: Boolean) => {
        isAuth.value = auth;
    }

    return {
        isAuth,
        setAuth,
    };
});