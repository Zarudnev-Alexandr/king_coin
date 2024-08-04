import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import {User} from "@/shared/api/types/user.ts";
import {AxiosInstance} from "axios";

class UserApiService {
  private userApi = '/users/logreg';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getCurrentUser(ref: string | undefined | null): Promise<Either<CommonResponseError, User>> {
    if (ref) {
      this.userApi += `?ref=${ref}`;
    }

    return this.errorHandler.processRequest<User>(async () => {
      const response = await this.client.post<User>(this.userApi);
      return response.data;
    })
  }
}

export default UserApiService;
