import {UserBoost} from "@/shared/api/types/user.ts";

interface BoostUpgradeResponse {
  user_id: number;
  boost_id: number;
  user_money: number;
  next_boost: UserBoost;
}

export default BoostUpgradeResponse;