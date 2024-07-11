<script setup lang="ts">

import IncomeHeader from "@/views/income-view/components/income-header.vue";
import IncomeActualTasks from "@/views/income-view/components/income-actual-tasks.vue";
import {actualTasks, dailyTasks, listTasks} from "@/shared/constants/tasks.ts";
import IncomeDailyTasks from "@/views/income-view/components/income-daily-tasks.vue";
import IncomeTaskList from "@/views/income-view/components/income-task-list.vue";
</script>

<template>
  <div class="income-wrapper">
    <income-header/>
    <income-actual-tasks :task-list="actualTasks"/>
    <income-daily-tasks :task-list="dailyTasks"/>
    <income-task-list :task-list="listTasks"/>
  </div>
</template>

<style scoped>
.income-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/img/app-bg.png');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  overflow-y: auto;
  padding: 0 16px 90px 16px;
  box-sizing: border-box;
  gap: 10px;
}
</style>