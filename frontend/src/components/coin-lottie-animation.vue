<script setup lang="ts">
import CoinAnimationJson from "@/assets/lottie/coin-animation.json";
import {Vue3Lottie} from 'vue3-lottie';
import {ref} from "vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";

const lottieAnimation = ref(null);
const appStore = useAppStore();

// Размеры из Lottie JSON
const animationWidth = 375;
const animationHeight = 712;
const aspectRatio = animationWidth / animationHeight;

</script>

<template>
  <div
      style="position:absolute; z-index: 25; width: 100%; height: 100%; bottom: 0;left: 0; display: flex; justify-content: center; align-items: center;"
      v-if="appStore.coinAnimation">
    <Vue3Lottie
        ref="lottieAnimation"
        :animationData="CoinAnimationJson"
        :auto-play="true"
        :loop="false"
        :style="{ width: '100%', height: `calc(100% * ${1/aspectRatio})` }"/>
  </div>
</template>