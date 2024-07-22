import AxiosClientCreator from "@/shared/api/axios/axios-client.ts";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";

const baseUrl = import.meta.env.VITE_BASE_URL;
const axiosClientCreator = new AxiosClientCreator(baseUrl, true);

const axiosInstance = axiosClientCreator.makeAxiosClient();
const errorHandler = new AxiosErrorHandler();

export {
  axiosInstance,
  errorHandler
}