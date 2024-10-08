import {Coin} from "@/shared/api/types/coin.ts";
import {useImprovementsStore} from "@/shared/pinia/improvements-store.ts";


export const checkIsAvailable = (coin?: Coin) => {
  const improvementsStore = useImprovementsStore();

  if (!coin) {
    return false;
  }

  if (coin.conditions_met) {
    return true;
  }

  for (const condition of coin.unmet_conditions) {
    if (condition.type === 'reach_upgrade_level') {
      const reachCoin = improvementsStore.getCardById(condition.related_upgrade_id!);
      return (reachCoin?.lvl ?? 0) >= condition.required_value;
    }
  }
  return false;
}

export const getTaskText = (coin: Coin) => {
  const improvementsStore = useImprovementsStore();

  if (coin.unmet_conditions.length === 0) {
    return '';
  }

  if (coin.unmet_conditions[0].type === 'subscribe_telegram') return 'Follow TG';
  if (coin.unmet_conditions[0].type === 'invite') return `Invite ${coin.unmet_conditions[0].required_value} friends`;
  if (coin.unmet_conditions[0].type === 'reach_upgrade_level') {
    const coinName = improvementsStore.getCardById(coin.unmet_conditions[0].related_upgrade_id!)?.name ?? ''
    return `${coinName} - ${coin.unmet_conditions[0].required_value} lvl`;
  }
}

export const availableOpenModal = (coin: Coin) => {
  const improvementsStore = useImprovementsStore();
  if (coin.price_of_next_lvl === null) {
    return false;
  }

  if (!coin.conditions_met) {
    if (coin.unmet_conditions.length === 0) {
      return false;
    }

    if (coin.unmet_conditions[0].type === 'reach_upgrade_level') {
      const reachCoin = improvementsStore.getCardById(coin.unmet_conditions[0].related_upgrade_id!);
      return (reachCoin?.lvl ?? 0) >= coin.unmet_conditions[0].required_value;
    }

    return coin.unmet_conditions[0].type === 'subscribe_telegram';
  }

  return true
}

export const isSpecialCard = (id: number) => {
  const improvementsStore = useImprovementsStore();
  return improvementsStore.specialCoinList.some(item => item.id === id);
}
