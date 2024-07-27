import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import GameResult from "@/shared/api/types/game-result.ts";

class GameApiService {
  private readonly gameResultApi = '/users/game-result';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async sendGameResult(score: number): Promise<Either<CommonResponseError, GameResult>> {
    return this.errorHandler.processRequest<GameResult>(async () => {
      const response = await this.client.post<GameResult>(
        this.gameResultApi,
        {"encrypted_information": score.toString()});
      return response.data;
    })
  }
}

export default GameApiService;