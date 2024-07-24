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
}