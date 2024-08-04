import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import {Friend} from "@/shared/api/types/friend.ts";

class FriendsApiService {
  private readonly referralLinkApi = '/users/get-referral-link';
  private readonly friendsApi = '/users/invited-users';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getRefLink(): Promise<Either<CommonResponseError, { referral_link: string }>> {
    return this.errorHandler.processRequest<{ referral_link: string }>(async () => {
      const response = await this.client.get<{ referral_link: string }>(this.referralLinkApi);
      return response.data;
    })
  }

  public async getFriends(): Promise<Either<CommonResponseError, { invited_users: Friend[] }>> {
    return this.errorHandler.processRequest<{ invited_users: Friend[] }>(async () => {
      const response = await this.client.get<{ invited_users: Friend[] }>(this.friendsApi);
      return response.data;
    })
  }
}

export default FriendsApiService;