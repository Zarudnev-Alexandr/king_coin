import {defineStore} from "pinia";
import {Ref, ref} from "vue";
import {Coin} from "@/shared/api/types/coin.ts";
import Combo from "@/shared/api/types/combo.ts";

export const useImprovementsStore = defineStore('improvementsStore', () => {
  const isLoading: Ref<boolean> = ref(false);
  const dataLoaded: Ref<boolean> = ref(false);
  const visibleComboNotify: Ref<boolean> = ref(false);

  // Карточка который выбран для улучшения
  const selectCoinForImpro: Ref<Coin | null> = ref(null);
  const combo: Ref<Combo | null> = ref(null);

  const cryptoCoinList: Ref<Coin[]> = ref([]);
  const actionCoinList: Ref<Coin[]> = ref([]);
  const specialCoinList: Ref<Coin[]> = ref([]);

  const setCryptoCoinList = (coins: Coin[]) => {
    cryptoCoinList.value = coins;
  }

  const setActionCoinList = (coins: Coin[]) => {
    actionCoinList.value = coins;
  }

  const setSpecialCoinList = (coins: Coin[]) => {
    specialCoinList.value = coins;
  }

  const setDataLoaded = (loaded: boolean) => {
    dataLoaded.value = loaded;
  }

  const setLoading = (loading: boolean) => {
    isLoading.value = loading;
  }

  const setSelectCoinForImpro = (coin: Coin | null) => {
    selectCoinForImpro.value = coin;
  }

  const setCombo = (comboData: Combo | null) => {
    combo.value = comboData;
  }

  const setComboNotify = (visible: boolean) => {
    visibleComboNotify.value = visible;
  }

  const upgradePurchaseCombo = (index: 1 | 2 | 3) => {
    if (combo.value) {
      if (index === 1) {
        combo.value.upgrade_1.is_bought = true;
      } else if (index === 2) {
        combo.value.upgrade_2.is_bought = true;
      } else if (index === 3) {
        combo.value.upgrade_3.is_bought = true;
      }
    }
  }

  return {
    isLoading,
    setLoading,
    dataLoaded,
    setDataLoaded,
    cryptoCoinList,
    setCryptoCoinList,
    actionCoinList,
    setActionCoinList,
    specialCoinList,
    setSpecialCoinList,
    selectCoinForImpro,
    setSelectCoinForImpro,
    combo,
    setCombo,
    visibleComboNotify,
    setComboNotify,
    upgradePurchaseCombo,
  }
});