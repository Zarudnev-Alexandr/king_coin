import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import LeaderboardRes from "@/shared/api/types/leaderboard-res.ts";

class RatingApiService {
  private readonly leaderBoardApi = '/users/leaderboard';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getRatings(category: 'columns' | 'money'): Promise<Either<CommonResponseError, LeaderboardRes>> {
    return this.errorHandler.processRequest<LeaderboardRes>(async () => {
      const response = await this.client.get<LeaderboardRes>(`${this.leaderBoardApi}?category=${category}`);
      return response.data;
    })
  }
}

export default RatingApiService;