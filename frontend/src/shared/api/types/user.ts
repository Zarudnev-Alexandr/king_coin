export interface UserBoost {
  boost_id: number,
  lvl: number,
  name: string,
  one_tap: number,
  pillars_10: number,
  pillars_30: number,
  pillars_100: number,
  price: number,
  tap_boost: number,
}

export interface User {
  earnings_per_hour: number,
  fio: string,
  last_login: string,
  money: number,
  tg_id: number,
  total_income: number,
  username: string | null,
  user_lvl: number,
  taps_for_level: number,
  boost: UserBoost,
  next_level_data: {
    lvl: number,
    required_money: number,
    taps_for_level: number,
    money_to_get_the_next_boost: number,
  },
  next_boost: UserBoost,
}