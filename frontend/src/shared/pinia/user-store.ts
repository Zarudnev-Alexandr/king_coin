import {defineStore} from "pinia";
import {ref} from "vue";
import {User} from "@/shared/api/types/user.ts";

export const useUserStore = defineStore('userStore', () => {
  const isAuth = ref<Boolean>(false);
  const user = ref<User | null>(null);

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

  return {
    isAuth,
    setAuth,
    user,
    setUser,
    moneyPlus,
  };
});