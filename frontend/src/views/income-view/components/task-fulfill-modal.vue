<script setup lang="ts">
import ActionModal from "@/components/ActionModal.vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import TaskFulfillSubribeContent from "@/views/income-view/components/task-fulfill-subscribe-content.vue";
import TaskFulfullDailyContent from "@/views/income-view/components/task-fulfull-daily-content.vue";
import TasksApiService from "@/shared/api/services/tasks-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {useIncomeStore} from "@/shared/pinia/income-store.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import {Ref, ref} from "vue";

const appStore = useAppStore();
const taskStore = useIncomeStore();
const userStore = useUserStore()
const taskApiService = new TasksApiService(axiosInstance, errorHandler);
const isReady: Ref<boolean> = ref(false);

const handleClose = () => {
  isReady.value = false;
  appStore.setSelectTaskForFulfill(null);
}

const handleAccept = () => {
  if (appStore.selectTaskForFulfill?.type === 'daily' && !taskStore.dailyTask?.is_collect) {
    claimDailyReward();
  } else if (!appStore.selectTaskForFulfill?.completed) {
    if (isReady.value) {
      checkTask();
    } else {
      setTimeout(() => {
        setIsReady();
      }, 5000);

      if (appStore.selectTaskForFulfill?.link) {
        window.open(appStore.selectTaskForFulfill?.link, '_blank');
      }
    }

  }
}

const setIsReady = () => {
  isReady.value = true;
}

const claimDailyReward = async () => {
  const res = await taskApiService.claimDailyTask();
  if (res && res.right) {
    taskStore.claimDailyTask();
    userStore.user!.money += res.right.reward;
    appStore.setSelectTaskForFulfill(null);
  }
}

const checkTask = async () => {
  const res = await taskApiService.checkTask(appStore.selectTaskForFulfill!.id);
  if (res && res.right) {
    taskStore.taskCompleted(appStore.selectTaskForFulfill!.id);
    userStore.user!.money += res.right.money_received;
    appStore.setSelectTaskForFulfill(null);
  }
}

const getMainButtonText = () => {
  if (appStore.selectTaskForFulfill?.type === 'subscribe_telegram' || appStore.selectTaskForFulfill?.type === 'generic') {
    console.log("isReady", isReady.value)
    return isReady.value ? 'Получить' : 'Выполнить';
  }
  return 'Забрать';
}
</script>

<template>
  <ActionModal v-if="appStore.selectTaskForFulfill"
               @close="handleClose"
               @on-accept="handleAccept"
               :main-button-text="getMainButtonText()">
    >
    <task-fulfill-subribe-content
        v-if="appStore.selectTaskForFulfill.type === 'subscribe_telegram' || appStore.selectTaskForFulfill?.type === 'generic'"/>
    <task-fulfull-daily-content v-if="appStore.selectTaskForFulfill.type === 'daily'"/>
    <task-fulfill-subribe-content v-if="appStore.selectTaskForFulfill.type === 'invite'"/>
  </ActionModal>
</template>

<style scoped>

</style>