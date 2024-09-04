import {UserCheck} from "@/shared/api/types/user-check.ts";

interface CheckTask {
  status: string,
  money_received: number,
  current_user_money: number,
  user_check: UserCheck;
}

export default CheckTask;