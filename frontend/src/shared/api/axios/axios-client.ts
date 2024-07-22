import axios, {AxiosInstance} from "axios";
import log from "loglevel";

class AxiosClientCreator {
  private defaultConnectTimeout = 15000;

  // private defaultReceiveTimeout = 25000;

  constructor(private baseURL: string, private enableLogs: boolean) {
  }

  public makeAxiosClient(): AxiosInstance {
    const instance = axios.create({
      baseURL: this.baseURL,
      timeout: this.defaultConnectTimeout,
      headers: {
        'Content-Type': 'application/json',
        'initData': Telegram.WebApp.initData !== '' ? JSON.stringify(Telegram.WebApp.initDataUnsafe.user) : '{"allows_write_to_pm": true, "first_name": "firstname", "id": 905351175, "language_code": "ru", "last_name": "", "username": "c2dent"}',
      },
    });

    if (this.enableLogs) {
      instance.interceptors.request.use(request => {
        log.info('Starting Request', request);
        return request;
      });

      instance.interceptors.response.use(response => {
        log.info('Response:', response);
        return response;
      });
    }

    return instance;
  }
}

export default AxiosClientCreator;