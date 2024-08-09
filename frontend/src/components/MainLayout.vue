<script setup lang="ts">
import BottomMenu from "@/components/BottomMenu.vue";
import CardImprovementsModalContent from "@/views/improvements-view/components/card-improvements-modal-content.vue";
import TaskFulfillModal from "@/views/income-view/components/task-fulfill-modal.vue";
import ComboNotify from "@/views/improvements-view/components/combo-notify.vue";
import LevelUpModal from "@/components/level-up-modal.vue";
import BonusModal from "@/views/main-view/components/bonus-modal.vue";
import CoinLottieAnimation from "@/components/coin-lottie-animation.vue";
</script>

<template>
  <div style="width: 100%; height: 100%; position: relative;">
    <router-view/>
    <BottomMenu/>
    <CardImprovementsModalContent/>
    <TaskFulfillModal/>
    <ComboNotify/>
    <level-up-modal/>
    <bonus-modal/>
    <coin-lottie-animation/>
  </div>
</template>

<style scoped>

</style>