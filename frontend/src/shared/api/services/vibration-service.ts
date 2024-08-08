import {useSettingsStore} from "@/shared/pinia/settings-store.ts";

class VibrationService {

  public static light = () => {
    const settingsStore = useSettingsStore();
    if (Telegram.WebApp && settingsStore.vibrationOn) {
      Telegram.WebApp.HapticFeedback.impactOccurred('light');
    }
  }

  public static medium = () => {
    const settingsStore = useSettingsStore();
    if (Telegram.WebApp && settingsStore.vibrationOn) {
      Telegram.WebApp.HapticFeedback.impactOccurred('medium');
    }
  }

  public static heavy = () => {
    const settingsStore = useSettingsStore();
    if (Telegram.WebApp && settingsStore.vibrationOn) {
      Telegram.WebApp.HapticFeedback.impactOccurred('heavy');
    }
  }
}

export default VibrationService;