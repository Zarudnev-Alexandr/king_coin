<script setup lang="ts">

</script>

<template>
  <div class="app-icon-with-shadow">
    <slot></slot>
    <img src="@/assets/svg/icon-shadow.svg" alt="" class="icon-shadow">
  </div>
</template>

<style scoped>
.app-icon-with-shadow {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 10px;

  .icon-shadow {
    width: 90%;
    height: 2.32px;
  }
}
</style>