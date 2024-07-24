interface CoinUpgradeResponse {
  user_remaining_money: number,
  upgrade_id: number,
  current_lvl: number,
  current_factor: number,
  factor_at_new_lvl: number | null,
  price_of_next_lvl: number | null,
  next_lvl: number | null,
  combo_status: {
    combo_completed: boolean,
    new_combo_created: boolean,
    reward_claimed: boolean,
    upgrade_1_purchased: boolean,
    upgrade_2_purchased: boolean,
    upgrade_3_purchased: boolean,
  }
}

export default CoinUpgradeResponse;