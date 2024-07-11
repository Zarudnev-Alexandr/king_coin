<script setup lang="ts">
import {formatNumber, formatNumberWithSpaces} from "@/helpers/formats.ts";
import ActionModal from "@/components/ActionModal.vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";

const appStore = useAppStore();

const handleClose = () => {
  appStore.setSelectCoinForImpro(null);
}

const handleAccept = () => {
  console.log("Было принято");
  appStore.setSelectCoinForImpro(null);
}
</script>

<template>
  <ActionModal v-if="appStore.selectCoinForImpro" @close="handleClose" @on-accept="handleAccept">
    <div class="card-impro-modal-content-wrapper">
      <img src="@/assets/img/specific/card-modal-content-example-icon.png" alt="">
      <span class="card-name sf-pro-font">{{ appStore.selectCoinForImpro.name }}</span>
      <span class="impro-description sf-pro-font">Очень уморительный текст с описанием монеты и преимуществ, которые получит тип, купив ее</span>
      <div class="impro-data-income">
        <span>Множитель</span>
        <div class="impro-data-income-value">
          <img src="@/assets/svg/coin.svg" alt="">
          <span class="sf-pro-font">+ {{ formatNumber(appStore.selectCoinForImpro.income) }}</span>
        </div>
      </div>
      <div class="imrpo-price">
        <img src="@/assets/svg/coin.svg" alt="">
        <span class="sf-pro-font">{{ formatNumberWithSpaces(appStore.selectCoinForImpro.price) }}</span>
      </div>
    </div>
  </ActionModal>
</template>

<style scoped>
.card-impro-modal-content-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding-bottom: 10px;

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

  .impro-description {
    font-size: 10px;
    font-weight: 400;
    line-height: 11.93px;
    text-align: center;
    color: rgba(194, 163, 117, 1);
    width: 80%;
  }

  .impro-data-income {
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

    .impro-data-income-value {
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

  .imrpo-price {
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