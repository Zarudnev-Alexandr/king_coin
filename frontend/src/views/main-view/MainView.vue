<script setup lang="ts">

import LevelIndicator from "@/views/main-view/components/level-indicator.vue";
import AppIconButton from "@/components/AppIconButton.vue";
import HeaderStatisticItem from "@/views/main-view/components/header-statistic-item.vue";
import {useRouter} from "vue-router";
import ActionModal from "@/components/ActionModal.vue";
import {ref} from "vue";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import {formatNumberWithSpaces} from "@/helpers/formats.ts";

const router = useRouter();
const visibleBoostModal = ref(false);
const userStore = useUserStore();
const user = userStore.user;

const gotoRatingView = () => {
  router.push({name: 'Rating'});
}
</script>

<template>
  <div class="main-view-wrapper">
    <div class="main-monkey"/>
    <div class="main-view-content">
      <div class="header-data">
        <div class="header-data-scoreboard">
          <div class="header-data-content">
            <div class="header-data-score-count">
              <img src="@/assets/svg/coin.svg" alt="">
              <span>{{ formatNumberWithSpaces(userStore.user?.money ?? 0) }}</span>
            </div>
            <div class="header-data-statistic">
              <header-statistic-item title="Доход за тап" :value="user?.boost.one_tap.toString() ?? ''"/>
              <header-statistic-item title="До lvl-апа" value="100k"/>
              <header-statistic-item title="Доход в час" :value="user!.earnings_per_hour.toString() ?? ''"/>
            </div>
          </div>
        </div>
      </div>
      <div class="bottom-data">
        <div class="bottom-data-actions">
          <AppIconButton style="width: 48px; height: 48px;" @on-click="gotoRatingView">
            <img src="@/assets/svg/rating-icon.svg" alt="">
          </AppIconButton>
          <AppIconButton style="width: 48px; height: 48px;">
            <img src="@/assets/svg/settings-icon.svg" alt="">
          </AppIconButton>
          <AppIconButton style="width: 48px; height: 48px;" @on-click="() => visibleBoostModal = true">
            <img src="@/assets/svg/boost-icon.svg" alt="">
          </AppIconButton>
        </div>
        <div class="current-level-wrapper">
          <span class="text-lvl sf-pro-font">Lvl: </span>
          <span class="app-text-gradient text-current-level sf-pro-font">{{ user?.boost.lvl }}</span>
          <img src="@/assets/svg/right-arrow.svg" alt="">
          <level-indicator :level="15" style="flex: 1"/>
        </div>
        <div style="height: 65px;"/>
      </div>
    </div>
    <action-modal v-if="visibleBoostModal" @close="() => visibleBoostModal = false" @on-accept="() => visibleBoostModal = false">
      <div class="boost-modal-wrapper">
        <div style="height: 30px"/>
        <img src="@/assets/img/boost-icon.png" alt="">
        <span class="boost-modal-title sf-pro-font">Усилитель</span>
        <span class="boost-description sf-pro-font">
          Увеличивает количество монет, которое вы можете заработать за одно нажатие
        </span>
        <span class="boost-description sf-pro-font">Уровень 1</span>
        <div class="boost-reward">
          <img src="@/assets/svg/coin.svg" alt="">
          <span class="sf-pro-font">+ 1 монета за тап</span>
        </div>
        <div class="boost-price">
          <img src="@/assets/svg/coin.svg" alt="">
          <span class="sf-pro-font">310 110</span>
        </div>
      </div>
    </action-modal>
  </div>
</template>

<style scoped>
.main-view-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/img/main-view-bg.png');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  position: relative;

  .boost-modal-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px 0;
    gap: 15px;

    img {
      width: 130px;
      height: 130px;
      transform: rotate(7deg);
    }

    .boost-modal-title {
      font-size: 25px;
      font-weight: 700;
      line-height: 29.83px;
      text-align: center;
      color: white;
    }

    .boost-description {
      font-size: 10px;
      font-weight: 400;
      line-height: 11.93px;
      text-align: center;
      color: rgba(194, 163, 117, 1);
      width: 65%;
    }

    .boost-reward {
      display: flex;
      justify-content: center;
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
        text-align: center;
        color: white;
      }
    }

    .boost-price {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 10px;

      img {
        width: 30px;
        height: 30px;
      }

      span {
        font-size: 28px;
        font-weight: 800;
        line-height: 33.41px;
        text-align: left;
        color: white;
      }
    }
  }

  .main-view-content {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;

    .header-data {
      background: linear-gradient(180deg, #000000 0%, rgba(0, 0, 0, 0) 58.43%);
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      box-sizing: border-box;
      padding-bottom: 50px;

      .header-data-scoreboard {
        background-image: url("@/assets/svg/header-scoreboard.svg");
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 50px 0 90px 0;
        opacity: 0;
        transform: translateY(-50px);
        animation: slideIn 0.5s ease-in-out forwards;

        .header-data-content {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        .header-data-statistic {
          display: flex;
          gap: 20px;
        }

        .header-data-score-count {
          display: flex;
          justify-content: center;
          gap: 8px;

          img {
            width: 48px;
            height: 49px;
          }

          span {
            font-family: 'SuperSquadRus', sans-serif;
            font-size: 34px;
            font-weight: 400;
            line-height: 46.32px;
            text-align: left;
            color: white;
            display: flex;
            text-shadow: -3px 3px 0 rgba(57, 34, 0, 1),
            3px 3px 0 rgba(57, 34, 0, 1),
            3px -3px 0 rgba(57, 34, 0, 1),
            -3px -3px 0 rgba(57, 34, 0, 1);
          }
        }
      }
    }

    .bottom-data {
      display: flex;
      flex-direction: column;
      padding: 0 10px;
      background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, #000000 58.43%);

      .current-level-wrapper {
        display: flex;
        align-items: center;
        padding: 20px 0;
        gap: 5px;

        .text-lvl {
          font-size: 15px;
          font-weight: 600;
          line-height: 17.9px;
          text-align: center;
          color: white;
        }

        .text-current-level {
          font-size: 15px;
          font-weight: 600;
          line-height: 17.9px;
          text-align: center;
        }
      }

      .bottom-data-actions {
        display: flex;
        flex-direction: column;
        align-items: end;
        gap: 20px;
      }
    }
  }

  .main-monkey {
    width: 100%;
    height: 85%;
    background-image: url('@/assets/img/main-view-monkey.png');
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    position: absolute;
    bottom: 0;
    right: 50%;
    transform: translateX(50%);
    z-index: 5;
  }
}

@keyframes slideIn {
  to {
    opacity: 1; /* Конечная прозрачность */
    transform: translateY(0); /* Конечное смещение */
  }
}
</style>