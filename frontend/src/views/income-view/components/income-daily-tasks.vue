<script setup lang="ts">
import IncomeTaskItem from "@/views/income-view/components/income-task-item.vue";

interface Props {
  taskList: {
    reward: number,
    title: string,
    type: string,
    isDone: boolean,
  }[]
}

const props: Props = defineProps<Props>();
</script>

<template>
  <div class="daily-tasks-wrap">
    <h3 class="sf-pro-font">Ежедневные задания</h3>
    <div class="task-list-wrap">
      <IncomeTaskItem v-for="(task, index) in props.taskList" :key="index" :task-item="task"/>
    </div>
  </div>
</template>

<style scoped>
.daily-tasks-wrap {
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