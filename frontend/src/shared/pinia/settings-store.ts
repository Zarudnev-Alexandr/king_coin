import {defineStore} from "pinia";
import {LocalStorageService} from "@/shared/api/services/local-storage-service.ts";
import {ref} from "vue";
import Languages from "@/shared/constants/languages.ts";

export const useSettingsStore = defineStore('settingsStore', () => {
  const localLanguage = new LocalStorageService<{ name: string, icon: string }>('language');
  const localSoundOn = new LocalStorageService<boolean>('soundOn');
  const localVibrationOn = new LocalStorageService<boolean>('vibrationOn');

  if (localLanguage.getItem() === null) {
    localLanguage.setItem(Languages[0]);
  }

  if (localSoundOn.getItem() === null) {
    localSoundOn.setItem(true);
  }

  if (localVibrationOn.getItem() === null) {
    localVibrationOn.setItem(true);
  }

  const soundOn = ref(localSoundOn.getItem());
  const vibrationOn = ref(localVibrationOn.getItem());
  const currenLanguage = ref(localLanguage.getItem());

  const setSoundOn = (value: boolean) => {
    localSoundOn.setItem(value);
    soundOn.value = value;
  };

  const setVibrationOn = (value: boolean) => {
    localVibrationOn.setItem(value);
    vibrationOn.value = value;
  };

  const setLanguage = (value: { name: string, icon: string }) => {
    localLanguage.setItem(value);
    currenLanguage.value = value;
  };

  return {
    soundOn,
    setSoundOn,
    vibrationOn,
    setVibrationOn,
    currenLanguage,
    setLanguage,
  }
});