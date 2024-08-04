import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import {User} from "@/shared/api/types/user.ts";
import {AxiosInstance} from "axios";
import {useRoute} from "vue-router";

class UserApiService {
  private userApi = '/users/logreg';
  private route = useRoute();

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getCurrentUser(): Promise<Either<CommonResponseError, User>> {

    if (this.route.query.ref) {
      this.userApi += `?ref=${this.route.query.ref}`;
    }

    return this.errorHandler.processRequest<User>(async () => {
      const response = await this.client.post<User>(this.userApi);
      return response.data;
    })
  }
}

export default UserApiService;
