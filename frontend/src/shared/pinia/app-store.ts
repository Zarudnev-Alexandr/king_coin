import {defineStore} from "pinia";
import {Ref, ref} from "vue";

export const useAppStore = defineStore('appStore', () => {
    const selectCoinForImpro: Ref<any> = ref(null);
    const selectTaskForFulfill: Ref<any> = ref(null);
    const visibleGameplay: Ref<boolean> = ref(false);

    const setSelectCoinForImpro = (coin: any) => {
        selectCoinForImpro.value = coin;
    }

    const setSelectTaskForFulfill = (task: any) => {
        selectTaskForFulfill.value = task;
    }

    const setVisibleGameplay = (visible: boolean) => {
        console.log(visible);
        visibleGameplay.value = visible;
    }

    return {
        selectCoinForImpro,
        setSelectCoinForImpro,
        selectTaskForFulfill,
        setSelectTaskForFulfill,
        visibleGameplay,
        setVisibleGameplay,
    }
});