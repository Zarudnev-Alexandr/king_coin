import {defineStore} from "pinia";
import {Ref, ref} from "vue";

export const useAppStore = defineStore('appStore', () => {
    const selectCoinForImpro: Ref<any> = ref(null);
    const selectTaskForFulfill: Ref<any> = ref(null);

    const setSelectCoinForImpro = (coin: any) => {
        selectCoinForImpro.value = coin;
    }

    const setSelectTaskForFulfill = (task: any) => {
        selectTaskForFulfill.value = task;
    }

    return {
        selectCoinForImpro,
        setSelectCoinForImpro,
        selectTaskForFulfill,
        setSelectTaskForFulfill,
    }
});