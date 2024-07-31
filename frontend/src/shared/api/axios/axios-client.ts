import axios, { AxiosInstance, AxiosError, AxiosRequestConfig } from 'axios';
import log from 'loglevel';
import './axios-extended.d.ts'; // Импортируем расширение типов

class AxiosClientCreator {
  private defaultConnectTimeout = 25000;

  constructor(private baseURL: string, private enableLogs: boolean) {}

  public makeAxiosClient(): AxiosInstance {
    const instance = axios.create({
      baseURL: this.baseURL,
      timeout: this.defaultConnectTimeout,
      headers: {
        'Content-Type': 'application/json',
        'initData': Telegram.WebApp.initData !== '' ? JSON.stringify(Telegram.WebApp.initDataUnsafe.user) : '{"allows_write_to_pm": true, "first_name": "firstname", "id": 7099, "language_code": "ru", "last_name": "", "username": "c2dent"}',
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
