import {defineStore} from "pinia";
import {ref} from "vue";
import {User, UserBoost} from "@/shared/api/types/user.ts";
import LvlUpData from "@/shared/api/types/lvl-up-data.ts";
import SocketEventUpdate from "@/shared/api/types/socket-event-update.ts";
import {getLevelByIndex} from "@/helpers/levels.ts";
import VibrationService from "@/shared/api/services/vibration-service.ts";

export const useUserStore = defineStore('userStore', () => {
  const isAuth = ref<Boolean>(false);
  const user = ref<User | null>(null);
  const bonusVisible = ref<Boolean>(true);
  const levelUpVisible = ref<Boolean>(false);
  const levelUpData = ref<LvlUpData | null>(null);
  const offlineBonusConfirm = ref(false);
  const vibrationService = new VibrationService();
  let playImproPulseAnimation = () => {
  }
  let playPulseAnimation = () => {
  };

  const setAuth = (auth: Boolean) => {
    isAuth.value = auth;
  }

  const setUser = (us: User | null) => {
    user.value = us;
  }

  const moneyPlus = (money: number) => {
    if (user.value) {
      user.value.money += money;
    }
  }

  const setPulseAnimationMethod = (pulseAnimation: () => void) => {
    playPulseAnimation = pulseAnimation;
  }

  const setImproPulseAnimationMethod = (pulseAnimation: () => void) => {
    playImproPulseAnimation = pulseAnimation;
  }

  const animationPlusMoney = (val: number) => {
    if (!user.value) return;

    playPulseAnimation();
    playImproPulseAnimation();
    const startTime = performance.now();
    const duration = 1000;
    const startVal = user.value?.money ?? 0;
    const updateInterval = 50; // Интервал обновления в миллисекундах

    function updateValue() {
      const currentTime = performance.now();
      const elapsedTime = currentTime - startTime;
      const progress = Math.min(elapsedTime / duration, 1);
      user.value!.money = startVal + (val * progress);

      if (progress < 1) {
        setTimeout(updateValue, updateInterval);
      } else {
        offlineBonusConfirm.value = true;
      }
    }

    updateValue();
  };

  const setMoney = (money: number) => {
    if (user.value) {
      user.value.money = money;
    }
  }

  const setBonusVisible = (visible: Boolean) => {
    bonusVisible.value = visible;
  }

  const setLevelUpVisible = (visible: Boolean) => {
    levelUpVisible.value = visible;
  }

  const setLevelUpData = (data: LvlUpData) => {
    levelUpData.value = data;
    if (user.value) {
      const oldTap = user.value?.taps_for_level;
      user.value.user_lvl = data.new_lvl;
      user.value.taps_for_level = data.new_taps_for_lvl;
      user.value.next_level_data.required_money = getLevelByIndex(data.new_lvl + 1).reward;
      levelUpData.value.new_taps_for_lvl = user.value.taps_for_level - oldTap;
    }
  }

  const setMoneyUpdate = (updateData: SocketEventUpdate) => {
    if (user.value) {
      if (!offlineBonusConfirm.value) {
        user.value.money = updateData.money - user.value.total_income;
      } else {
        user.value.money = updateData.money;
      }
      user.value.earnings_per_hour = updateData.hourly_income;
      user.value.next_level_data.money_to_get_the_next_boost = updateData.money_to_next_level;
    }
  }

  const updateBoostData = (nextBoost: UserBoost) => {
    if (user.value) {
      user.value.boost = user.value.next_boost;
      user.value.next_boost = nextBoost;
    }
  }

  return {
    isAuth,
    setAuth,
    user,
    setUser,
    moneyPlus,
    updateBoostData,
    setMoney,
    bonusVisible,
    setBonusVisible,
    levelUpVisible,
    setLevelUpVisible,
    levelUpData,
    setLevelUpData,
    setMoneyUpdate,
    vibrationService,
    setPulseAnimationMethod,
    setImproPulseAnimationMethod,
    animationPlusMoney,
    offlineBonusConfirm,
  };
});