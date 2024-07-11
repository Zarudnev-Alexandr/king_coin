<script setup lang="ts">
interface Props {
  level: number;
}

const props: Props = defineProps<Props>();
</script>

<template>
  <div class="level-indicator">
    <div class="level" :style="{ width: `${props.level / 40 * 100}%` }"></div>
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