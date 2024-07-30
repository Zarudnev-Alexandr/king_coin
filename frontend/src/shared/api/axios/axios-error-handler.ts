import { AxiosError } from 'axios';
import { CommonResponseError, DefaultApiError, Either, ERROR_CODES } from '@/shared/api/axios/types.ts';

class AxiosErrorHandler {
  public async processRequest<T>(makeRequest: () => Promise<T>): Promise<Either<CommonResponseError, T>> {
    try {
      const response = await makeRequest();
      this.checkDataEmpty(response);

      return { right: response as T };
    } catch (error: any) {
      if (error.response && error.response.data && error.response.data.detail) {
        return { left: { message: error.response.data.detail } };
      }
      return { left: await this.processAxiosError(error as AxiosError) };
    }
  }

  private checkDataEmpty(data: any) {
    if (!data) throw Error('missing data');
  }

  private async processAxiosError(error: AxiosError): Promise<CommonResponseError> {
    if (error.code === ERROR_CODES.NO_NETWORK) {
      return { message: 'No network' };
    }

    const statusCode = error.response?.status;

    if (statusCode === ERROR_CODES.UNAUTHORIZED) {
      return { message: 'Unauthorized' };
    }

    if (statusCode === ERROR_CODES.TOO_MANY_REQUESTS) {
      return { message: 'Too many requests' };
    }

    let apiError: DefaultApiError | undefined;

    try {
      apiError = error.response?.data as DefaultApiError;
    } catch (e) {
      console.warn('Failed to parse API error', e);
    }

    return apiError ? { message: apiError.name } : { message: 'Undefined error' };
  }
}

export default AxiosErrorHandler;