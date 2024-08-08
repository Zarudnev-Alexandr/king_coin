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
  const vibrationService = new VibrationService();

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
      user.value.user_lvl = data.new_lvl;
      user.value.taps_for_level = data.new_taps_for_lvl;
      user.value.next_level_data.required_money = getLevelByIndex(data.new_lvl + 1).reward;
    }
  }

  const setMoneyUpdate = (updateData: SocketEventUpdate) => {
    if (user.value) {
      user.value.money = updateData.money;
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
  };
});