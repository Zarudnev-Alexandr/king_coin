<script setup lang="ts">
import {formatNumberWithSpaces} from "@/helpers/formats.ts";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import FloatButton from "@/components/FloatButton.vue";

const {selectTaskForFulfill} = useAppStore();

const goToSubscribe = () => {
  window.open(selectTaskForFulfill?.link ?? '', '_blank');
}
</script>

<template>
  <div class="fulfill-modal-wrap">
    <img src="@/assets/svg/income/task-fulfill-example-avatar.png" alt="">
    <span class="card-name sf-pro-font">{{ selectTaskForFulfill?.name }}</span>
    <div class="description-wrap">
      <span class="fulfill-description sf-pro-font">{{ selectTaskForFulfill?.description }}</span>
      <FloatButton @click="goToSubscribe" style="width: 128px; height: 55.69px"
                   v-if="selectTaskForFulfill?.type === 'subscribe_telegram'"
      >
        <h3 class="subscribe-btn">{{ $t('subscribe') }}</h3>
      </FloatButton>
    </div>
    <div class="fulfill-price">
      <img src="@/assets/svg/coin.svg" alt="">
      <span class="sf-pro-font">{{ formatNumberWithSpaces(selectTaskForFulfill?.reward ?? 0) }}</span>
    </div>
  </div>
</template>

<style scoped>
.fulfill-modal-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 15px;
  padding-bottom: 10px;
  padding-top: 30px;

  .description-wrap {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;

    .subscribe-btn {
      font-family: 'SuperSquadRus', sans-serif;
      font-size: 14px;
      font-weight: 400;
      line-height: 21.62px;
      text-align: center;
      color: rgba(93, 56, 0, 1);
    }
  }

  img {
    border-radius: 10px;
    width: 106px;
    height: auto;
  }

  .card-name {
    font-size: 28px;
    font-weight: 800;
    line-height: 33.41px;
    text-align: center;
    color: white;
  }

  .fulfill-description {
    font-size: 10px;
    font-weight: 400;
    line-height: 11.93px;
    text-align: center;
    color: rgba(194, 163, 117, 1);
    width: 70%;
  }

  .fulfill-price {
    display: flex;
    gap: 8px;
    justify-content: center;
    align-items: center;

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
</style>