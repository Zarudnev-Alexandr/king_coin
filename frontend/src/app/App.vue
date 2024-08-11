<script setup lang="ts">
import {useUserStore} from "@/shared/pinia/user-store.ts";
import SplashView from "@/views/SplashView.vue";
import MainLayout from "@/components/MainLayout.vue";
import NotAvailablePlatformView from "@/views/not-available-platform-view/not-available-platform-view.vue";
import Landscape from "@/components/landscape.vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import {useGameStore} from "@/shared/pinia/game-store.ts";

const userStore = useUserStore();
const appStore = useAppStore();
const gameStore = useGameStore();
Telegram.WebApp.expand();
const isMobile = Telegram.WebApp.platform === 'android' || Telegram.WebApp.platform === 'ios';

window.addEventListener('resize', () => {
  if (window.innerHeight > window.innerWidth) {
    appStore.setIsLandscape(false);
  } else {
    appStore.setIsLandscape(true);
    if (gameStore.currentActiveModal === '') {
      gameStore.setCurrentActiveModal('pause');
    }
  }
});
</script>

<template>
  <div v-set-screen-height style="width: 100%; height: 100%">
    <SplashView v-if="!userStore.isAuth && isMobile"/>
    <MainLayout v-if="userStore.isAuth && isMobile">
      <router-view/>
    </MainLayout>
    <not-available-platform-view v-if="!isMobile"/>
    <landscape v-if="appStore.isLandscape" />
  </div>
</template>

<style scoped>

</style>
