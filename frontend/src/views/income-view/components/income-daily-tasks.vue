<script setup lang="ts">
import IncomeTaskItem from "@/views/income-view/components/income-task-item.vue";
import Task from "@/shared/api/types/task.ts";

const task = {
  name: "Ежедневная награда",
  description: "Самый крупный telegram канал из крипто-джунглей",
  type: "daily",
  reward: 30000,
  requirement: 4,
  link: null,
  id: 0,
  completed: false,
} as Task;

</script>

<template>
  <div class="daily-tasks-wrap">
    <h3 class="sf-pro-font">Ежедневные задания</h3>
    <div class="task-list-wrap">
      <IncomeTaskItem :task-item="task as Task"/>
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