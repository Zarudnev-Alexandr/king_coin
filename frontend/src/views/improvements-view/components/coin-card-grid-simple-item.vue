<script setup lang="ts">
import {formatNumber} from "@/helpers/formats.ts";
import {Coin} from "@/shared/api/types/coin.ts";
import GoldCoin from "@/assets/svg/coin.svg";
import SilverCoin from "@/assets/svg/silver-coin.svg";
import {computed} from "vue";
import {useUserStore} from "@/shared/pinia/user-store.ts";
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
  <div class="coin-card-item">
    <div class="card-item-up-part">
      <div class="up-part-data">
        <span class="sf-pro-font">{{ props.cardItem.name }}</span>
        <div class="up-part-data-income">
          <span class="sf-pro-font">{{ $t('hourly_income') }}</span>
          <div class="up-part-data-income-value">
            <img :src="isMinLvl ? SilverCoin : GoldCoin" alt="">
            <span class="sf-pro-font">+ {{
                formatNumber((isMinLvl ? props.cardItem.factor_at_new_lvl : props.cardItem.factor) ?? 0)
              }}</span>
          </div>
        </div>
      </div>
      <div class="up-part-avatar">
        <img v-if="!isAvailable" src="@/assets/svg/unavailable-simple-card.svg" class="unavaliable-layer" alt="">
        <img :src="props.cardItem.image_url" alt="">
      </div>
    </div>
    <div style="width: 100%; border-top: 1px solid rgba(131, 101, 51, 1)"></div>
    <div class="card-item-down-part">
      <span class="sf-pro-font">lvl {{ props.cardItem.lvl }}</span>
      <div class="down-part-price-wrapper">
        <img :src="haveMoney ? GoldCoin : SilverCoin" alt="" v-if="props.cardItem.price_of_next_lvl && isAvailable">
        <span class="sf-pro-font" v-if="props.cardItem.price_of_next_lvl && isAvailable">
          {{ formatNumber(props.cardItem.price_of_next_lvl) }}</span>
        <span v-else>{{ isAvailable ? $t('max') : getTaskText(props.cardItem) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.coin-card-item {
  flex: 1 1 45%;
  box-sizing: border-box;
  background: rgba(57, 34, 0, 1);
  border-radius: 10px;
  display: flex;
  flex-direction: column;

  .card-item-down-part {
    display: flex;
    justify-content: space-between;
    padding: 12px 7px;

    span {
      font-size: 12px;
      font-weight: 600;
      line-height: 14.32px;
      text-align: left;
      color: rgba(238, 214, 147, 1);
    }

    .down-part-price-wrapper {
      display: flex;
      gap: 5px;

      img {
        width: 14px;
        height: 14px;
      }

      span {
        font-size: 12px;
        font-weight: 600;
        line-height: 14.32px;
        text-align: right;
        color: white;
      }
    }
  }

  .card-item-up-part {
    padding: 12px;
    display: flex;
    justify-content: space-between;

    .up-part-avatar {
      display: flex;
      justify-content: end;
      position: relative;

      .unavaliable-layer {
        position: absolute;
        right: 0;
        top: 0;
      }

      img {
        width: 53px;
      }
    }

    .up-part-data {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: start;

      span {
        font-size: 12px;
        font-weight: 600;
        line-height: 14.32px;
        text-align: left;
        color: white;

      }

      .up-part-data-income {
        display: flex;
        flex-direction: column;
        gap: 7px;

        img {
          width: 14px;
          height: 14px;
        }

        span {
          font-size: 10px;
          font-weight: 400;
          color: rgba(238, 214, 147, 1);
          overflow: hidden;
          line-height: 1.1;
          margin: 0;
          padding: 0;
          display: block;
          text-align: left;
        }

        .up-part-data-income-value {
          display: flex;
          align-items: center;
          gap: 5px;

          span {
            font-size: 12px;
            font-weight: 600;
            line-height: 14.32px;
            text-align: center;
            color: white;
          }
        }
      }
    }
  }
}
</style>