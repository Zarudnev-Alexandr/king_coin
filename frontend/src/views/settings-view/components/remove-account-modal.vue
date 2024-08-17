<script setup lang="ts">

import FloatButton from "@/components/FloatButton.vue";

const emits = defineEmits(['close', 'accept']);

const close = () => {
  emits('close');
}

const accept = () => {
  emits('accept');
}
</script>

<template>
  <div class="remove-modal-wrap">
    <h2 class="title">{{ $t('are_you_sure') }}</h2>
    <span class="subtitle">{{ $t('data_cannot_be_recovered') }}</span>

    <div class="buttons-wrap">
      <FloatButton style="flex: 1" @click="close">
        <span>{{ $t('no_im_staying') }}</span>
      </FloatButton>

      <div class="remove-icon-wrap" @click="accept">
        <img src="@/assets/img/remove/remove-left-top-shadow.svg" class="left-top-shadow" alt="">
        <img src="@/assets/img/remove/remove-bottom-right-shadow.svg" class="left-bottom-shadow" alt="">
        <img src="@/assets/img/remove/remove-icon.svg" alt="" style="width: 24px; height: 24px;">
      </div>
    </div>

    <img src="@/assets/img/remove/delete-monkey.webp" alt="">
  </div>
</template>

<style scoped>
.remove-modal-wrap {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 30;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  gap: 15px;

  .title {
    font-family: 'SuperSquadRus', sans-serif;
    font-size: 34px;
    font-weight: 400;
    line-height: 52.49px;
    text-align: center;
    color: white;
    margin: 0;
  }

  .subtitle {
    font-size: 12px;
    font-weight: 600;
    line-height: 17.38px;
    text-align: center;
    color: white;
    width: 219px;
  }

  .buttons-wrap {
    width: 219px;
    display: flex;
    gap: 5px;

    span {
      font-family: 'SuperSquadRus', sans-serif;
      font-size: 14px;
      font-weight: 400;
      line-height: 21.62px;
      text-align: center;
      color: rgba(93, 56, 0, 1);
    }

    .remove-icon-wrap {
      background-color: rgba(57, 34, 0, 1);
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 10px;
      border: 2px solid white;
      width: 65px;
      height: 65px;
      position: relative;

      .left-bottom-shadow {
        position: absolute;
        bottom: 0;
        right: 0;
        width: 45.69px;
        height: 45.69px;
      }

      .left-top-shadow {
        position: absolute;
        top: 3px;
        left: 3px;
        width: 16.22px;
        height: 12.28px;
      }
    }
  }

  img {
    width: 100%;
  }
}
</style>