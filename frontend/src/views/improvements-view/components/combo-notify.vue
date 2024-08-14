<script setup lang="ts">

import FloatButton from "@/components/FloatButton.vue";
import {useImprovementsStore} from "@/shared/pinia/improvements-store.ts";
import {computed, ref, Ref, watch} from "vue";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import {useI18n} from "vue-i18n";

const {setComboNotify} = useImprovementsStore();
const improvementsStore = useImprovementsStore();
const userStore = useUserStore();
const appStore = useAppStore();
const images: Ref<{ url: string, name: string }[]> = ref([]);
const {t} = useI18n();

const handleConfirm = () => {
  if (images.value.length > 2 && !improvementsStore.combo?.reward_claimed) {
    userStore.animationPlusMoney(6000000);
    improvementsStore.combo!.reward_claimed = true;
    appStore.playCoinAnimation();
  }

  setComboNotify(false);
}

watch(() => improvementsStore.combo, (newReward, _) => {
  if (!newReward) {
    images.value = [];
    return
  }
  let imgTemp = [];

  if (newReward?.upgrade_1.is_bought) {
    imgTemp.push({url: newReward.upgrade_1.image_url!, name: newReward.upgrade_1.name})
  }

  if (newReward?.upgrade_2.is_bought) {
    imgTemp.push({url: newReward.upgrade_2.image_url!, name: newReward.upgrade_2.name})
  }

  if (newReward?.upgrade_3.is_bought) {
    imgTemp.push({url: newReward.upgrade_3.image_url!, name: newReward.upgrade_3.name})
  }
  images.value = imgTemp;
}, {deep: true});

const getButtonText = computed(() => {
  return images.value.length > 2 ? t('get_bonus') : t('need_more')
});

const getDescriptionText = computed(() => {
  return images.value.length > 2 ? t('all_cards_collected') : t('combo_collected_one', {count: images.value.length});
});
</script>

<template>
  <div class="combo-notify-wrapper" v-if="improvementsStore.visibleComboNotify">
    <div class="combo-info-wrapper">
      <span class="title">{{ $t('combo') }}</span>
      <span class="info sf-pro-font">{{ getDescriptionText }}</span>
      <FloatButton style="width: 175px; height: 65px;" @click="handleConfirm">
        <span class="button-text">{{ getButtonText }}</span>
      </FloatButton>
    </div>
    <div style="display: flex; position:relative;">
      <img src="@/assets/img/combo/bottom-left-coin.png" class="bottom-left" alt="">
      <img src="@/assets/img/combo/top-left-coin.png" class="top-left" alt="">
      <img src="@/assets/img/combo/right-top-coin.png" class="right-top" alt="">
      <img src="@/assets/img/combo/monkey.png" alt="" class="monkey">
    </div>
  </div>
</template>

<style scoped>
.combo-notify-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: end;
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 50;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  gap: 20px;

  .monkey {
    width: 100%;
    height: auto;
  }

  .combo-info-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;

    .title {
      font-family: 'SuperSquadRus', sans-serif;
      font-size: 34px;
      font-weight: 400;
      line-height: 52.49px;
      text-align: center;
      color: white;
    }

    .info {
      font-size: 10px;
      font-weight: 400;
      line-height: 11.93px;
      text-align: center;
      color: white;
      max-width: 206px;
    }

    .button-text {
      font-family: 'SuperSquadRus', sans-serif;
      font-size: 14px;
      font-weight: 400;
      line-height: 21.62px;
      text-align: center;
      color: rgba(93, 56, 0, 1);
    }
  }

  .bottom-left {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 111px;
    height: auto;
  }

  .top-left {
    position: absolute;
    left: 10px;
    top: 10px;
    width: 50px;
    height: auto;
  }

  .right-top {
    position: absolute;
    right: 10px;
    top: 25px;
    width: 53px;
    height: auto;
  }
}
</style>