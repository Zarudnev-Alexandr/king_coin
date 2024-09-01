<script setup lang="ts">
import {computed, Ref, ref, watch} from 'vue';
import IncomeTaskItem from "@/views/income-view/components/income-task-item.vue";
import Task from "@/shared/api/types/task.ts";
import {useIncomeStore} from "@/shared/pinia/income-store.ts";
import dailyRewards from "@/shared/constants/daily-rewards.ts";
import {useI18n} from "vue-i18n";
import {ShowPromiseResult} from "@/shared/api/types/adsgram";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import TasksApiService from "@/shared/api/services/tasks-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import AdTaskAvatar from "@/assets/svg/income/ad-task-avatar.webp";
import DailyTaskAvatar from "@/assets/svg/income/daily-task-avatar.svg";

const incomeStore = useIncomeStore();
const appStore = useAppStore();
const tasksApiService = new TasksApiService(axiosInstance, errorHandler)
const userStore = useUserStore();
const AdController = window.Adsgram?.init({blockId: "2584"});
const {t} = useI18n();

const getCurrentDailyReward = computed(() => {
  const reward = dailyRewards.find((reward) => incomeStore.dailyTask?.day === reward.day);
  return reward ? reward.reward : 0;
});

const getCurrentDailyIsCollect = computed(() => {
  return incomeStore.dailyTask?.is_collect ?? false;
});

const getWatchedAdsCount = computed(() => {
  return incomeStore.dailyTask?.ads_watched_today ?? 0;
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
  image_url: DailyTaskAvatar,
  end_time: null,
});

const adTask: Ref<Task> = ref({
  name: t('watch_an_ad', {count: incomeStore.dailyTask?.ads_watched_today ?? 0}),
  description: "Посмотрите рекламу и получите 3 монеты",
  type: "ad",
  reward: incomeStore.dailyTask?.ads_reward ?? 0,
  requirement: 3,
  link: null,
  id: 1,
  completed: getWatchedAdsCount.value >= 3,
  end_time: null,
  image_url: AdTaskAvatar
});

const handleDailyAd = async () => {
  if (getWatchedAdsCount.value >= 3) return;

  AdController?.show().then(async (result: ShowPromiseResult) => {
    if (!result.done) return;

    const res = await tasksApiService.confirmWatchedAd();
    if (res && res.right && incomeStore.dailyTask) {
      userStore.moneyPlus(adTask.value.reward);
      incomeStore.dailyTask.ads_watched_today += 1;
      adTask.value.name = t('watch_an_ad', {count: incomeStore.dailyTask?.ads_watched_today ?? 0});
      adTask.value.completed = incomeStore.dailyTask.ads_watched_today >= 3;
      userStore.vibrationService.medium();
      appStore.playCoinAnimation();
    }

  }).catch((result: ShowPromiseResult) => {
    console.log(result);
  })
}

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
      <income-task-item :task-item="adTask" :custom-handle="handleDailyAd"/>
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
