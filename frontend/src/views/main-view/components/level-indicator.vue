<script setup lang="ts">
import {useUserStore} from "@/shared/pinia/user-store.ts";
import {onMounted, ref, watch} from "vue";

const {user} = useUserStore();
const userStore = useUserStore();
const percent = ref(0);

const calcPercent = () => {
  if (!user?.next_level_data.lvl) {
    return 100;
  }

  if (user.next_level_data.required_money === 0) {
    return 0;
  }

  return (user.money / user.next_level_data.required_money) * 100;
}

watch(() => userStore.user?.money, (_) => {
  percent.value = calcPercent();
});

onMounted(() => {
  percent.value = calcPercent();
});
</script>

<template>
  <div class="level-indicator">
    <div class="level" :style="{ width: `${percent}%` }"></div>
  </div>
</template>

<style scoped>
.level-indicator {
  height: 6px;
  width: 100%;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  border: 1px solid white;
  display: flex;

  .level {
    background: linear-gradient(90deg, #FF8200 0%, #FFC800 100%);
  }
}
</style>