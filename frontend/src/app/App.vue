<script setup lang="ts">
import {useUserStore} from "@/shared/pinia/user-store.ts";
import SplashView from "@/views/SplashView.vue";
import MainLayout from "@/components/MainLayout.vue";

const userStore = useUserStore();
</script>

<template>
  <div v-set-screen-height style="width: 100%; height: 100%">
    <SplashView v-if="!userStore.isAuth"/>
    <MainLayout v-else>
      <router-view/>
    </MainLayout>
  </div>
</template>

<style scoped>

</style>
