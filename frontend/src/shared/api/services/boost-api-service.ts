import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import BoostUpgradeResponse from "@/shared/api/types/boost-upgrade-response.ts";

class BoostApiService {
  private readonly upgradeBoostApi = '/users/upgrade-boost';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async upgradeBoost(): Promise<Either<CommonResponseError, BoostUpgradeResponse>> {
    return this.errorHandler.processRequest<BoostUpgradeResponse>(async () => {
      const response = await this.client.post<BoostUpgradeResponse>(this.upgradeBoostApi);
      return response.data;
    })
  }
}

export default BoostApiService;