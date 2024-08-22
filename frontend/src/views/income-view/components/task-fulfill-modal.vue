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
import ModalActionButton from "@/components/ModalActionButton.vue";
import {useI18n} from "vue-i18n";
import {ToastType} from "@/shared/api/types/toast.ts";

const appStore = useAppStore();
const taskStore = useIncomeStore();
const userStore = useUserStore()
const taskApiService = new TasksApiService(axiosInstance, errorHandler);
const isReady: Ref<boolean> = ref(false);
const {t} = useI18n();

const handleClose = () => {
  isReady.value = false;
  appStore.setSelectTaskForFulfill(null);
}

const isDisabled = () => {
  return appStore.selectTaskForFulfill?.type === 'daily' && taskStore.dailyTask?.is_collect;
}

const handleAccept = () => {
  if (appStore.selectTaskForFulfill?.type === 'daily' && !taskStore.dailyTask?.is_collect) {
    claimDailyReward();
  } else if (!appStore.selectTaskForFulfill?.completed) {
    if (appStore.selectTaskForFulfill?.type === 'subscribe_telegram') {
      checkTask();
      return;
    }

    if (isReady.value) {
      checkTask();
    } else {
      setTimeout(() => {
        setIsReady();
      }, 1000);

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
  } else {
    appStore.pushToast(ToastType.ERROR, t('no_subscription'));
  }
}

const getMainButtonText = () => {
  if (appStore.selectTaskForFulfill?.type === 'generic') {
    return isReady.value ? t('get_it') : t('complete');
  } else if (appStore.selectTaskForFulfill?.type === 'subscribe_telegram') {
    return t('get_it')
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
      <task-fulfill-subribe-content v-if="appStore.selectTaskForFulfill.type === 'invite'"/>
    </template>
  </ActionModal>
</template>

<style scoped>

</style>