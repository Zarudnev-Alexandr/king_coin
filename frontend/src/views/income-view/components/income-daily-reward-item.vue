<script setup lang="ts">
import {formatNumberWithSpaces} from "@/helpers/formats.ts";
import {useIncomeStore} from "@/shared/pinia/income-store.ts";
import CoinImg from "@/assets/svg/coin.svg";
import TaskDoneIcon from "@/assets/svg/income/task-is-done-icon.png"

interface Props {
  day: number,
  reward: number,
  active: boolean
}

const props: Props = defineProps<Props>();
const {dailyTask} = useIncomeStore();

const checkIsActive = () => {
  if (dailyTask?.day === props.day) {
    return dailyTask.is_collect;
  }
  return props.day < (dailyTask?.day ?? 0);
}

const getIcon = () => {
  if (checkIsActive()) {
    return TaskDoneIcon;
  }
  return CoinImg;
}
</script>

<template>
  <div class="daily-reward-item-wrap"
       :class="{'active': checkIsActive(), 'opacity50': props.day > (dailyTask?.day ?? 0)}">
    <img :src="getIcon()" alt="">
    <span class="daily-reward-day sf-pro-font">День {{ props.day }}</span>
    <span class="daily-reward-reward sf-pro-font">{{ formatNumberWithSpaces(props.reward) }}</span>
  </div>
</template>

<style scoped>
.daily-reward-item-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 4px 0;
  width: calc(25% - 5px);
  gap: 5px;
  background: rgba(93, 56, 0, 1);
  border-radius: 10px;
  box-sizing: border-box;

  img {
    width: 20px;
    height: 20px;
  }

  .daily-reward-day {
    font-size: 10px;
    font-weight: 400;
    line-height: 11.93px;
    text-align: center;
    color: white;
  }

  .daily-reward-reward {
    font-size: 12px;
    font-weight: 600;
    line-height: 14.32px;
    text-align: center;
    color: white;
  }
}

.opacity50 {
  opacity: 0.5;
}

.active {
  background: linear-gradient(90deg, #FF8200 0%, #FFC800 100%) !important;
}
</style>