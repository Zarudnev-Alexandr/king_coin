import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";

class FriendsApiService {
  private readonly referralLinkApi = '/users/get-referral-link';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getRefLink(): Promise<Either<CommonResponseError, {referral_ling: string}>> {
    return this.errorHandler.processRequest<{referral_ling: string}>(async () => {
      const response = await this.client.get<{referral_ling: string}>(this.referralLinkApi);
      return response.data;
    })
  }
}

export default FriendsApiService;