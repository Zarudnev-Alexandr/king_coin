<script setup lang="ts">

import LevelsHeader from "@/views/levels-view/components/levels-header.vue";
import {Levels} from "@/shared/constants/levels.ts";
import {formatNumberWithSpaces} from "@/helpers/formats.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";

const userStore = useUserStore();
</script>

<template>
  <div class="levels-view-wrapper">
    <levels-header/>
    <div class="levels-list-wrapper">
      <div v-for="item in Levels" class="level-item-wrapper" :class="{active: item.lvl === userStore.user?.user_lvl}">
        <img :src="item.image" alt="">
        <div class="level-item-info">
          <span class="item-info-name sf-pro-font">{{ item.name }}</span>
          <span class="item-info-level sf-pro-font">lvl {{ item.lvl }}</span>
        </div>
        <div style="flex: 1"></div>
        <div class="level-item-reward">
          <img src="@/assets/svg/coin.svg" alt="">
          <span>{{ formatNumberWithSpaces(item.reward) }} +</span>
        </div>
      </div>
    </div>
    <h1></h1>
  </div>
</template>

<style scoped>
.levels-view-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  margin: 0 auto;
  background-image: url('@/assets/img/app-bg.png');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  overflow-y: auto;
  gap: 10px;

  .levels-list-wrapper {
    display: flex;
    flex-direction: column;
    background-color: rgba(57, 34, 0, 1);
    margin: 5px 15px;
    border-radius: 10px;
    padding: 20px 10px;
    gap: 10px;

    .level-item-wrapper {
      background-color: rgba(93, 56, 0, 1);
      padding: 9px 12px;
      display: flex;
      align-items: center;
      border-radius: 10px;
      gap: 12px;

      img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
      }

      .level-item-reward {
        display: flex;
        align-items: center;
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

      .level-item-info {
        display: flex;
        flex-direction: column;
        gap: 5px;

        .item-info-name {
          font-size: 12px;
          font-weight: 600;
          line-height: 14.32px;
          text-align: left;
          color: white;
        }

        .item-info-level {
          font-size: 10px;
          font-weight: 400;
          line-height: 11.93px;
          text-align: left;
          color: rgba(238, 214, 147, 1);
        }
      }
    }
  }

  .active {
    background: linear-gradient(90deg, #FF8200 0%, #FFC800 100%);

    .item-info-level {
      color: white !important;
    }
  }
}
</style>