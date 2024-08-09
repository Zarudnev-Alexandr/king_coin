<script setup lang="ts">

import LevelIndicator from "@/views/main-view/components/level-indicator.vue";
import AppIconButton from "@/components/AppIconButton.vue";
import HeaderStatisticItem from "@/views/main-view/components/header-statistic-item.vue";
import {useRouter} from "vue-router";
import ActionModal from "@/components/ActionModal.vue";
import {computed, onMounted, ref} from "vue";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import {formatNumber, formatNumberWithSpaces} from "@/helpers/formats.ts";
import Level1Image from "@/assets/img/level/character-1.webp"
import Level2Image from "@/assets/img/level/character-2.webp"
import Level3Image from "@/assets/img/level/character-3.webp"
import Level4Image from "@/assets/img/level/character-4.webp"
import Level5Image from "@/assets/img/level/character-5.webp"
import Level6Image from "@/assets/img/level/character-6.webp"
import Level7Image from "@/assets/img/level/character-7.webp"
import Level8Image from "@/assets/img/level/character-8.webp"
import Level9Image from "@/assets/img/level/character-9.webp"
import Level10Image from "@/assets/img/level/character-10.webp"
import BoostApiService from "@/shared/api/services/boost-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import ModalActionButton from "@/components/ModalActionButton.vue";

const router = useRouter();
const visibleBoostModal = ref(false);
const userStore = useUserStore();
const user = userStore.user;
const boostApiService = new BoostApiService(axiosInstance, errorHandler);

const gotoRatingView = () => {
  router.push({name: 'Rating'});
}

const goToSettings = () => {
  router.push({name: 'Settings'});
}

const getLevelImage = () => {
  switch (user?.user_lvl) {
    case 1:
      return Level1Image;
    case 2:
      return Level2Image;
    case 3:
      return Level3Image;
    case 4:
      return Level4Image;
    case 5:
      return Level5Image;
    case 6:
      return Level6Image;
    case 7:
      return Level7Image;
    case 8:
      return Level8Image;
    case 9:
      return Level9Image;
    case 10:
      return Level10Image;
    default:
      return Level1Image;
  }
}
const mainMonkeyAvatar = computed(() => {
  return {
    backgroundImage: `url(${getLevelImage()})`
  };
});

const openBoostModal = () => {
  if (!user?.next_boost || !user?.next_boost.lvl) return;

  visibleBoostModal.value = true;
}

const upgradeBoost = async () => {
  if (user!.money < user!.next_boost.price) return;

  const res = await boostApiService.upgradeBoost();
  if (res && res.right) {
    userStore.moneyPlus(-user!.next_boost.price);
    userStore.updateBoostData(res.right.next_boost);
    visibleBoostModal.value = false;
  }
}

const isDisabled = () => {
  return user!.money < user!.next_boost.price;
}

const goToLevels = () => {
  router.push({name: 'Levels'});
}

onMounted(() => {
  userStore.vibrationService.light();
});
</script>

<template>
  <div class="main-view-wrapper">
    <div class="main-monkey" :style="mainMonkeyAvatar"/>
    <div class="main-view-content">
      <div class="header-data">
        <div class="header-data-scoreboard">
          <div class="header-data-content">
            <div class="header-data-score-count">
              <img src="@/assets/img/coin.webp" alt="">
              <span>{{ formatNumberWithSpaces(userStore.user?.money ?? 0) }}</span>
            </div>
            <div class="header-data-statistic">
              <header-statistic-item title="Доход за тап"
                                     :value="(user?.taps_for_level ?? 0) + (user?.boost.one_tap ?? 0)"/>
              <header-statistic-item title="До lvl-апа"
                                     :value="formatNumber(user?.next_level_data.required_money ?? 0)"/>
              <header-statistic-item title="Доход в час" :value="formatNumber(user?.earnings_per_hour ?? 0)"/>
            </div>
          </div>
        </div>
      </div>
      <div class="gradient-black"></div>
      <div class="bottom-data">
        <div class="bottom-data-actions">
          <AppIconButton style="width: 48px; height: 48px;" @on-click="gotoRatingView">
            <img src="@/assets/svg/rating-icon.svg" alt="">
          </AppIconButton>
          <AppIconButton style="width: 48px; height: 48px;" @on-click="goToSettings">
            <img src="@/assets/svg/settings-icon.svg" alt="">
          </AppIconButton>
          <AppIconButton style="width: 48px; height: 48px;" @on-click="openBoostModal">
            <img src="@/assets/svg/boost-icon.svg" alt="">
          </AppIconButton>
        </div>
        <div class="current-level-wrapper">
          <div class="current-level-left-block" @click="goToLevels">
            <span class="text-lvl sf-pro-font">Lvl: </span>
            <span class="app-text-gradient text-current-level sf-pro-font">{{ user?.user_lvl }}</span>
            <img src="@/assets/svg/right-arrow.svg" alt="">
          </div>
          <level-indicator style="flex: 1"/>
        </div>
      </div>
    </div>
    <action-modal v-if="visibleBoostModal" @close="() => visibleBoostModal = false"
                  @on-accept="upgradeBoost">
      <div class="boost-modal-wrapper">
        <div style="height: 30px"/>
        <img src="@/assets/img/boost-icon.webp" alt="">
        <span class="boost-modal-title sf-pro-font">Усилитель</span>
        <span class="boost-description sf-pro-font">
          Увеличивает количество монет, которое вы можете заработать за одно нажатие
        </span>
        <span class="boost-description sf-pro-font">Уровень {{ userStore.user?.next_boost.lvl }}</span>
        <div class="boost-reward">
          <img src="@/assets/img/coin.webp" alt="">
          <span class="sf-pro-font">+ {{ userStore.user?.next_boost.tap_boost }} монета за тап</span>
        </div>
        <div class="boost-price">
          <img src="@/assets/img/coin.webp" alt="">
          <span class="sf-pro-font">{{ formatNumber(userStore.user?.next_boost.price ?? 0) }}</span>
        </div>
      </div>
      <template #actions>
        <modal-action-button
            style="width: 133px; height: 67px"
            button-text="Получить"
            @on-accept="upgradeBoost"
            :is-disabled="isDisabled()"
            :disabled-text="isDisabled() ? 'Нет денег' : 'Получить'"
        />
      </template>
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
  background-image: url('@/assets/img/main-view-bg.webp');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  position: relative;
  box-sizing: border-box;

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

    .gradient-black {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 215px;
      background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, #000000 58.43%);
      z-index: 11;
    }

    .header-data {
      background: linear-gradient(180deg, #000000 0%, rgba(0, 0, 0, 0) 58.43%);
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      box-sizing: border-box;
      position: relative;
      z-index: 12;

      .header-data-scoreboard {
        background-image: url("@/assets/img/header-scoreboard.webp");
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
      padding: 0 10px 65px 10px;
      position: relative;
      z-index: 12;

      .current-level-wrapper {
        display: flex;
        align-items: center;
        padding: 20px 0;
        gap: 5px;

        .current-level-left-block {
          display: flex;
          gap: 5px;
        }

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
    background-image: url('@/assets/img/level/character-1.webp');
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