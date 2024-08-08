import {useSettingsStore} from "@/shared/pinia/settings-store.ts";

class VibrationService {
  private static settingsStore = useSettingsStore();

  public static light = () => {
    if (Telegram.WebApp && this.settingsStore.vibrationOn) {
      Telegram.WebApp.HapticFeedback.impactOccurred('light');
    }
  }

  public static medium = () => {
    if (Telegram.WebApp && this.settingsStore.vibrationOn) {
      Telegram.WebApp.HapticFeedback.impactOccurred('medium');
    }
  }

  public static heavy = () => {
    if (Telegram.WebApp && this.settingsStore.vibrationOn) {
      Telegram.WebApp.HapticFeedback.impactOccurred('heavy');
    }
  }
}

export default VibrationService;