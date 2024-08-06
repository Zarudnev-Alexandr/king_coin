<script setup lang="ts">
import {formatNumber, formatNumberWithSpaces} from "@/helpers/formats.ts";
import ActionModal from "@/components/ActionModal.vue";
import {useImprovementsStore} from "@/shared/pinia/improvements-store.ts";
import CoinApiService from "@/shared/api/services/coin-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import ComboApiService from "@/shared/api/services/combo-api-service.ts";
import CoinUpgradeResponse from "@/shared/api/types/coin-upgrade-response.ts";

const improvementsStore = useImprovementsStore();
const userStore = useUserStore();
const coinApiService = new CoinApiService(axiosInstance, errorHandler);
const comboApiService = new ComboApiService(axiosInstance, errorHandler);

const handleClose = () => {
  improvementsStore.setSelectCoinForImpro(null);
}

const checkCombo = (res: CoinUpgradeResponse) => {
  if (res.combo_status.upgrade_1_purchased && improvementsStore.combo) {
    improvementsStore.combo.upgrade_1.is_bought = true;
    improvementsStore.combo.upgrade_1.name = improvementsStore.selectCoinForImpro?.name ?? '';
    improvementsStore.combo.upgrade_1.image_url = improvementsStore.selectCoinForImpro?.image_url ?? '';
    improvementsStore.setComboNotify(true);
  } else if (res.combo_status.upgrade_2_purchased && improvementsStore.combo) {
    improvementsStore.combo.upgrade_2.is_bought = true;
    improvementsStore.combo.upgrade_2.name = improvementsStore.selectCoinForImpro?.name ?? '';
    improvementsStore.combo.upgrade_2.image_url = improvementsStore.selectCoinForImpro?.image_url ?? '';
    improvementsStore.setComboNotify(true);
  } else if (res.combo_status.upgrade_3_purchased && improvementsStore.combo) {
    improvementsStore.combo.upgrade_3.is_bought = true;
    improvementsStore.combo.upgrade_3.name = improvementsStore.selectCoinForImpro?.name ?? '';
    improvementsStore.combo.upgrade_3.image_url = improvementsStore.selectCoinForImpro?.image_url ?? '';
    improvementsStore.setComboNotify(true);
  }
}

const updateCombo = () => {
  comboApiService.getComboData().then(res => {
    if (res.right) {
      improvementsStore.setCombo(res.right);
      improvementsStore.setComboNotify(true);
    }
  });
}

const handleAccept = async () => {
  if (!improvementsStore.selectCoinForImpro || !userStore.user) {
    return;
  }

  if (userStore.user.money < (improvementsStore.selectCoinForImpro.price_of_next_lvl ?? 0)) {
    return;
  }

  const res = await coinApiService.upgradeCoin(improvementsStore.selectCoinForImpro.id, userStore.user.tg_id); // todo поправить после исправление в бэке
  if (res.right) {
    userStore.user.money -= improvementsStore.selectCoinForImpro.price_of_next_lvl ?? 0;
    userStore.user.earnings_per_hour += improvementsStore.selectCoinForImpro.factor_at_new_lvl ?? 0;
    improvementsStore.selectCoinForImpro.price_of_next_lvl = res.right.price_of_next_lvl;
    improvementsStore.selectCoinForImpro.factor_at_new_lvl = res.right.factor_at_new_lvl;
    improvementsStore.selectCoinForImpro.factor = res.right.current_factor;
    improvementsStore.selectCoinForImpro.lvl = res.right.current_lvl;

    if (res.right.combo_status.new_combo_created) {
      updateCombo()
    } else {
      checkCombo(res.right);
    }
    improvementsStore.setSelectCoinForImpro(null);
  }
}
</script>

<template>
  <ActionModal v-if="improvementsStore.selectCoinForImpro" @close="handleClose" @on-accept="handleAccept">
    <div class="card-impro-modal-content-wrapper">
      <img src="@/assets/img/specific/card-modal-content-example-icon.png" alt="">
      <span class="card-name sf-pro-font">{{ improvementsStore.selectCoinForImpro.name }}</span>
      <span class="impro-description sf-pro-font">{{ improvementsStore.selectCoinForImpro.description }}</span>
      <div class="impro-data-income">
        <span>Прибыль в час</span>
        <div class="impro-data-income-value">
          <img src="@/assets/svg/coin.svg" alt="">
          <span class="sf-pro-font">+ {{
              formatNumber(improvementsStore.selectCoinForImpro.factor_at_new_lvl ?? 0)
            }}</span>
        </div>
      </div>
      <div class="imrpo-price">
        <img src="@/assets/svg/coin.svg" alt="">
        <span class="sf-pro-font">{{
            formatNumberWithSpaces(improvementsStore.selectCoinForImpro.price_of_next_lvl ?? 0)
          }}</span>
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
  padding-top: 30px;

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