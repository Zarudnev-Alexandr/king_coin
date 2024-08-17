<script setup lang="ts">
import {formatNumber} from "@/helpers/formats.ts";
import {Coin} from "@/shared/api/types/coin.ts";
import {computed} from "vue";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import GoldCoin from "@/assets/svg/coin.svg";
import SilverCoin from "@/assets/svg/silver-coin.svg";
import {checkIsAvailable, getTaskText} from "@/helpers/coin.ts";

interface Props {
  cardItem: Coin
}

const userStore = useUserStore();
const props: Props = defineProps<Props>();

const haveMoney = computed(() => {
  return (props.cardItem.price_of_next_lvl ?? 0) <= (userStore.user?.money ?? 0)
});

const isMinLvl = computed(() => {
  return props.cardItem.lvl === 0;
});

const isAvailable = computed(() => {
  return checkIsAvailable(props.cardItem);
})
</script>

<template>
  <div class="coin-special-card-item-wrapper">
    <div class="bg-img">
      <img v-if="!isAvailable" src="@/assets/svg/unavailable-special-card.svg" class="unavailable-layer" alt="">
      <img :src="props.cardItem.image_url" alt="">
      <div class="coin-special-card-gradient"/>
    </div>
    <div class="coin-special-card-data">
      <span class="text-style-white">{{ props.cardItem.name }}</span>
      <p class="sf-pro-font">{{ $t('hourly_income') }}</p>
      <div class="coin-special-card-income">
        <img class="coin-img" :src="isMinLvl ? SilverCoin : GoldCoin" alt="">
        <span class="text-style-white">{{
            formatNumber((isMinLvl ? props.cardItem.factor_at_new_lvl : props.cardItem.factor) ?? 0)
          }}</span>
      </div>
    </div>
    <div style="width: 100%; border-top: 1px solid rgba(131, 101, 51, 1)"></div>
    <div class="card-item-down-part">
      <span class="text-style-white" style="color: rgba(238, 214, 147, 1)!important;">lvl {{
          props.cardItem.lvl
        }}</span>
      <div class="down-part-price-wrapper">
        <img class="coin-img" :src="haveMoney ? GoldCoin : SilverCoin"
             v-if="props.cardItem.price_of_next_lvl && isAvailable" alt="">
        <span class="text-style-white" v-if="props.cardItem.price_of_next_lvl && isAvailable">
          {{ formatNumber(props.cardItem.price_of_next_lvl ?? 0) }}</span>
        <span v-else class="lvl-max sf-pro-font">{{ isAvailable ? $t('max') : getTaskText(props.cardItem) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.coin-special-card-item-wrapper {
  background-color: rgba(57, 34, 0, 1);
  border-radius: 10px;
  min-height: 204px;
  flex: 1 1 45%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  position: relative;

  .bg-img {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 0;

    .unavailable-layer {
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
      width: 100%;
    }

    img {
      width: 100%;
      object-fit: cover;
      border-radius: 10px;
    }

    .coin-special-card-gradient {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 66px;
      z-index: 1;
      background: linear-gradient(180deg, rgba(57, 34, 0, 0) 0%, #392200 100%);
    }
  }

  .coin-special-card-data {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 10px 0;
    gap: 5px;
    position: relative;
    z-index: 5;

    .coin-special-card-income {
      display: flex;
      justify-content: center;
      gap: 5px;
    }

    p {
      font-size: 10px;
      font-weight: 400;
      line-height: 11.93px;
      text-align: center;
      color: rgba(238, 214, 147, 1);
      margin: 0;
    }
  }

  .card-item-down-part {
    display: flex;
    justify-content: space-between;
    padding: 5px 12px 10px 12px;

    .down-part-price-wrapper {
      display: flex;
      gap: 5px;

      .lvl-max {
        font-size: 12px;
        font-weight: 600;
        line-height: 14.32px;
        text-align: right;
        color: white;
      }
    }
  }
}

.coin-img {
  width: 14px;
  height: 14px;
}

.text-style-white {
  font-family: 'SF Pro Text', sans-serif;
  font-size: 12px;
  font-weight: 600;
  line-height: 14.32px;
  text-align: right;
  color: white;
}
</style>