<script setup lang="ts">
import {computed, Ref, ref, UnwrapRef} from "vue";
import CoinCardGrid from "@/views/improvements-view/components/coin-card-grid.vue";
import {useImprovementsStore} from "@/shared/pinia/improvements-store.ts";

const activeTab: Ref<UnwrapRef<string>> = ref('Crypto');
const improvementsStore = useImprovementsStore();

const currentCardList = computed(() => {
  if (activeTab.value === 'Crypto') {
    return improvementsStore.cryptoCoinList;
  } else if (activeTab.value === 'Action') {
    return improvementsStore.actionCoinList;
  } else if (activeTab.value === 'Special') {
    return improvementsStore.specialCoinList;
  }
});

const changeTab = (tab: string) => {
  activeTab.value = tab;
}
</script>

<template>
  <div class="coin-card-list">
    <div class="coin-card-list-tab">
      <div class="coin-card-list-tab-item"
           :class="{'active': activeTab === 'Crypto'}"
           @click="() => changeTab('Crypto')">
        <span>Crypto</span>
      </div>
      <div class="coin-card-list-tab-item"
           :class="{'active': activeTab === 'Action'}"
           @click="() => changeTab('Action')">
        <span>Action</span>
      </div>
      <div class="coin-card-list-tab-item"
           :class="{'active': activeTab === 'Special'}"
           @click="() => changeTab('Special')">
        <span>Special</span>
      </div>
      <div class="coin-card-list-tab-item">
        <span>Soon</span>
      </div>
    </div>
    <coin-card-grid v-if="currentCardList" :card-list="currentCardList" :current-tab="activeTab"/>
  </div>
</template>

<style scoped>
.coin-card-list {
  display: flex;
  padding: 0 16px;
  flex-direction: column;
  gap: 15px;

  .coin-card-list-tab {
    display: flex;
    border-radius: 10px;
    background-color: rgba(57, 34, 0, 1);
    padding: 5px;

    .coin-card-list-tab-item {
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