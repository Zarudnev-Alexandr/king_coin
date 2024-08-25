<script setup lang="ts">
import ActionModal from "@/components/ActionModal.vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import TaskFulfillSubribeContent from "@/views/income-view/components/task-fulfill-subscribe-content.vue";
import TaskFulfullDailyContent from "@/views/income-view/components/task-fulfull-daily-content.vue";
import TasksApiService from "@/shared/api/services/tasks-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {useIncomeStore} from "@/shared/pinia/income-store.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import ModalActionButton from "@/components/ModalActionButton.vue";
import {useI18n} from "vue-i18n";
import {ToastType} from "@/shared/api/types/toast.ts";
import TaskFulfillInivteContent from "@/views/income-view/components/task-fulfill-inivte-content.vue";

const appStore = useAppStore();
const taskStore = useIncomeStore();
const userStore = useUserStore()
const taskApiService = new TasksApiService(axiosInstance, errorHandler);
const {t} = useI18n();

const handleClose = () => {
  appStore.setSelectTaskForFulfill(null);
}

const isDisabled = () => {
  return appStore.selectTaskForFulfill?.type === 'daily' && taskStore.dailyTask?.is_collect;
}

const handleAccept = () => {
  if (appStore.selectTaskForFulfill?.type === 'daily' && !taskStore.dailyTask?.is_collect) {
    claimDailyReward();
  } else if (!appStore.selectTaskForFulfill?.completed) {
    checkTask();
  }
}

const claimDailyReward = async () => {
  const res = await taskApiService.claimDailyTask();
  if (res && res.right) {
    taskStore.claimDailyTask();
    userStore.moneyPlus(res.right.reward);
    appStore.setSelectTaskForFulfill(null);
    appStore.playCoinAnimation();
  }
}

const checkTask = async () => {
  const checkTaskId = appStore.selectTaskForFulfill!.id;
  const res = await taskApiService.checkTask(appStore.selectTaskForFulfill!.id);
  if (res && res.right) {
    taskStore.taskCompleted(checkTaskId);
    userStore.user!.money += res.right.money_received;
    appStore.setSelectTaskForFulfill(null);
    appStore.playCoinAnimation();
  }

  if (res && res.left) {
    console.log(res.left);
    if (appStore.selectTaskForFulfill?.type === 'generic') {
      if (res.left.message === 'Task not started yet') {
        appStore.pushToast(ToastType.ERROR, t('not_completed_task'));
      } else {
        appStore.pushToast(ToastType.WARNING, t('wait_20_min'))
      }
      return;
    }

    appStore.pushToast(ToastType.ERROR, t('not_completed_task'));
  }
}

const getMainButtonText = () => {
  if (appStore.selectTaskForFulfill?.type === 'generic') {
    return t('check');
  } else if (appStore.selectTaskForFulfill?.type === 'subscribe_telegram') {
    return t('get_it');
  } else if (appStore.selectTaskForFulfill?.type === 'invite') {
    return t('check');
  }
  return t('claim');
}
</script>

<template>
  <ActionModal v-if="appStore.selectTaskForFulfill"
               @close="handleClose"
               @on-accept="handleAccept"
               :main-button-text="getMainButtonText()">
    <template #actions>
      <modal-action-button
          style="width: 133px; height: 67px"
          :button-text="getMainButtonText()"
          @on-accept="handleAccept"
          :is-disabled="isDisabled()"
          :disabled-text="isDisabled() ? $t('see_you_tomorrow') : $t('claim')"
      />
    </template>
    <template #default>
      <task-fulfill-subribe-content
          v-if="appStore.selectTaskForFulfill.type === 'subscribe_telegram' || appStore.selectTaskForFulfill?.type === 'generic'"/>
      <task-fulfull-daily-content v-if="appStore.selectTaskForFulfill.type === 'daily'"/>
      <task-fulfill-inivte-content v-if="appStore.selectTaskForFulfill.type === 'invite'"/>
    </template>
  </ActionModal>
</template>

<style scoped>

</style>