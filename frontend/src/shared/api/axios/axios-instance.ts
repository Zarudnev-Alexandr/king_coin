import AxiosClientCreator from "@/shared/api/axios/axios-client.ts";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";

const baseUrl = 'https://king-coin.online/api';
const axiosClientCreator = new AxiosClientCreator(baseUrl, true);

const axiosInstance = axiosClientCreator.makeAxiosClient();
const errorHandler = new AxiosErrorHandler();

export {
  axiosInstance,
  errorHandler
}