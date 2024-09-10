<script setup lang="ts">
import {formatNumber, formatNumberWithSpaces} from "@/helpers/formats.ts";
import ActionModal from "@/components/ActionModal.vue";
import {useImprovementsStore} from "@/shared/pinia/improvements-store.ts";
import CoinApiService from "@/shared/api/services/coin-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import ComboApiService from "@/shared/api/services/combo-api-service.ts";
import CoinUpgradeResponse from "@/shared/api/types/coin-upgrade-response.ts";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import ModalActionButton from "@/components/ModalActionButton.vue";
import GoldCoin from "@/assets/svg/coin.svg";
import SilverCoin from "@/assets/svg/silver-coin.svg";
import {computed, Ref, ref} from "vue";
import {checkIsAvailable} from "@/helpers/coin.ts";
import {useI18n} from "vue-i18n";
import ImproModalDescription from "@/views/improvements-view/components/impro-modal-description.vue";
import {ToastType} from "@/shared/api/types/toast.ts";

const improvementsStore = useImprovementsStore();
const userStore = useUserStore();
const appStore = useAppStore();
const {t} = useI18n();
const coinApiService = new CoinApiService(axiosInstance, errorHandler);
const comboApiService = new ComboApiService(axiosInstance, errorHandler);
const isLoading: Ref<boolean> = ref(false);

const handleClose = () => {
  improvementsStore.setSelectCoinForImpro(null);
}

const isDisabled = () => {
  if (!improvementsStore.selectCoinForImpro?.conditions_met) return false;

  if (!improvementsStore.selectCoinForImpro || !improvementsStore.selectCoinForImpro!.price_of_next_lvl) return true;

  return userStore.user!.money < improvementsStore.selectCoinForImpro!.price_of_next_lvl!;
}

const checkSubscribe = async () => {
  if (!improvementsStore.selectCoinForImpro || isLoading.value) return

  isLoading.value = true
  const cardId = improvementsStore.selectCoinForImpro?.id;
  const res = await coinApiService.checkIsAvailable(improvementsStore.selectCoinForImpro!);
  if (res && res.right && improvementsStore.selectCoinForImpro) {
    const card = improvementsStore.getCardById(cardId);
    if (card) card.conditions_met = true;
  } else if (res && res.left) {
    appStore.pushToast(ToastType.ERROR, t('no_subscription'));
  }
  isLoading.value = false
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
  if (!improvementsStore.selectCoinForImpro || !userStore.user || isLoading.value) {
    return;
  }

  if (!improvementsStore.selectCoinForImpro.conditions_met && improvementsStore.selectCoinForImpro.unmet_conditions[0].type === 'subscribe_telegram') {
    await checkSubscribe();
    return;
  }

  if (userStore.user.money < (improvementsStore.selectCoinForImpro.price_of_next_lvl ?? 0)) {
    return;
  }

  isLoading.value = true
  const res = await coinApiService.upgradeCoin(improvementsStore.selectCoinForImpro.id, userStore.user.tg_id);
  if (res.right) {
    userStore.animationPlusMoney(res.right.user_check.money - userStore.user.money);
    userStore.user.earnings_per_hour = res.right.user_check.total_hourly_income;
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
    appStore.playCoinAnimation();

    if (res.right.user_check.info) {
      userStore.setLevelUpData(res.right.user_check.info.data);
      userStore.setLevelUpVisible(true);
    }
  } else {
    appStore.pushToast(ToastType.ERROR, t('request_error_text'))
  }

  isLoading.value = false;
}

const getPlusImpro = () => {
  if (!improvementsStore.selectCoinForImpro) {
    return 0;
  }
  return ((improvementsStore.selectCoinForImpro.factor_at_new_lvl ?? 0) - (improvementsStore.selectCoinForImpro.factor ?? 0));
}

const isSpecialCategory = computed(() => improvementsStore.selectCoinForImpro?.category_id === 3);

const mainButtonText = computed(() => {
  if (!improvementsStore.selectCoinForImpro) return t('get_it');
  if (!improvementsStore.selectCoinForImpro.conditions_met && improvementsStore.selectCoinForImpro.unmet_conditions[0].type === 'subscribe_telegram') {
    return t('check')
  }

  return t('get_it');
})
</script>

<template>
  <ActionModal v-if="improvementsStore.selectCoinForImpro"
               @close="handleClose"
               @on-accept="handleAccept"
               :hide-bottom-right-bg-svg="isSpecialCategory"
               :hide-top-left-bg-svg="isSpecialCategory"
  >
    <div class="card-impro-modal-content-wrapper">
      <div v-if="isSpecialCategory" style="height: 190px"/>
      <div v-else class="simple-card-img-wrap">
        <img v-if="!checkIsAvailable(improvementsStore.selectCoinForImpro)"
             src="@/assets/svg/unavailable-simple-modal.svg"
             class="simple-card-unavailable"
             alt="">
        <img :src="improvementsStore.selectCoinForImpro.image_url" alt="" class="simple-card-img">
      </div>

      <div v-if="isSpecialCategory" class="special-img-wrap">
        <img v-if="!checkIsAvailable(improvementsStore.selectCoinForImpro)"
             src="@/assets/svg/unavailable-special-card.svg"
             class="unavaliable-layer" alt="">
        <img :src="improvementsStore.selectCoinForImpro.image_url" alt=""/>
        <div class="special-img-gradient"/>
      </div>
      <span class="card-name sf-pro-font z-10">{{ improvementsStore.selectCoinForImpro.name }}</span>
      <impro-modal-description/>
      <div class="impro-data-income z-10">
        <span>{{ $t('hourly_profit') }}</span>
        <div class="impro-data-income-value">
          <img :src="checkIsAvailable(improvementsStore.selectCoinForImpro!) ? GoldCoin : SilverCoin" alt="">
          <span class="sf-pro-font">+ {{ formatNumber(getPlusImpro()) }}</span>
        </div>
      </div>
      <div class="imrpo-price z-10">
        <img :src="checkIsAvailable(improvementsStore.selectCoinForImpro!) ? GoldCoin : SilverCoin" alt="">
        <span class="sf-pro-font">{{
            formatNumberWithSpaces(improvementsStore.selectCoinForImpro.price_of_next_lvl ?? 0)
          }}</span>
      </div>
    </div>
    <template #actions>
      <modal-action-button
          style="width: 133px; height: 67px"
          :button-text="mainButtonText"
          @on-accept="handleAccept"
          :is-disabled="isDisabled()"
          :is-loading="isLoading"
          :disabled-text="isDisabled() ? $t('no_money') : $t('get_it')"
      />
    </template>

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
  position: relative;

  .special-img-wrap {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 0;
    width: 100%;

    .unavaliable-layer {
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
      width: 100%;
    }

    img {
      width: 100%;
      object-fit: cover;
      border-radius: 10px 10px 0 0;
    }

    .special-img-gradient {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 190px;
      z-index: 1;
      background: linear-gradient(180deg, rgba(57, 34, 0, 0) 0%, #392200 100%);
    }
  }

  .simple-card-img-wrap {
    position: relative;

    .simple-card-unavailable {
      position: absolute;
      right: 0;
      top: 0;
    }

    .simple-card-img {
      border-radius: 10px;
      width: 106px;
      height: auto;
    }
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
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;

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

.z-10 {
  position: relative;
  z-index: 10;
}
</style>