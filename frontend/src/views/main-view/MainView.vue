<script setup lang="ts">

import LevelIndicator from "@/views/main-view/components/level-indicator.vue";
import AppIconButton from "@/components/AppIconButton.vue";
import HeaderStatisticItem from "@/views/main-view/components/header-statistic-item.vue";
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
              <span>90 000 000</span>
            </div>
            <div class="header-data-statistic">
              <header-statistic-item title="Множитель" value="1,3"/>
              <header-statistic-item title="До lvl-апа" value="100k"/>
              <header-statistic-item title="Доход в час" value="100k"/>
            </div>
          </div>
        </div>
      </div>
      <div class="bottom-data">
        <div class="bottom-data-actions">
          <AppIconButton style="width: 48px; height: 48px;">
            <img src="@/assets/svg/settings-icon.svg" alt="">
          </AppIconButton>
          <AppIconButton style="width: 48px; height: 48px;">
            <img src="@/assets/svg/boost-icon.svg" alt="">
          </AppIconButton>
        </div>
        <div class="current-level-wrapper">
          <span class="text-lvl sf-pro-font">Lvl: </span>
          <span class="app-text-gradient text-current-level sf-pro-font">15</span>
          <img src="@/assets/svg/right-arrow.svg" alt="">
          <level-indicator :level="15" style="flex: 1"/>
        </div>
        <div style="height: 65px;"/>
      </div>
    </div>
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