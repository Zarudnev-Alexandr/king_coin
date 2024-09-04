import {UserCheck} from "@/shared/api/types/user-check.ts";

interface TaskDailyClaim {
  day: number,
  reward: number,
  total_money: number,
  user_check: UserCheck
}

export default TaskDailyClaim;