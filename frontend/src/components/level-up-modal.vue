<script setup lang="ts">

import ActionModal from "@/components/ActionModal.vue";
import {useUserStore} from "@/shared/pinia/user-store.ts";

const userStore = useUserStore();

const handleClose = () => {
  userStore.setLevelUpVisible(false);
}
</script>

<template>
  <action-modal @close="handleClose" @on-accept="handleClose" v-if="userStore.levelUpData && userStore.levelUpVisible">
    <div class="level-up-modal-wrapper">
      <div style="height: 30px"/>
      <img src="@/assets/img/game/player.png" alt="">
      <span class="level-up-modal-title sf-pro-font">Level Up!</span>
      <span class="level-up-description sf-pro-font">Теперь ты очень крутая горилла!</span>
      <div style="height: 20px"/>
      <div style="display: flex; flex-direction: column; gap: 5px; align-items: center">
        <span class="level-up-description sf-pro-font">Уровень {{ userStore.levelUpData?.new_lvl ?? 0 }}</span>
        <div class="level-up-reward">
          <img src="@/assets/svg/coin.svg" alt="">
          <span class="sf-pro-font">+ {{ userStore.levelUpData?.new_taps_for_lvl ?? 0 }} монета</span>
        </div>
      </div>

    </div>
  </action-modal>
</template>

<style scoped>
.level-up-modal-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 0;
  gap: 15px;

  img {
    width: 106px;
    height: 80px;
    transform: rotate(7deg);
  }

  .level-up-modal-title {
    font-size: 25px;
    font-weight: 700;
    line-height: 29.83px;
    text-align: center;
    color: white;
  }

  .level-up-description {
    font-size: 10px;
    font-weight: 400;
    line-height: 11.93px;
    text-align: center;
    color: rgba(194, 163, 117, 1);
    width: 65%;
  }

  .level-up-reward {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;

    img {
      width: 14px;
      height: 14px;
    }

    span {
      font-size: 12px;
      font-weight: 600;
      line-height: 14.32px;
      text-align: center;
      color: white;
    }
  }
}
</style>