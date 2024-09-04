import {UserCheck} from "@/shared/api/types/user-check.ts";

interface GameResult {
  money_added: number;
  users_money: number;
  user_check: UserCheck;
}

export default GameResult;