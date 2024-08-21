<script setup lang="ts">

import RatingHeader from "@/views/rating-view/components/RatingHeader.vue";
import {onMounted, ref, Ref} from "vue";
import RatingSkeleton from "@/views/main-view/components/rating-skeleton.vue";
import RatingApiService from "@/shared/api/services/rating-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import RatingUserItem from "@/views/rating-view/components/rating-user-item.vue";
import LeaderboardRes from "@/shared/api/types/leaderboard-res.ts";

const activeTab: Ref<string> = ref('coins');
const isLoadingColumns = ref(false);
const isLoadingCoin = ref(false);
const ratingApiService = new RatingApiService(axiosInstance, errorHandler);
const coinLeaders: Ref<LeaderboardRes | null> = ref(null);
const columnLeaders: Ref<LeaderboardRes | null> = ref(null);

const changeTab = (tab: string, _: any[]) => {
  activeTab.value = tab;
}

onMounted(() => {
  isLoadingColumns.value = true;
  isLoadingCoin.value = true;

  ratingApiService.getRatings('columns').then((res) => {
    if (res.right) {
      columnLeaders.value = res.right;
    }

    isLoadingColumns.value = false;
  })

  ratingApiService.getRatings('money').then((res) => {
    if (res.right) {
      coinLeaders.value = res.right;
    }

    isLoadingCoin.value = false;
  });
})
</script>

<template>
  <div class="rating-view-wrapper">
    <RatingHeader/>
    <div class="rating-content-wrap"
         v-if="(coinLeaders?.leaderboard.length ?? 0) > 0 && (columnLeaders?.leaderboard.length ?? 0) > 0">
      <div class="rating-tab-wrapper">
        <div class="rating-list-tab">
          <div class="rating-list-tab-item"
               :class="{'active': activeTab === 'coins'}"
               @click="() => changeTab('coins', [])">
            <span>{{ $t('coins') }}</span>
          </div>
          <div class="rating-list-tab-item"
               :class="{'active': activeTab === 'columns'}"
               @click="() => changeTab('columns', [])">
            <span>{{ $t('columns') }}</span>
          </div>
          <div class="rating-list-tab-item"
               :class="{'active': activeTab === 'income'}">
            <span>{{ $t('soon') }}</span>
          </div>
        </div>
      </div>

      <div class="rating-list-wrap">
        <rating-user-item v-if="activeTab === 'coins'" :item="coinLeaders!.current_user" :activeTab="activeTab"/>
        <rating-user-item v-if="activeTab === 'columns'" :item="columnLeaders!.current_user" :activeTab="activeTab"/>

        <div class="rating-list">
          <div style="height: 40px"/>
          <div class="img-wrap">
            <img src="@/assets/svg/rating-top-100.svg" alt="">
          </div>

          <div v-if="activeTab === 'coins'" style="display: flex; flex-direction: column; gap: 10px">
            <rating-user-item
                v-for="item in coinLeaders!.leaderboard"
                :item="item"
                :active-tab="activeTab"/>
          </div>

          <div v-if="activeTab === 'columns'" style="display: flex; flex-direction: column; gap: 10px">
            <rating-user-item
                v-for="item in columnLeaders!.leaderboard"
                :item="item"
                :active-tab="activeTab"/>
          </div>

        </div>
      </div>


    </div>

    <rating-skeleton v-else/>
    <h2/>
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

  .rating-content-wrap {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .rating-list-wrap {
      display: flex;
      flex-direction: column;
      gap: 10px;
      padding: 0 15px;

      .rating-list {
        border-radius: 10px;
        background-color: rgba(57, 34, 0, 1);
        padding: 20px 10px;
        display: flex;
        flex-direction: column;
        position: relative;
        gap: 10px;

        .img-wrap {
          position: absolute;
          top: -20px;
          left: 0;
          width: 100%;
          display: flex;
          justify-content: center;

          img {
            width: 232px;
          }
        }
      }
    }
  }

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