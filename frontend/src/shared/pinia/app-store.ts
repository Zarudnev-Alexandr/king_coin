import {defineStore} from "pinia";
import {Ref, ref} from "vue";
import Task from "@/shared/api/types/task.ts";

export const useAppStore = defineStore('appStore', () => {
    const selectCoinForImpro: Ref<any> = ref(null);
    const selectTaskForFulfill: Ref<Task | null> = ref(null);
    const visibleGameplay: Ref<boolean> = ref(false);

    const setSelectCoinForImpro = (coin: any) => {
        selectCoinForImpro.value = coin;
    }

    const setSelectTaskForFulfill = (task: Task | null) => {
        selectTaskForFulfill.value = task;
    }

    const setVisibleGameplay = (visible: boolean) => {
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