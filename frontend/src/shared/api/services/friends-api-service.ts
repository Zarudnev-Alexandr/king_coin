import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";

class FriendsApiService {
  private readonly referralLinkApi = '/users/get-referral-link';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getRefLink(): Promise<Either<CommonResponseError, {referral_link: string}>> {
    return this.errorHandler.processRequest<{referral_link: string}>(async () => {
      const response = await this.client.get<{referral_link: string}>(this.referralLinkApi);
      return response.data;
    })
  }
}

export default FriendsApiService;