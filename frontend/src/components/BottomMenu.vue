<script setup lang="ts">
import AppMainButton from "@/components/AppMainButton.vue";
import {useRoute, useRouter} from "vue-router";
import {useGameStore} from "@/shared/pinia/game-store.ts";

const route = useRoute()
const router = useRouter();
const gameStore = useGameStore();

const handleClick = (name: string) => {
  if (gameStore.gameInitStarted && !gameStore.isPaused) {
    gameStore.setPause(true);
    gameStore.setCurrentActiveModal('exit');
    gameStore.setTransitionView(name);
    return;
  }

  try {
    router.push({name})
  } catch (e) {
    console.error(e)
  }
}

const handleMainButtonClick = () => {
  if (route.name === 'Gameplay') {
    if (gameStore.gameInitStarted)
      gameStore.setPause(!gameStore.isPaused);
  } else {
    handleClick('Gameplay')
  }
}
</script>

<template>
  <div class="menu-bottom-wrapper">
    <AppMainButton :title="$t('play')" class="main-button" @click="handleMainButtonClick">
      <span v-if="(gameStore.isPaused || !gameStore.gameInitStarted) || route.name !== 'Gameplay'" class="pause-play-text">{{ $t('play') }}</span>
      <div v-else class="app-button-pause">
        <img src="@/assets/svg/bottom-menu/menu-button-pause.svg" alt="">
        <span class="pause-play-text">{{ $t('pause') }}</span>
      </div>
    </AppMainButton>
    <div class="button-wrapper">
      <div class="button-item" @click="() => handleClick('Main')" :class="{'active' : route.name === 'Main'}">
        <div class="button-item-content">
          <img src="@/assets/svg/bottom-menu/main-active.svg" alt="" v-if="route.name === 'Main'">
          <img src="@/assets/svg/bottom-menu/main.svg" alt="" v-else>
          <span class="button-title">{{ $t('home') }}</span>
        </div>
      </div>
      <div class="button-item"
           @click="() => handleClick('Improvements')"
           :class="{'active' : route.name === 'Improvements'}">
        <div class="button-item-content">
          <img src="@/assets/svg/bottom-menu/improvement-active.svg" alt="" v-if="route.name === 'Improvements'">
          <img src="@/assets/svg/bottom-menu/improvement.svg" alt="" v-else>
          <span class="button-title">{{ $t('upgrades') }}</span>
        </div>
      </div>

      <div style="width: 97px">
      </div>

      <div class="button-item"
           @click="() => handleClick('Income')"
           :class="{'active' : route.name === 'Income'}">
        <div class="button-item-content">
          <img src="@/assets/svg/bottom-menu/income-active.svg" alt="" v-if="route.name === 'Income'">
          <img src="@/assets/svg/bottom-menu/income.svg" alt="" v-else>
          <span class="button-title">{{ $t('income') }}</span>
        </div>
      </div>
      <div class="button-item"
           @click="() => handleClick('Friends')"
           :class="{'active' : route.name === 'Friends'}"
      >
        <div class="button-item-content">
          <img src="@/assets/svg/bottom-menu/friends-active.svg" alt="" v-if="route.name === 'Friends'">
          <img src="@/assets/svg/bottom-menu/friends.svg" alt="" v-else>
          <span class="button-title">{{ $t('friends') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.menu-bottom-wrapper {
  position: fixed;
  bottom: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 0 10px;
  box-sizing: border-box;
  z-index: 20;
  background: transparent;

  .button-wrapper {
    background: rgba(57, 34, 0, 1);
    border-top: 3px solid white;
    border-left: 3px solid white;
    border-right: 3px solid white;
    border-radius: 15px 15px 0 0;
    -moz-border-radius-topleft: 15px;
    -moz-border-radius-topright: 15px;
    width: 100%;
    box-sizing: border-box;
    display: flex;
    gap: 3px;
    padding: 5px;

    .button-item {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 48px;
      border-radius: 10px;

      cursor: pointer;
      flex: 1;

      .button-item-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 5px;
      }

      .button-title {
        font-family: 'SF Pro Text', sans-serif;
        font-size: 10px;
        font-weight: 400;
        line-height: 11.93px;
        text-align: center;
        color: rgba(160, 116, 50, 1);
      }
    }

    .active {
      background: rgba(93, 56, 0, 1);
    }
  }

  .app-button-pause {
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: center;
  }

  .pause-play-text {
    font-family: 'SuperSquadRus', sans-serif;
    font-size: 14px;
    font-weight: 400;
    color: rgba(88, 54, 0, 1);
  }

  .main-button {
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 97px;
    height: 67px;
    transform: translate(-50%, 0);
  }
}
</style>