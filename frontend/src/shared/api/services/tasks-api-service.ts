import {AxiosInstance} from "axios";
import AxiosErrorHandler from "@/shared/api/axios/axios-error-handler.ts";
import {CommonResponseError, Either} from "@/shared/api/axios/types.ts";
import Task from "@/shared/api/types/task.ts";
import TaskDaily from "@/shared/api/types/task-daily.ts";
import TaskDailyClaim from "@/shared/api/types/task-daily-claim.ts";
import CheckTask from "@/shared/api/types/check-task.ts";
import {UserCheck} from "@/shared/api/types/user-check.ts";

class TasksApiService {
  private readonly taskApi = '/tasks/tasks';
  private readonly dailyTaskApi = '/users/daily-reward';
  private readonly dailyClaimApi = '/users/claim-daily-reward';
  private readonly checkTaskApi = '/tasks/check/';
  private readonly confirmWatchAd = '/users/watch-ad';
  private readonly startGenericTask = '/tasks/start_generic';

  constructor(private client: AxiosInstance, private errorHandler: AxiosErrorHandler) {
  }

  public async getTasks(): Promise<Either<CommonResponseError, Task[]>> {
    return this.errorHandler.processRequest<Task[]>(async () => {
      const response = await this.client.get<Task[]>(this.taskApi);
      return response.data;
    })
  }

  public async getDailyTaskInfo(): Promise<Either<CommonResponseError, TaskDaily>> {
    return this.errorHandler.processRequest<TaskDaily>(async () => {
      const response = await this.client.get<TaskDaily>(this.dailyTaskApi);
      return response.data;
    })
  }

  public async claimDailyTask(): Promise<Either<CommonResponseError, TaskDailyClaim>> {
    return this.errorHandler.processRequest<TaskDailyClaim>(async () => {
      const response = await this.client.post<TaskDailyClaim>(this.dailyClaimApi);
      return response.data;
    })
  }

  public async checkTask(id: number): Promise<Either<CommonResponseError, CheckTask>> {
    return this.errorHandler.processRequest<CheckTask>(async () => {
      const response = await this.client.post<CheckTask>(this.checkTaskApi + id);
      return response.data;
    })
  }

  public async confirmWatchedAd(): Promise<Either<CommonResponseError, { message: string, user_check: UserCheck }>> {
    return this.errorHandler.processRequest<{ message: string, user_check: UserCheck }>(async () => {
      const response = await this.client.post<{ message: string, user_check: UserCheck }>(this.confirmWatchAd);
      return response.data;
    })
  }

  public async startGeneric(id: number): Promise<Either<CommonResponseError, { message: string }>> {
    return this.errorHandler.processRequest<{ message: string }>(async () => {
      const response = await this.client.post<{ message: string }>(`${this.startGenericTask}/${id}`);
      return response.data;
    })
  }
}

export default TasksApiService;