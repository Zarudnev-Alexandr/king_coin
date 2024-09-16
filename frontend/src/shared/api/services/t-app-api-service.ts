import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import FeedItem from "@/shared/api/types/feed-item.ts";

class TAppApiService {
  private readonly feeds = '/feed'
  private readonly apiKey = import.meta.env.VITE_TAPP_API_KEY;

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
    this.client.defaults.headers.common['initData'] = '';
  }

  public async getFeeds(): Promise<Either<CommonResponseError, FeedItem[]>> {
    const params = `user_id=${1567445}&apikey=${this.apiKey}` // Todo error надо id поменять
    return this.errorHandler.processRequest<FeedItem[]>(async () => {
      const response = await this.client.get<FeedItem[]>(`${this.feeds}?${params}`);
      return response.data;
    })
  }
}

export default TAppApiService;