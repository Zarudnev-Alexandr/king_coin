<script setup lang="ts">

import ComboCardItem from "@/views/improvements-view/components/combo-card-item.vue";
import CardComboUnboxItem from "@/views/improvements-view/components/card-combo-unbox-item.vue";
</script>

<template>
  <div class="combo-wrapper">
    <div class="combo-indicator">
      <span class="sf-pro-font combo-indicator-title">Дневное комбо</span>
      <div class="combo-indicator-icons">
        <span class="combo-indicator-icon-item active"></span>
        <span class="combo-indicator-icon-item"></span>
        <span class="combo-indicator-icon-item"></span>
      </div>
      <div class="get-combo-button">
        <img src="@/assets/svg/coin.svg" alt="">
        <span class="sf-pro-font">+ 5 000 000</span>
      </div>
    </div>

    <div class="combo-list">
      <ComboCardItem title="BadCoin"/>
      <card-combo-unbox-item/>
      <card-combo-unbox-item/>
    </div>
  </div>
</template>

<style scoped>
.combo-wrapper {
  display: flex;
  flex-direction: column;
  padding: 0 16px;
  gap: 20px;

  .combo-list {
    display: flex;
    gap: 8px;
  }

  .combo-indicator {
    background-color: rgba(57, 34, 0, 1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    border-radius: 10px;
    box-sizing: border-box;
    padding: 4px;

    .combo-indicator-icons {
      display: flex;
      justify-content: center;
      gap: 8px;

      .combo-indicator-icon-item {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: rgba(93, 56, 0, 1);
      }

      .active {
        background: linear-gradient(90deg, #FF8200 0%, #FFC800 100%);
      }
    }

    .get-combo-button {
      padding: 8px 7px;
      border-radius: 9px;
      background: linear-gradient(90deg, #FF8200 0%, #FFC800 100%);
      display: flex;
      align-items: center;
      gap: 4px;

      img {
        width: 16.5px;
        height: 16.5px;
      }

      span {
        font-size: 12px;
        font-weight: 700;
        line-height: 14.32px;
        text-align: right;
        color: white;
      }
    }

    .combo-indicator-title {
      font-size: 12px;
      font-weight: 600;
      line-height: 14.32px;
      text-align: left;
      padding-left: 15px;
      color: white;
    }
  }
}
</style>