import {defineStore} from "pinia";
import {ref} from "vue";
import {User, UserBoost} from "@/shared/api/types/user.ts";

export const useUserStore = defineStore('userStore', () => {
  const isAuth = ref<Boolean>(false);
  const user = ref<User | null>(null);
  const bonusVisible = ref<Boolean>(true);

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
  };
});