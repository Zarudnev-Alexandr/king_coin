import AxiosClientCreator from "@/shared/api/axios/axios-client.ts";

const baseUrl = 'https://wallapi.tappads.io/v1';
const axiosClientCreator = new AxiosClientCreator(baseUrl, true);

const axiosTappInstance = axiosClientCreator.makeAxiosClient();

export {
  axiosTappInstance,
}