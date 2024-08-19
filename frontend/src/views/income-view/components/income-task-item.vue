<script setup lang="ts">
import CoinCountItem from "@/views/friends-view/components/coin-count-item.vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import Task from "@/shared/api/types/task.ts";

interface Props {
  taskItem: Task;
  customHandle?: () => void;
}

const appStore = useAppStore();
const props: Props = defineProps<Props>();

const handleClick = () => {
  if (props.customHandle) {
    props.customHandle();
    return;
  }

  if (props.taskItem.type === 'invite') {
    return;
  }
  appStore.setSelectTaskForFulfill(props.taskItem);
}
</script>

<template>
  <div class="task-item-wrapper" @click="handleClick">
    <div class="task-item-avatar">
      <img src="@/assets/svg/income/task-item-avatar-example.png" alt="" class="task-avatar">
      <img src="@/assets/svg/income/task-is-done-icon.png" alt="" class="is-done-icon" v-if="props.taskItem.completed">
    </div>
    <h2 class="sf-pro-font">{{ props.taskItem.name }}</h2>
    <CoinCountItem :count="props.taskItem.reward" format-number="withSpace"/>
  </div>
</template>

<style scoped>
.task-item-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 9px 12px;
  background-color: rgba(93, 56, 0, 1);
  gap: 15px;
  border-radius: 10px;

  h2 {
    flex: 1;
    font-size: 12px;
    font-weight: 600;
    line-height: 14.32px;
    text-align: left;
    color: white;
  }

  .task-item-avatar {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;

    .task-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
    }

    .is-done-icon {
      width: 20px;
      height: 20px;
      position: absolute;
      top: 0;
      right: -5px;
    }
  }
}
</style>