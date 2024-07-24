import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import Combo from "@/shared/api/types/combo.ts";

class ComboApiService {
  private readonly getComboApi = '/upgrades/user-combo';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getComboData(): Promise<Either<CommonResponseError, Combo>> {
    return await this.errorHandler.processRequest<Combo>(async () => {
      const response = await this.client.get<any>(this.getComboApi);

      if (response.data.detail) {
        throw new Error(response.data.detail);
      }

      return response.data as Combo;
    })
  }
}

export default ComboApiService;