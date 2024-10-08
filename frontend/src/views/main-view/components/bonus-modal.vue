<script setup lang="ts">
import FloatButton from "@/components/FloatButton.vue";
import {computed} from "vue";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import {formatNumberWithSpaces} from "@/helpers/formats.ts";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import {useI18n} from "vue-i18n";

const userStore = useUserStore();
const appStore = useAppStore();
const {t} = useI18n();

const handleGetBonus = () => {
  userStore.setBonusVisible(false);
  userStore.animationPlusMoney(userStore.user!.total_income);
  appStore.playCoinAnimation();
}

const titleText = computed(() => {
  if (userStore.user?.is_registred) {
    if (userStore.user?.total_income === 5000) {
      return t('bonus');
    }
    return t('friend_bonus');
  } else {
    return t('profit');
  }
})

const subtitleText = computed(() => {
  if (userStore.user?.is_registred) {
    return t('glad_to_see_you');
  } else {
    return t('coins_accumulated');
  }
})
</script>

<template>
  <div class="bonus-modal-wrapper" v-if="userStore.bonusVisible">
    <div class="bonus-modal-content">
      <span class="bonus-title">{{ titleText }}</span>
      <h3 class="bonus-subtitle sf-pro-font">{{ subtitleText }}</h3>
      <div class="bonus-reward">
        <img src="@/assets/svg/coin.svg" alt="">
        <span class="sf-pro-font">{{ formatNumberWithSpaces(userStore.user?.total_income ?? 0) }}</span>
      </div>
      <FloatButton @click="handleGetBonus" style="width: 175px; height: 65px">
        <span class="bonus-main-button">{{ $t('get_it') }}</span>
      </FloatButton>
    </div>
    <img src="@/assets/img/bonus.png" style="width: 100%" alt="">
  </div>
</template>

<style scoped>
.bonus-modal-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 30;
  gap: 15px;
  background-color: rgba(0, 0, 0, 0.8);
  opacity: 0;
  transform: translateY(50px);
  animation: slideIn 0.5s ease-in-out forwards;

  .bonus-modal-content {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;

    .bonus-title {
      font-family: 'SuperSquadRus', sans-serif;
      font-size: 34px;
      font-weight: 400;
      line-height: 52.49px;
      text-align: center;
      color: white;
    }

    .bonus-subtitle {
      font-size: 12px;
      font-weight: 600;
      line-height: 17.38px;
      text-align: center;
      color: white;
      width: 206px;
    }

    .bonus-reward {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 5px;

      img {
        width: 30px;
        height: 30px;
      }

      span {
        font-size: 28px;
        font-weight: 700;
        line-height: 40.54px;
        text-align: left;
        color: white;
      }
    }

    .bonus-main-button {
      font-family: 'SuperSquadRus', sans-serif;
      font-size: 14px;
      font-weight: 400;
      line-height: 21.62px;
      text-align: center;
      color: rgba(93, 56, 0, 1);
    }
  }
}

@keyframes slideIn {
  to {
    opacity: 1; /* Конечная прозрачность */
    transform: translateY(0); /* Конечное смещение */
  }
}
</style>