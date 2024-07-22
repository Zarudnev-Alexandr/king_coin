export type Either<L, R> = { left?: L; right?: R };

// Константы для кодов ошибок
export const ERROR_CODES = {
  NO_NETWORK: 'ECONNABORTED',
  UNAUTHORIZED: 401,
  TOO_MANY_REQUESTS: 429,
};

export interface CommonResponseError {
  message: string;
}


export interface DefaultApiError {
  name: string;
  code: string;
}

export class DataStructureError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'DataStructureError';
  }
}
