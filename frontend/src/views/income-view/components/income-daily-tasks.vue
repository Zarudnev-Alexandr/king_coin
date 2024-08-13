<script setup lang="ts">
import {computed, ref, watch} from 'vue';
import IncomeTaskItem from "@/views/income-view/components/income-task-item.vue";
import Task from "@/shared/api/types/task.ts";
import {useIncomeStore} from "@/shared/pinia/income-store.ts";
import dailyRewards from "@/shared/constants/daily-rewards.ts";
import {useI18n} from "vue-i18n";

const incomeStore = useIncomeStore();
const {t} = useI18n();

const getCurrentDailyReward = computed(() => {
  const reward = dailyRewards.find((reward) => incomeStore.dailyTask?.day === reward.day);
  return reward ? reward.reward : 0;
});

const getCurrentDailyIsCollect = computed(() => {
  return incomeStore.dailyTask?.is_collect ?? false;
});

const task = ref<Task>({
  name: t('daily_reward'),
  description: t('largest_telegram_channel'),
  type: "daily",
  reward: getCurrentDailyReward.value,
  requirement: 4,
  link: null,
  id: 0,
  completed: getCurrentDailyIsCollect.value,
  end_time: null,
});

watch(getCurrentDailyReward, (newReward) => {
  task.value.reward = newReward;
});

watch(getCurrentDailyIsCollect, (newIsCollect) => {
  task.value.completed = newIsCollect;
});


</script>

<template>
  <div class="daily-tasks-wrap">
    <h3 class="sf-pro-font">{{ $t('daily_tasks') }}</h3>
    <div class="task-list-wrap">
      <IncomeTaskItem :task-item="task"/>
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
