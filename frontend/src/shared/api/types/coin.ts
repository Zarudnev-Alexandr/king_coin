export interface MetCondition {
  type: 'reach_upgrade_level' | 'invite' | 'subscribe_telegram',
  required_value: number;
  current_value: number;
  related_upgrade_id: number;
  channel_url?: string;
  description?: string;
  name_of_condition_upgrade?: string;
}

export interface Coin {
  name: string,
  category_id: number,
  image_url: string,
  is_in_shop: boolean,
  description: string,
  id: number,
  lvl: number,
  is_bought: boolean,
  factor: number | null,
  factor_at_new_lvl: number | null,
  price_of_next_lvl: number | null,
  conditions_met: boolean,
  unmet_conditions: MetCondition[],
}