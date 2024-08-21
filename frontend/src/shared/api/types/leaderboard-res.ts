import RatingUser from "@/shared/api/types/rating-user-item.ts";

interface LeaderboardRes {
  current_user: RatingUser;
  leaderboard: RatingUser[];
}

export default LeaderboardRes;