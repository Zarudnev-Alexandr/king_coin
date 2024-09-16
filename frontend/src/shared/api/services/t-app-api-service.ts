import axios from "axios"; // Импортируем axios
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import FeedItem from "@/shared/api/types/feed-item.ts";

class TAppApiService {
  private readonly feeds = '/feed';
  private readonly apiKey = import.meta.env.VITE_TAPP_API_KEY;
  private readonly userAgent = navigator.userAgent;

  // Создаем экземпляр axios
  private readonly axiosInstance = axios.create({
    baseURL: 'https://wallapi.tappads.io/v1', // Замените на ваш базовый URL
    headers: {
      'Content-Type': 'application/json' // Заголовок для всех запросов
    }
  });

  constructor(private errorHandler: AxiosErrorHandler) {
  }

  public async getFeeds(): Promise<Either<CommonResponseError, FeedItem[]>> {
    const userId = 1567445; // Можно поменять id тут

    // Формируем параметры запроса
    const params = new URLSearchParams({
      user_id: userId.toString(),
      apikey: this.apiKey,
      ua: this.userAgent,
    }).toString();

    return this.errorHandler.processRequest<FeedItem[]>(async () => {
      const response = await this.axiosInstance.get<FeedItem[]>(`${this.feeds}?${params}`);
      return response.data;
    });
  }

  public async onClick(item: FeedItem): Promise<Either<CommonResponseError, {}>> {
    return this.errorHandler.processRequest<FeedItem[]>(async () => {
      const response = await this.axiosInstance.get<FeedItem[]>(item.click_postback);
      return response.data;
    });
  }

  public async check(item: FeedItem): Promise<boolean> {
    const res = await this.getFeeds();
    if (res && res.right) {
      let task = res.right.find(el => el.id === item.id)

      if (!task) return false;

      return task.is_done;
    }
    return false;
  }
}

export default TAppApiService;