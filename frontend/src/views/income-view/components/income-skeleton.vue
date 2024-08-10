<script setup lang="ts">
interface Props {
  isLoading: boolean;
  isDailyLoading: boolean;
}

const props = defineProps<Props>();
</script>

<template>
  <div class="income-skeleton-wrap">
    <div class="actual" v-if="props.isLoading">
      <img src="@/assets/svg/income/actual-tasks-coin-icon.png" alt="">
      <span class="sf-pro-font">Актуальные задания</span>
      <div class="task-item skeleton-loading"></div>
    </div>

    <div class="actual" v-if="props.isDailyLoading">
      <span class="sf-pro-font">Ежедневные задания</span>
      <div class="task-item skeleton-loading"></div>
      <div class="task-item skeleton-loading"></div>
    </div>

    <div class="actual" v-if="props.isLoading">
      <span class="sf-pro-font">Список заданий</span>
      <div class="task-item skeleton-loading"></div>
      <div class="task-item skeleton-loading"></div>
      <div class="task-item skeleton-loading"></div>
      <div class="task-item skeleton-loading"></div>
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
  background: linear-gradient(90deg, rgba(93, 56, 0, 1) 25%, rgba(113, 68, 0, 1) 50%, rgba(93, 56, 0, 1) 75%);
  background-size: 200% 100%; /* Увеличиваем размер фона для плавного эффекта */
  animation: skeleton-loading 1.5s infinite;
}

.income-skeleton-wrap {
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-sizing: border-box;

  .actual {
    border-radius: 10px;
    background-color: rgba(57, 34, 0, 1);
    padding: 20px 10px;
    display: flex;
    flex-direction: column;
    position: relative;
    gap: 10px;

    span {
      font-size: 12px;
      font-weight: 600;
      line-height: 14.32px;
      text-align: left;
      color: white;
      padding-left: 15px;
    }

    img {
      width: 70px;
      height: 67px;
      position: absolute;
      top: -30px;
      right: 5px;
    }
  }
}

.task-item {
  height: 59px;
  background-color: rgba(93, 56, 0, 1);
  border-radius: 10px;
}
</style>
