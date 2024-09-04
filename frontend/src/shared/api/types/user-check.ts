import LvlUpData from "@/shared/api/types/lvl-up-data.ts";

export interface UserCheckInfo {
  event: string;
  data: LvlUpData
}

export interface UserCheck {
  hours_passed: number;
  info: UserCheckInfo | null;
  money: number;
  total_hourly_income: number;
  total_income: number;
}
