<script setup lang="ts">
import ComboCardItem from "@/views/improvements-view/components/combo-card-item.vue";
import CardComboUnboxItem from "@/views/improvements-view/components/card-combo-unbox-item.vue";
import {computed, onMounted} from "vue";
import ComboApiService from "@/shared/api/services/combo-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {useImprovementsStore} from "@/shared/pinia/improvements-store.ts";

const comboApiService = new ComboApiService(axiosInstance, errorHandler);
const improvementsStore = useImprovementsStore();

onMounted(async () => {
  if (improvementsStore.combo) {
    return;
  }

  const res = await comboApiService.getComboData();
  if (res.right) {
    improvementsStore.setCombo(res.right);
  }
})

const images = computed(() => {
  const combo = improvementsStore.combo;
  if (!combo) return [];

  let images = []
  if (combo?.upgrade_1.is_bought) {
    images.push({url: combo.upgrade_1.image_url, name: combo.upgrade_1.name})
  }

  if (combo?.upgrade_2.is_bought) {
    images.push({url: combo.upgrade_2.image_url, name: combo.upgrade_2.name})
  }

  if (combo?.upgrade_3.is_bought) {
    images.push({url: combo.upgrade_3.image_url, name: combo.upgrade_3.name})
  }

  return images;
})
</script>

<template>
  <div class="combo-wrapper" v-if="improvementsStore.cryptoCoinList.length > 0">
    <div class="combo-indicator">
      <span class="sf-pro-font combo-indicator-title">Дневное комбо</span>
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
      <ComboCardItem :title="images[0].name" v-if="images.length > 0"/>
      <card-combo-unbox-item v-else/>
      <ComboCardItem :title="images[1].name" v-if="images.length > 1"/>
      <card-combo-unbox-item v-else/>
      <ComboCardItem :title="images[2].name" v-if="images.length > 2"/>
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