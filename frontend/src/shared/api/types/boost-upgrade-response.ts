import {UserBoost} from "@/shared/api/types/user.ts";
import {UserCheck} from "@/shared/api/types/user-check.ts";

interface BoostUpgradeResponse {
  user_id: number;
  boost_id: number;
  user_money: number;
  next_boost: UserBoost;
  user_check: UserCheck;
}

export default BoostUpgradeResponse;