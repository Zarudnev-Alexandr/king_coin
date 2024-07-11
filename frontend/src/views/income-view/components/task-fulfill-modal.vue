<script setup lang="ts">
import ActionModal from "@/components/ActionModal.vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import TaskFulfillSubribeContent from "@/views/income-view/components/task-fulfill-subscribe-content.vue";
import TaskFulfullDailyContent from "@/views/income-view/components/task-fulfull-daily-content.vue";

const appStore = useAppStore();

const handleClose = () => {
  appStore.setSelectTaskForFulfill(null);
}

const handleAccept = () => {
  console.log("Было принято");
  appStore.setSelectTaskForFulfill(null);
}

const getMainButtonText = () => {
  if (appStore.selectTaskForFulfill.type === 'subscription') {
    return 'Выполнить';
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
    <task-fulfill-subribe-content v-if="appStore.selectTaskForFulfill.type === 'subscription'"/>
    <task-fulfull-daily-content v-if="appStore.selectTaskForFulfill.type === 'daily'"/>
    <task-fulfill-subribe-content v-if="appStore.selectTaskForFulfill.type === 'referral'"/>
  </ActionModal>
</template>

<style scoped>

</style>