<script setup lang="ts">

import IncomeHeader from "@/views/income-view/components/income-header.vue";
import IncomeActualTasks from "@/views/income-view/components/income-actual-tasks.vue";
import IncomeDailyTasks from "@/views/income-view/components/income-daily-tasks.vue";
import IncomeTaskList from "@/views/income-view/components/income-task-list.vue";
import {computed, onMounted, ref} from "vue";
import TasksApiService from "@/shared/api/services/tasks-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {useIncomeStore} from "@/shared/pinia/income-store.ts";
import VibrationService from "@/shared/api/services/vibration-service.ts";
import IncomeSkeleton from "@/views/income-view/components/income-skeleton.vue";
import TAppTaskList from "@/views/income-view/components/t-app-task-list.vue";

const taskService = new TasksApiService(axiosInstance, errorHandler);

const vibrationService = new VibrationService();
const {setTasks, setDailyTask, tasks, dailyTask} = useIncomeStore();
const isLoading = ref(false);
const isLoadingDaily = ref(false);

onMounted(async () => {
  vibrationService.light();

  if (tasks.length === 0) {
    isLoading.value = true;
    const res = await taskService.getTasks();
    if (res && res.right) {
      setTasks(res.right);
      isLoading.value = false;
    }
  }

  if (!dailyTask) {
    isLoadingDaily.value = true;
    const dailyRes = await taskService.getDailyTaskInfo();
    if (dailyRes && dailyRes.right) {
      setDailyTask(dailyRes.right);
      isLoadingDaily.value = false;
    }
  }
})

const isLoadingTasks = computed(() => {
  return isLoading.value || isLoadingDaily.value;
})
</script>

<template>
  <div class="income-wrapper">
    <income-header/>
    <income-actual-tasks v-if="!isLoadingTasks"/>
    <income-daily-tasks v-if="!isLoadingTasks"/>
    <income-task-list v-if="!isLoadingTasks"/>
    <income-skeleton v-if="isLoadingTasks"/>
    <t-app-task-list/>
  </div>
</template>

<style scoped>
.income-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/img/app-bg.webp');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  overflow-y: auto;
  padding: 0 16px 90px 16px;
  box-sizing: border-box;
  gap: 10px;
}
</style>