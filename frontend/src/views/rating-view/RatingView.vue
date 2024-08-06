<script setup lang="ts">

import RatingHeader from "@/views/rating-view/components/RatingHeader.vue";
import {ref, Ref, UnwrapRef} from "vue";

const activeTab: Ref<UnwrapRef<string>> = ref('coins');

const changeTab = (tab: string, _: any[]) => {
  activeTab.value = tab;
}
</script>

<template>
  <div class="rating-view-wrapper">
    <RatingHeader/>
    <div class="rating-tab-wrapper">
      <div class="rating-list-tab">
        <div class="rating-list-tab-item"
             :class="{'active': activeTab === 'coins'}"
             @click="() => changeTab('coins', [])">
          <span>Монеты</span>
        </div>
        <div class="rating-list-tab-item"
             :class="{'active': activeTab === 'columns'}"
             @click="() => changeTab('columns', [])">
          <span>Колонны</span>
        </div>
        <div class="rating-list-tab-item"
             :class="{'active': activeTab === 'income'}"
             @click="() => changeTab('income', [])">
          <span>Доход в час</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rating-view-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/img/app-bg.webp');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  overflow-y: auto;
  gap: 30px;

  .rating-tab-wrapper {
    display: flex;
    padding: 0 16px;
    flex-direction: column;
    gap: 15px;
  }

  .rating-list-tab {
    display: flex;
    border-radius: 10px;
    background-color: rgba(57, 34, 0, 1);
    padding: 5px;

    .rating-list-tab-item {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 12px 24px;
      border-radius: 8px;
      flex: 1;

      span {
        font-family: 'SFProText', sans-serif;
        font-size: 10px;
        font-weight: 400;
        line-height: 11.93px;
        text-align: center;
        color: white;
      }
    }

    .active {
      background-color: rgba(93, 56, 0, 1);
    }
  }
}
</style>