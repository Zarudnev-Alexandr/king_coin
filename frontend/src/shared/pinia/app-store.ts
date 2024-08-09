import {defineStore} from "pinia";
import {Ref, ref} from "vue";
import Task from "@/shared/api/types/task.ts";
import VibrationService from "@/shared/api/services/vibration-service.ts";

export const useAppStore = defineStore('appStore', () => {
  const selectCoinForImpro: Ref<any> = ref(null);
  const selectTaskForFulfill: Ref<Task | null> = ref(null);
  const visibleGameplay: Ref<boolean> = ref(false);
  const coinAnimation: Ref<boolean> = ref(false);
  const vibrationService = new VibrationService();

  const setSelectCoinForImpro = (coin: any) => {
    selectCoinForImpro.value = coin;
  }

  const setSelectTaskForFulfill = (task: Task | null) => {
    selectTaskForFulfill.value = task;
  }

  const setVisibleGameplay = (visible: boolean) => {
    visibleGameplay.value = visible;
  }

  const setCoinAnimation = (visible: boolean) => {
    coinAnimation.value = visible;
  }

  const playCoinAnimation = () => {
    coinAnimation.value = true;
    vibrationService.heavy();
    setTimeout(() => {
      coinAnimation.value = false;
    }, 1200)
  }

  return {
    selectCoinForImpro,
    setSelectCoinForImpro,
    selectTaskForFulfill,
    setSelectTaskForFulfill,
    visibleGameplay,
    setVisibleGameplay,
    coinAnimation,
    setCoinAnimation,
    playCoinAnimation,
    vibrationService,
  }
});