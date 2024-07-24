<script setup lang="ts">
import IncomeTaskItem from "@/views/income-view/components/income-task-item.vue";
import Task from "@/shared/api/types/task.ts";

const task = {
  name: "Подпишись на Telegram канал",
  reward: 13188500,
  completed: false,
  type: 'subscription',
  description: "Подпишись на наш Telegram канал и получи 13 188 500 KingCoin",
  link: null,
  requirement: 0,
  id: 0,
} as Task;
</script>

<template>
  <div class="actual-tasks-wrap">
    <img src="@/assets/svg/income/actual-tasks-coin-icon.png" alt="">
    <h3 class="sf-pro-font">Актуальные задания</h3>
    <div class="task-list-wrap">
      <IncomeTaskItem :task-item="task"/>
    </div>
  </div>
</template>

<style scoped>
.actual-tasks-wrap {
  background-color: rgba(57, 34, 0, 1);
  border-radius: 10px;
  padding: 15px 10px;
  display: flex;
  flex-direction: column;
  position: relative;

  .task-list-wrap {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  img {
    width: 70px;
    height: 67px;
    position: absolute;
    top: -30px;
    right: 5px;
  }

  h3 {
    font-size: 12px;
    font-weight: 600;
    line-height: 14.32px;
    text-align: left;
    color: white;
    padding-left: 15px;
  }
}
</style>