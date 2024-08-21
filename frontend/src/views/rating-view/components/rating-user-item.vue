<script setup lang="ts">
import {Levels} from "@/shared/constants/levels.ts";
import {formatNumberWithSpaces} from "@/helpers/formats.ts";
import CoinIcon from "@/assets/svg/coin.svg";
import ColumnIcon from "@/assets/svg/column-icon.svg";
import RatingUser from "@/shared/api/types/rating-user-item.ts";

interface Props {
  item: RatingUser,
  activeTab: string,
}

const {item, activeTab} = defineProps<Props>();
</script>

<template>
  <div class="rating-user-item-wrap">
    <img :src="Levels[0].image" alt="">
    <div class="name-lvl-wrap">
      <span class="name sf-pro-font">{{ item.fio }}</span>
      <div class="lvl-wrap">
        <img src="@/assets/svg/friends/friend-grandmaster-league-icon.png" alt="">
        <span class="lvl sf-pro-font">{{ Levels[0].name }}</span>
      </div>
    </div>
    <div style="flex: 1"/>
    <div class="rating-item-profit-wrap">
      <div class="coin-count-wrap">
        <img :src="activeTab === 'coins' ? CoinIcon : ColumnIcon" alt="">
        <span class="sf-pro-font"> {{
            formatNumberWithSpaces(activeTab === 'coins' ? item.money : item.columns_passed)
          }}</span>
      </div>
      <div class="rating-invite-count-wrap">
        <img src="@/assets/svg/friends/friend-group-icon.png" alt="">
        <span class="sf-pro-font"> {{ item.rank }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rating-user-item-wrap {
  width: 100%;
  display: flex;
  padding: 9px 12px;
  align-items: center;
  gap: 10px;
  border-radius: 10px;
  box-sizing: border-box;
  background-color: rgba(93, 56, 0, 1);

  img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }

  .rating-item-profit-wrap {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-end;
    gap: 5px;

    .coin-count-wrap {
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

    .rating-invite-count-wrap {
      display: flex;
      align-items: center;
      gap: 3px;

      img {
        width: 10px;
        height: 10px;
      }

      span {
        font-size: 10px;
        font-weight: 400;
        line-height: 11.93px;
        text-align: right;
        color: rgba(238, 214, 147, 1);
      }
    }
  }

  .name-lvl-wrap {
    display: flex;
    flex-direction: column;
    gap: 5px;

    .name {
      font-size: 12px;
      font-weight: 600;
      line-height: 17.38px;
      text-align: left;
      color: white;
    }

    .lvl-wrap {
      display: flex;
      align-items: center;
      gap: 5px;

      .lvl {
        font-size: 9px;
        font-weight: 400;
        line-height: 13.03px;
        text-align: left;
        color: rgba(238, 214, 147, 1);
      }


      img {
        width: 6.28px;
        height: 8.05px;
      }
    }
  }
}
</style>