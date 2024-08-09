<script setup lang="ts">

import Combo from "@/views/improvements-view/components/combo.vue";
import CoinCardList from "@/views/improvements-view/components/coin-card-list.vue";
import CoinApiService from "@/shared/api/services/coin-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {onBeforeUnmount, onMounted, ref} from "vue";
import {useImprovementsStore} from "@/shared/pinia/improvements-store.ts";
import {CoinCategory} from "@/shared/api/types/coin-category.ts";
import {formatNumberWithSpaces} from "@/helpers/formats.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";

const coinApiService = new CoinApiService(axiosInstance, errorHandler);
const {
  setLoading,
  dataLoaded,
  setDataLoaded,
  setCryptoCoinList,
  setActionCoinList,
  setSpecialCoinList,
} = useImprovementsStore();
const userStore = useUserStore();
const isAnimating = ref(false);

onMounted(async () => {
  userStore.setImproPulseAnimationMethod(startAnimation);
  userStore.vibrationService.light();
  if (dataLoaded) {
    return;
  }

  setLoading(true);
  const response = await coinApiService.getCategories();
  if (response.right) {
    setDataLoaded(true);
    response.right.map((item: CoinCategory) => {
      if (item.category === 'Crypto') {
        setCryptoCoinList(item.upgrades);
      } else if (item.category === 'Action') {
        setActionCoinList(item.upgrades);
      } else if (item.category === 'Special') {
        setSpecialCoinList(item.upgrades);
      }
    });
    setLoading(false);
  }
});

function startAnimation() {
  isAnimating.value = true;
  setTimeout(() => {
    isAnimating.value = false;
  }, 1000);
}

onBeforeUnmount(() => {
  userStore.setImproPulseAnimationMethod(() => {
  });
});
</script>

<template>
  <div class="improvements-wrapper">
    <div class="improvements-header">
      <div class="impro-scoreboard">
        <div style="height: 35px"></div>
        <div class="impro-scoreboard-content" :class="{ 'pulse-animation': isAnimating }">
          <img src="@/assets/img/coin.webp" alt="">
          <span>{{ formatNumberWithSpaces(userStore.user?.money ?? 0) }}</span>
        </div>
      </div>
    </div>
    <combo/>
    <coin-card-list style="margin-top: 20px;"/>
    <div style="margin-top: 100px;"></div>
  </div>
</template>

<style scoped>
.improvements-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/img/app-bg.webp');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  overflow-y: auto;

  .improvements-header {
    height: 178px;
    width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    z-index: 10;

    .impro-scoreboard {
      background-image: url("@/assets/img/improvement-scoreboard.webp");
      background-repeat: no-repeat;
      background-size: cover;
      background-position: center;
      padding: 15px 0 80px 0;
      opacity: 0;
      transform: translateY(-50px);
      animation: slideIn 0.5s ease-in-out forwards;
    }

    .impro-scoreboard-content {
      display: flex;
      justify-content: center;
      gap: 10px;

      img {
        width: 55px;
        height: 56px;
      }

      span {
        font-family: 'SuperSquadRus', sans-serif;
        font-size: 34px;
        font-weight: 400;
        line-height: 53px;
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

.pulse-animation {
  animation: pulse 0.3s infinite;
}

@keyframes slideIn {
  to {
    opacity: 1; /* Конечная прозрачность */
    transform: translateY(0); /* Конечное смещение */
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}
</style>