import {defineStore} from "pinia";
import {Ref, ref} from "vue";
import Task from "@/shared/api/types/task.ts";
import VibrationService from "@/shared/api/services/vibration-service.ts";
import {Toast, ToastType} from "@/shared/api/types/toast.ts";

export const useAppStore = defineStore('appStore', () => {
  const selectCoinForImpro: Ref<any> = ref(null);
  const selectTaskForFulfill: Ref<Task | null> = ref(null);
  const visibleGameplay: Ref<boolean> = ref(false);
  const coinAnimation: Ref<boolean> = ref(false);
  const toasts: Ref<Toast[]> = ref([]);
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

  const pushToast = (type: ToastType, message: string) => {
    // Ограничение количества тостов
    if (toasts.value.length >= 3) {
      toasts.value.shift();
    }

    // Добавление нового тоста
    const toast = new Toast(type, message);
    toasts.value.push(toast);

    // Удаление тоста через 2 секунды
    setTimeout(() => {
      const index = toasts.value.indexOf(toast);
      if (index !== -1) {
        toasts.value.splice(index, 1);
      }
    }, 2000);
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
    toasts,
    pushToast,
  }
});