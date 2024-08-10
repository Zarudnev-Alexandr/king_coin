<script setup lang="ts">
</script>

<template>
  <div class="skeleton-wrapper">
    <div class="combo-header skeleton-loading"></div>

    <div class="combo-wrapper">
      <div v-for="_ in 3" class="combo-item skeleton-loading"></div>
    </div>

    <div class="coin-card-list-tab">
      <div class="coin-card-list-tab-item active">
        <span>Crypto</span>
      </div>
      <div class="coin-card-list-tab-item">
        <span>Action</span>
      </div>
      <div class="coin-card-list-tab-item">
        <span>Special</span>
      </div>
      <div class="coin-card-list-tab-item">
        <span>Soon</span>
      </div>
    </div>

    <div class="card-grid-wrapper">
      <div v-for="_ in 6" class="card-grid-item skeleton-loading"></div>
    </div>
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
  background: linear-gradient(90deg, rgba(57, 34, 0, 1) 25%, rgba(78, 46, 0, 1) 50%, rgba(57, 34, 0, 1) 75%);
  background-size: 200% 100%; /* Увеличиваем размер фона для более плавного эффекта */
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  padding: 0 16px;
  box-sizing: border-box;

  .combo-header {
    width: 100%;
    height: 40px;
    background-color: rgba(57, 34, 0, 1);
    border-radius: 10px;
  }

  .combo-wrapper {
    display: flex;
    gap: 5px;

    .combo-item {
      height: 77px;
      background-color: rgba(57, 34, 0, 1);
      flex: 1;
      border-radius: 10px;
    }
  }

  .coin-card-list-tab {
    display: flex;
    border-radius: 10px;
    background-color: rgba(57, 34, 0, 1);
    padding: 5px;

    .coin-card-list-tab-item {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 12px 24px;
      border-radius: 8px;
      flex: 1;

      span {
        font-family: 'SFProText', sans-serif;
        font-size: 10px;
        font-weight: 400;
        line-height: 11.93px;
        text-align: center;
        color: white;
      }
    }

    .active {
      background-color: rgba(93, 56, 0, 1);
    }
  }

  .card-grid-wrapper {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;

    .card-grid-item {
      height: 111px;
      background-color: rgba(57, 34, 0, 1);
      border-radius: 10px;
      width: 47%;
    }
  }
}
</style>
