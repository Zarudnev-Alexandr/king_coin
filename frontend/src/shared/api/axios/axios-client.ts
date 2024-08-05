import axios, {AxiosInstance, AxiosError, AxiosRequestConfig} from 'axios';
import log from 'loglevel';
import './axios-extended.d.ts'; // Импортируем расширение типов

class AxiosClientCreator {
  private defaultConnectTimeout = 25000;

  constructor(private baseURL: string, private enableLogs: boolean) {
  }

  public makeAxiosClient(): AxiosInstance {
    const testInitData = "query_id=AAFOE9phAgAAAE4T2mELCGHs&user=%7B%22id%22%3A5936649038%2C%22first_name%22%3A%22Last%22%2C%22last_name%22%3A%22%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1722801085&hash=44ccde3a7cb1eac019a4d4912933c32c472f385b056110e07a76bf300a406c07"
    ;
    const instance = axios.create({
      baseURL: this.baseURL,
      timeout: this.defaultConnectTimeout,
      headers: {
        'Content-Type': 'application/json',
        'initData': Telegram.WebApp.initData !== '' ? JSON.stringify(Telegram.WebApp.initData) : testInitData,
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

    // Add retry logic interceptor
    instance.interceptors.response.use(
      response => response,
      async (error: AxiosError) => {
        const config = error.config as AxiosRequestConfig & { _retryCount?: number };
        log.error('Request failed:', error);

        // Retry logic
        const shouldRetry = error.code === 'ECONNABORTED' || error.response?.status === 500 || error.message === 'Network Error';
        if (shouldRetry) {
          config._retryCount = (config._retryCount || 0) + 1;
          if (config._retryCount < 3) {
            log.warn(`Retrying request... attempt #${config._retryCount}`);
            return new Promise((resolve) => setTimeout(() => resolve(instance(config)), 1000)); // Retry after 1 second
          }
        }

        return Promise.reject(error);
      }
    );

    return instance;
  }
}

export default AxiosClientCreator;
