import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import Task from "@/shared/api/types/task.ts";

class TasksApiService {
  private readonly taskApi = '/tasks/tasks';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getTasks(): Promise<Either<CommonResponseError, Task[]>> {
    return this.errorHandler.processRequest<Task[]>(async () => {
      const response = await this.client.get<Task[]>(this.taskApi);
      return response.data;
    })
  }
}

export default TasksApiService;