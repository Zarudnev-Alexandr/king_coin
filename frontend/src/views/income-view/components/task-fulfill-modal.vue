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
import {ref} from "vue";

const appStore = useAppStore();
const taskStore = useIncomeStore();
const userStore = useUserStore()
const taskApiService = new TasksApiService(axiosInstance, errorHandler);
const {t} = useI18n();
const isLoading = ref(false);

const handleClose = () => {
  appStore.setSelectTaskForFulfill(null);
}

const isDisabled = () => {
  if (appStore.selectTaskForFulfill?.type === 'daily') {
    return taskStore.dailyTask?.is_collect;
  }
  return appStore.selectTaskForFulfill?.completed;
}

const handleAccept = () => {
  if (appStore.selectTaskForFulfill?.type === 'daily' && !taskStore.dailyTask?.is_collect) {
    claimDailyReward();
  } else if (!appStore.selectTaskForFulfill?.completed) {
    checkTask();
  }
}

const claimDailyReward = async () => {
  isLoading.value = true;
  const res = await taskApiService.claimDailyTask();
  if (res && res.right) {
    taskStore.claimDailyTask();
    userStore.moneyPlus(res.right.user_check.money - userStore.user!.money);
    appStore.setSelectTaskForFulfill(null);
    appStore.playCoinAnimation();

    if (res.right.user_check.info) {
      userStore.setLevelUpData(res.right.user_check.info.data);
      userStore.setLevelUpVisible(true);
    }
  } else {
    appStore.pushToast(ToastType.ERROR, t('request_error_text'))
  }

  isLoading.value = false;
}

const checkTask = async () => {
  const checkTaskId = appStore.selectTaskForFulfill!.id;
  isLoading.value = true;
  const res = await taskApiService.checkTask(appStore.selectTaskForFulfill!.id);
  if (res && res.right) {
    taskStore.taskCompleted(checkTaskId);
    userStore.moneyPlus(res.right.user_check.money - userStore.user!.money);
    appStore.setSelectTaskForFulfill(null);
    appStore.playCoinAnimation();

    if (res.right.user_check.info) {
      userStore.setLevelUpData(res.right.user_check.info.data);
      userStore.setLevelUpVisible(true);
    }
  }

  isLoading.value = false;

  if (res && res.left) {
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

const getDisabledButtonText = () => {
  if (!isDisabled()) return t('claim');
  if (appStore.selectTaskForFulfill?.type === 'daily') {
    return t('see_you_tomorrow')
  }

  return t('completed');
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
          :is-loading="isLoading"
          :disabled-text="getDisabledButtonText()"
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