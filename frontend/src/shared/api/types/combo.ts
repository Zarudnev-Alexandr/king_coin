interface Combo {
  user_id: number,
  combo_id: number,
  upgrade_1: {
    is_bought: boolean,
    image_url: string | null,
    name: string,
  },
  upgrade_2: {
    is_bought: boolean,
    image_url: string | null,
    name: string,
  },
  upgrade_3: {
    is_bought: boolean,
    image_url: string | null,
    name: string,
  },
  reward_claimed: boolean,
  combo: {
    upgrade_1_id: number | null,
    upgrade_2_id: number | null,
    upgrade_3_id: number | null,
    reward: number,
    id: number,
  }
}

export default Combo;