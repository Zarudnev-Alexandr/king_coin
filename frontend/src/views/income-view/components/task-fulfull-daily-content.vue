<script setup lang="ts">
import IncomeDailyRewardItem from "@/views/income-view/components/income-daily-reward-item.vue";
import dailyRewards from "@/shared/constants/daily-rewards.ts";
</script>

<template>
  <div class="fulfill-modal-wrap">
    <img src="@/assets/svg/income/task-modal-daily-example-avatar.png " alt="">
    <span class="card-name sf-pro-font">Ежедневная награда</span>
    <span class="fulfill-description sf-pro-font">Самый крупный telegram канал из крипто-джунглей</span>
    <div class="fulfill-reward-grid">
      <income-daily-reward-item v-for="item in dailyRewards"
                                :reward="item.reward"
                                :day="item.day"
                                :active="item.active"/>
    </div>
  </div>
</template>

<style scoped>
.fulfill-modal-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 15px;
  padding: 0 5px 10px 5px;

  .fulfill-reward-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    padding: 0 5px;
  }

  img {
    border-radius: 10px;
    width: 106px;
    height: auto;
  }

  .card-name {
    font-size: 28px;
    font-weight: 800;
    line-height: 33.41px;
    text-align: center;
    color: white;
  }

  .fulfill-description {
    font-size: 10px;
    font-weight: 400;
    line-height: 11.93px;
    text-align: center;
    color: rgba(194, 163, 117, 1);
    width: 70%;
  }


}
</style>