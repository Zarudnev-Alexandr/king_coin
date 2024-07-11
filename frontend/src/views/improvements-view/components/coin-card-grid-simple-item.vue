<script setup lang="ts">
import {formatNumber} from "@/helpers/formats.ts";

interface Props {
  cardItem: any
}

const props: Props = defineProps<Props>();
</script>

<template>
  <div class="coin-card-item">
    <div class="card-item-up-part">
      <div class="up-part-data">
        <span class="sf-pro-font">{{ props.cardItem.name }}</span>
        <div class="up-part-data-income">
          <span class="sf-pro-font">Множитель</span>
          <div class="up-part-data-income-value">
            <img src="@/assets/svg/coin.svg" alt="">
            <span class="sf-pro-font">+ {{ formatNumber(props.cardItem.income) }}</span>
          </div>
        </div>
      </div>
      <div class="up-part-icon">
        <img src="@/assets/img/impro-card-icon.png" alt="">
      </div>
    </div>
    <div style="width: 100%; border-top: 1px solid rgba(131, 101, 51, 1)"></div>
    <div class="card-item-down-part">
      <span class="sf-pro-font">lvl {{ props.cardItem.level }}</span>
      <div class="down-part-price-wrapper">
        <img src="@/assets/svg/coin.svg" alt="">
        <span class="sf-pro-font">{{ formatNumber(props.cardItem.price) }}</span>
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
        img {
          width: 14px;
          height: 14px;
        }

        span {
          font-size: 10px;
          font-weight: 400;
          line-height: 11.93px;
          text-align: center;
          color: rgba(238, 214, 147, 1);
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