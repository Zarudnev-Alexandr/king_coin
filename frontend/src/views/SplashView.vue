<script setup lang="ts">
import {onMounted} from "vue";
import AppIconButton from "@/components/AppIconButton.vue";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import UserApiService from "@/shared/api/services/user-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import log from 'loglevel';
import SocketEventUpdate from "@/shared/api/types/socket-event-update.ts";
import {useRoute, useRouter} from "vue-router";
import LvlUpData from "@/shared/api/types/lvl-up-data.ts";
import BonusImg from "@/assets/img/bonus.png";

const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const userApiService = new UserApiService(axiosInstance, errorHandler);

const updateEachSecond = () => {

  setInterval(() => {
    if (userStore.user === null) {
      return;
    }

    const moneyOnSec = userStore.user.earnings_per_hour / 3600;
    userStore.moneyPlus(moneyOnSec);

  }, 1000);
}

onMounted(async () => {
  const img = new Image();
  img.src = BonusImg;
  img.onload = () => {};
  img.onerror = () => {};

  await router.isReady();

  Telegram.WebApp.expand();
  Telegram.WebApp.disableVerticalSwipes();

  let ref = null;

  if (route.query.ref) {
    ref = route.query.ref;
  }

  const response = await userApiService.getCurrentUser(ref as string);
  if (response.left) {
    return;
  }

  userStore.setUser(response.right!);
  userStore.moneyPlus(-response.right!.total_income);
  userStore.setAuth(true);
  updateEachSecond();

  const socket = new WebSocket(`wss://king-coin.online/api/ws/${userStore.user?.tg_id}`);
  socket.onopen = () => {
    log.info('Соединение установлено');
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Socket data", data);
    if (data.event === 'update') {
      userStore.setMoneyUpdate(data.data as SocketEventUpdate);
    } else if (data.event === 'new_lvl') {
      userStore.setLevelUpData(data.data as LvlUpData);
      userStore.setLevelUpVisible(true);
    }
  };

  socket.onclose = (event) => {
    if (event.wasClean) {
      log.info('Соединение закрыто чисто');
    } else {
      log.info('Обрыв соединения');
    }
    log.info(`Код: ${event.code} | Причина: ${event.reason}`);
  };
})
</script>

<template>
  <div class="splash-wrapper">
    <div class="splash-logo">
      <img src="@/assets/svg/logo-group.svg" alt="">
    </div>
    <div class="splash-loader">
      <div class="splash-loader-content">
        <div class="content-monet">
          <img src="@/assets/img/splash-monet.png" alt="">
        </div>
        <div class="splash-loader-content-indicator">
          <span class="splash-loader-content-text">Загрузка</span>
          <div class="splash-loader-content-indicator-group">
            <span class="splash-loader-content-indicator-item"></span>
            <span class="splash-loader-content-indicator-item"></span>
            <span class="splash-loader-content-indicator-item"></span>
            <span class="splash-loader-content-indicator-item"></span>
            <span class="splash-loader-content-indicator-item"></span>
            <span class="splash-loader-content-indicator-item"></span>
            <span class="splash-loader-content-indicator-item"></span>
          </div>
        </div>
        <div class="splash-loader-content-shared">
          <span class="splash-loader-content-shred-text">
            Наши официальные соц. сети
          </span>
          <div class="splash-loader-content-shared-links">
            <AppIconButton style="width: 48px; height: 48px;">
              <svg width="20" height="17" viewBox="0 0 20 17" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd"
                      d="M18.6529 0.463273C17.3216 0.941009 0.914291 7.08984 0.67263 7.2016C-0.130392 7.57288 -0.224272 8.06328 0.444229 8.39499C0.508771 8.427 1.61933 8.77343 2.91212 9.16486L5.26271 9.8765L10.6001 6.61946C13.5357 4.82807 15.9967 3.34228 16.0689 3.31774C16.2502 3.25608 16.4062 3.26184 16.479 3.33289C16.53 3.38261 16.5321 3.40757 16.4916 3.48064C16.4648 3.52899 14.5154 5.25593 12.1596 7.31829C9.80382 9.38064 7.87002 11.0842 7.86223 11.1039C7.85449 11.1236 7.77481 12.1533 7.68515 13.392L7.52219 15.6442L7.69927 15.6209C7.79667 15.6081 7.95091 15.5591 8.04201 15.5119C8.13315 15.4649 8.74646 14.9229 9.40498 14.3077C10.0635 13.6924 10.6251 13.1804 10.653 13.17C10.6808 13.1596 11.7295 13.8842 12.9833 14.7802C14.2371 15.6763 15.3612 16.4538 15.4813 16.5079C15.7963 16.6499 16.1511 16.6639 16.3815 16.5437C16.5874 16.4362 16.7885 16.1693 16.8731 15.8914C16.9059 15.7839 17.6227 12.553 18.4661 8.71177C19.8702 2.31629 19.9995 1.69711 20 1.36517C20.0005 1.05155 19.9871 0.976954 19.9009 0.811883C19.8402 0.695502 19.7366 0.576678 19.6354 0.507231C19.4039 0.348418 19.0207 0.331286 18.6529 0.463273Z"
                      fill="#5D3800"/>
              </svg>
            </AppIconButton>

            <AppIconButton style="width: 48px; height: 48px;">
              <svg width="20" height="15" viewBox="0 0 20 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd"
                      d="M7.8976 0.0214696C4.52265 0.0885398 2.54068 0.255813 1.92087 0.525748C1.35871 0.770599 0.883772 1.23025 0.604673 1.79959C0.242442 2.53853 0.0513153 4.15572 0.00659948 6.86013C-0.0291481 9.01988 0.0815569 10.9847 0.30889 12.2258C0.556913 13.5799 1.23591 14.3526 2.41024 14.6174C3.47695 14.858 6.30911 15.0003 10.0249 15C13.819 14.9997 16.5258 14.8637 17.6583 14.6163C18.0282 14.5355 18.5552 14.2568 18.8312 13.9959C19.1184 13.7245 19.4113 13.2536 19.5331 12.8678C19.8655 11.8147 20.0701 8.74373 19.9778 6.19377C19.8526 2.735 19.5893 1.64815 18.7022 0.928215C18.2913 0.594741 18.0089 0.472986 17.3759 0.356374C16.5924 0.212038 14.7033 0.084605 12.7154 0.0419931C10.3859 -0.0079072 9.55372 -0.0114843 7.8976 0.0214696ZM10.5888 5.88909C11.9936 6.7568 13.1414 7.48616 13.1394 7.50995C13.1366 7.54429 8.06813 10.7055 8.0159 10.7055C8.00818 10.7055 8.00189 9.26684 8.00189 7.50848C8.00189 5.75012 8.00927 4.31146 8.01828 4.31146C8.02733 4.31146 9.18406 5.02138 10.5888 5.88909Z"
                      fill="#5D3800"/>
              </svg>
            </AppIconButton>

            <AppIconButton style="width: 48px; height: 48px;">
              <svg width="22" height="13" viewBox="0 0 22 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd"
                      d="M9.21859 0.00728983C8.80015 0.0388814 8.26971 0.122976 8.05744 0.191388C7.69297 0.308862 7.23878 0.727818 7.32277 0.869065C7.33821 0.895026 7.42276 0.930148 7.51062 0.947083C7.90507 1.02318 8.23776 1.25567 8.3869 1.55939C8.6418 2.07857 8.75645 3.70239 8.61931 4.85192C8.5287 5.61178 8.49038 5.78792 8.35603 6.06344C7.99555 6.80251 7.1677 6.2042 6.25533 4.5453C5.93064 3.95498 5.0169 2.06029 4.81301 1.5547C4.56659 0.943643 4.48857 0.831128 4.20839 0.683001L3.9719 0.557975L2.18717 0.571291C0.575493 0.583311 0.388935 0.592292 0.263057 0.663742C0.0635113 0.777061 -0.0217258 0.931756 0.00467962 1.13292C0.0329343 1.34843 0.709843 2.91175 1.20866 3.91356C2.17982 5.86397 3.00234 7.28028 3.88164 8.51601C5.17486 10.3335 5.74705 10.9232 7.06831 11.8004C7.68527 12.2099 8.13055 12.4391 8.68102 12.6302C9.43736 12.8928 9.76661 12.9433 10.8958 12.9702C12.0196 12.9969 12.3425 12.9632 12.5806 12.7945C12.7767 12.6554 12.8374 12.4637 12.874 11.8673C12.9101 11.2788 13.0207 10.7741 13.1728 10.5046C13.3069 10.2667 13.5985 9.99206 13.7236 9.98562C14.1601 9.96328 14.4045 10.1517 15.3163 11.2138C16.1713 12.2095 16.4873 12.5025 16.9596 12.7375C17.1725 12.8434 17.4337 12.9508 17.5402 12.9762C17.7982 13.0377 21.2813 12.9686 21.5062 12.8975C21.7288 12.8271 21.9686 12.5827 21.9741 12.4206C21.9891 11.977 21.9269 11.777 21.6282 11.3084C21.2357 10.6925 20.8984 10.2992 19.7503 9.11822C18.5311 7.86412 18.446 7.7474 18.4442 7.32786C18.4428 6.97566 18.6012 6.70506 19.6716 5.23174C21.1815 3.1534 21.7861 2.14953 21.9542 1.44178C22.0528 1.02671 21.9967 0.826436 21.7423 0.685145L21.5612 0.584607L19.3894 0.59962C17.8542 0.61021 17.1866 0.629871 17.1117 0.666646C16.966 0.738185 16.8114 0.99905 16.6178 1.50063C16.1019 2.83654 15.0399 4.76113 14.34 5.62822C14.0615 5.97331 13.6286 6.3265 13.4842 6.3265C13.2826 6.3265 13.1164 6.19124 12.9904 5.9247L12.8741 5.67858L12.8859 3.35863C12.8985 0.863792 12.8931 0.790108 12.6709 0.460698C12.452 0.136248 11.9184 0.0249847 10.4873 0.00545778C9.90776 -0.00249597 9.33686 -0.00164696 9.21859 0.00728983Z"
                      fill="#5D3800"/>
              </svg>
            </AppIconButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.splash-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/img/loader-bg.webp');
  background-repeat: no-repeat;
  background-size: cover; /* Изображение масштабируется, чтобы полностью покрыть контейнер */
  background-position: center; /* Изображение центрируется */
}

.splash-logo {
  width: 100%;
  display: flex;
  padding: 20px;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.splash-loader {
  width: 100%;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, #000000 58.43%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 30px 0;
}

.splash-loader-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  gap: 75px;
}

.splash-loader-content-shared {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;

  .splash-loader-content-shred-text {
    font-family: 'SF Pro Text', sans-serif;
    font-size: 14px;
    font-weight: 500;
    line-height: 16.71px;
    text-align: center;
    color: white;
  }

  .splash-loader-content-shared-links {
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
  }
}

.splash-loader-content-indicator {
  display: flex;
  flex-direction: column;
  gap: 15px;

  .splash-loader-content-text {
    font-family: 'SF Pro Text', sans-serif;
    font-size: 28px;
    font-weight: 800;
    line-height: 33.41px;
    text-align: center;
    background: linear-gradient(90deg, #FF8200 0%, #FFC800 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }


  .splash-loader-content-indicator-group {
    display: flex;
    justify-content: center;
    gap: 8px;

    .splash-loader-content-indicator-item {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      animation: loader 1.4s infinite;
    }

    .splash-loader-content-indicator-item:nth-child(1) {
      animation-delay: 0s;
    }

    .splash-loader-content-indicator-item:nth-child(2) {
      animation-delay: 0.2s;
    }

    .splash-loader-content-indicator-item:nth-child(3) {
      animation-delay: 0.4s;
    }

    .splash-loader-content-indicator-item:nth-child(4) {
      animation-delay: 0.6s;
    }

    .splash-loader-content-indicator-item:nth-child(5) {
      animation-delay: 0.8s;
    }

    .splash-loader-content-indicator-item:nth-child(6) {
      animation-delay: 1s;
    }

    .splash-loader-content-indicator-item:nth-child(7) {
      animation-delay: 1.2s;
    }
  }
}

.content-monet {
  position: absolute;

  top: 0;
  left: -44px;

  img {
    width: 57px;
    height: 40px;
  }
}

@keyframes loader {
  0%, 20%, 100% {
    background-color: white;
  }
  10% {
    background-color: orange;
  }
}
</style>