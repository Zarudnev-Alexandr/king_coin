import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {AxiosInstance} from "axios";
import {CoinCategory} from "@/shared/api/types/coin-category.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";

class CoinApiService {
  private readonly categoryAllApi = '/upgrades/upgrade-category/all';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getCategories(): Promise<Either<CommonResponseError, CoinCategory[]>> {
    return this.errorHandler.processRequest<CoinCategory[]>(async () => {
      const response = await this.client.get<CoinCategory[]>(this.categoryAllApi);
      return response.data;
    })
  }
}

export default CoinApiService;