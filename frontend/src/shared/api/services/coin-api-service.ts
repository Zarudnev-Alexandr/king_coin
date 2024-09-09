import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {AxiosInstance} from "axios";
import {CoinCategory} from "@/shared/api/types/coin-category.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import CoinUpgradeResponse from "@/shared/api/types/coin-upgrade-response.ts";
import {Coin} from "@/shared/api/types/coin.ts";

class CoinApiService {
  private readonly categoryAllApi = '/upgrades/upgrade-category/all';
  private readonly upgradeCoinApi = '/upgrades/buy-upgrade';
  private readonly checkIsAvailableApi = '/upgrades/can-i-buy-upgrade';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getCategories(): Promise<Either<CommonResponseError, CoinCategory[]>> {
    return this.errorHandler.processRequest<CoinCategory[]>(async () => {
      const response = await this.client.get<CoinCategory[]>(this.categoryAllApi);
      return response.data;
    })
  }

  public async upgradeCoin(coinId: number, userId: number): Promise<Either<CommonResponseError, CoinUpgradeResponse>> {
    return this.errorHandler.processRequest<CoinUpgradeResponse>(async () => {
      const response = await this.client.post(this.upgradeCoinApi, {user_id: userId, upgrade_id: coinId});
      return response.data;
    })
  }

  public async checkIsAvailable(coin: Coin): Promise<Either<CommonResponseError, { detail: string }>> {
    return this.errorHandler.processRequest<{ detail: string }>(async () => {
      const response = await this.client.get(`${this.checkIsAvailableApi}?upgrade_id=${coin.id}`);
      return response.data;
    })
  }
}

export default CoinApiService;