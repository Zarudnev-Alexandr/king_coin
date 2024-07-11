<script setup lang="ts">
const emit = defineEmits(['onClick']);

const onClick = () => {
  emit('onClick');
};
</script>

<template>
  <div class="bg-icon" @click="onClick">
    <slot></slot>
  </div>
</template>

<style scoped>
.bg-icon {
  background-image: url("@/assets/svg/bg-icon.svg");
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>