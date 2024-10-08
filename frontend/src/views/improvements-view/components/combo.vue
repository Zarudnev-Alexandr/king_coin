<script setup lang="ts">
import ComboCardItem from "@/views/improvements-view/components/combo-card-item.vue";
import CardComboUnboxItem from "@/views/improvements-view/components/card-combo-unbox-item.vue";
import {onMounted, Ref, ref, watch} from "vue";
import ComboApiService from "@/shared/api/services/combo-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {useImprovementsStore} from "@/shared/pinia/improvements-store.ts";
import {isSpecialCard} from "@/helpers/coin.ts";

const comboApiService = new ComboApiService(axiosInstance, errorHandler);
const improvementsStore = useImprovementsStore();
const images: Ref<{ url: string, name: string, isSpecial: boolean }[]> = ref([]);

onMounted(async () => {
  if (improvementsStore.combo) {
    updateImages();
    return;
  }

  const res = await comboApiService.getComboData();
  if (res.right) {
    improvementsStore.setCombo(res.right);
  }
})


watch(() => improvementsStore.combo, (newReward, _) => {
  if (!newReward) {
    images.value = [];
    return
  }

  updateImages();
}, {deep: true});

const updateImages = () => {
  if (!improvementsStore.combo) {
    return;
  }

  let imgTemp = []

  if (improvementsStore.combo?.upgrade_1.is_bought) {
    const isSpecial = isSpecialCard(improvementsStore.combo.combo.upgrade_1_id!)
    imgTemp.push({
      url: improvementsStore.combo.upgrade_1.image_url!,
      name: improvementsStore.combo.upgrade_1.name,
      isSpecial: isSpecial
    })
  }

  if (improvementsStore.combo?.upgrade_2.is_bought) {
    const isSpecial = isSpecialCard(improvementsStore.combo.combo.upgrade_2_id!)
    imgTemp.push({
      url: improvementsStore.combo.upgrade_2.image_url!,
      name: improvementsStore.combo.upgrade_2.name,
      isSpecial: isSpecial
    })
  }

  if (improvementsStore.combo?.upgrade_3.is_bought) {
    const isSpecial = isSpecialCard(improvementsStore.combo.combo.upgrade_3_id!)
    imgTemp.push({
      url: improvementsStore.combo.upgrade_3.image_url!,
      name: improvementsStore.combo.upgrade_3.name,
      isSpecial: isSpecial
    })
  }
  images.value = imgTemp;
}
</script>

<template>
  <div class="combo-wrapper" v-if="improvementsStore.cryptoCoinList.length > 0">
    <div class="combo-indicator">
      <span class="sf-pro-font combo-indicator-title">{{ $t('daily_combo') }}</span>
      <div class="combo-indicator-icons">
        <span class="combo-indicator-icon-item" :class="{active: images.length > 0}"></span>
        <span class="combo-indicator-icon-item" :class="{active: images.length > 1}"></span>
        <span class="combo-indicator-icon-item" :class="{active: images.length > 2}"></span>
      </div>
      <div class="get-combo-button">
        <img src="@/assets/svg/coin.svg" alt="">
        <span class="sf-pro-font">+ 6 000 000</span>
      </div>
    </div>

    <div class="combo-list">
      <ComboCardItem :title="images[0].name" :img_url="images[0].url" v-if="images.length > 0"
                     :is-special="images[0].isSpecial"/>
      <card-combo-unbox-item v-else/>
      <ComboCardItem :title="images[1].name" :img_url="images[1].url" v-if="images.length > 1"
                     :is-special="images[1].isSpecial"/>
      <card-combo-unbox-item v-else/>
      <ComboCardItem :title="images[2].name" :img_url="images[2].url" v-if="images.length > 2"
                     :is-special="images[2].isSpecial"/>
      <card-combo-unbox-item v-else/>
    </div>
  </div>
</template>

<style scoped>
.combo-wrapper {
  display: flex;
  flex-direction: column;
  padding: 0 16px;
  gap: 20px;

  .combo-list {
    display: flex;
    gap: 8px;
  }

  .combo-indicator {
    background-color: rgba(57, 34, 0, 1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    border-radius: 10px;
    box-sizing: border-box;
    padding: 4px;

    .combo-indicator-icons {
      display: flex;
      justify-content: center;
      gap: 8px;

      .combo-indicator-icon-item {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: rgba(93, 56, 0, 1);
      }

      .active {
        background: linear-gradient(90deg, #FF8200 0%, #FFC800 100%);
      }
    }

    .get-combo-button {
      padding: 8px 7px;
      border-radius: 9px;
      background: linear-gradient(90deg, #FF8200 0%, #FFC800 100%);
      display: flex;
      align-items: center;
      gap: 4px;

      img {
        width: 16.5px;
        height: 16.5px;
      }

      span {
        font-size: 12px;
        font-weight: 700;
        line-height: 14.32px;
        text-align: right;
        color: white;
      }
    }

    .combo-indicator-title {
      font-size: 12px;
      font-weight: 600;
      line-height: 14.32px;
      text-align: left;
      padding-left: 15px;
      color: white;
    }
  }
}
</style>