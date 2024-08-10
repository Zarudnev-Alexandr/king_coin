<script setup lang="ts">
</script>

<template>
  <div class="friends-skeleton-wrapper">
    <div class="friends-statistic">
      <div class="friends-count skeleton-loading"></div>
      <div class="friends-count skeleton-loading"></div>
    </div>
    <div v-for="_ in 6" class="friend-item skeleton-loading"></div>
  </div>
</template>

<style scoped>
@keyframes skeleton-loading {
  0% {
    background-position: -150% 0;
  }
  100% {
    background-position: 150% 0;
  }
}

.skeleton-loading {
  background: linear-gradient(90deg, rgba(93, 56, 0, 1) 25%, rgba(113, 68, 0, 1) 50%, rgba(93, 56, 0, 1) 75%);
  background-size: 200% 100%; /* Увеличиваем размер фона для плавного эффекта */
  animation: skeleton-loading 1.5s infinite;
}

.friends-skeleton-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px 10px;
  margin: 0 16px;
  box-sizing: border-box;
  background-color: rgba(57, 34, 0, 1);
  border-radius: 10px;

  .friends-statistic {
    box-sizing: border-box;
    padding: 0 8px;
    display: flex;
    justify-content: space-between;

    .friends-count {
      box-sizing: border-box;
      width: 85px;
      height: 15px;
      border-radius: 4px;
      background-color: rgba(93, 56, 0, 1);
    }
  }

  .friend-item {
    height: 60px;
    border-radius: 10px;
    background-color: rgba(93, 56, 0, 1);
    box-sizing: border-box;
  }
}
</style>
