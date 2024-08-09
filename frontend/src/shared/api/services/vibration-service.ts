import {useSettingsStore} from "@/shared/pinia/settings-store.ts";

class VibrationService {
  settingsStore = useSettingsStore();

  public light = () => {
    if (Telegram.WebApp && this.settingsStore.vibrationOn) {
      Telegram.WebApp.HapticFeedback.impactOccurred('light');
    }
  }

  public medium = () => {
    if (Telegram.WebApp && this.settingsStore.vibrationOn) {
      Telegram.WebApp.HapticFeedback.notificationOccurred('success');
    }
  }

  public heavy = () => {
    if (Telegram.WebApp && this.settingsStore.vibrationOn) {
      Telegram.WebApp.HapticFeedback.impactOccurred('heavy');
    }
  }
}

export default VibrationService;