import {defineStore} from "pinia";
import {ref, Ref} from "vue";
import Task from "@/shared/api/types/task.ts";
import TaskDaily from "@/shared/api/types/task-daily.ts";

export const useIncomeStore = defineStore('incomeStore', () => {
  const isLoading: Ref<boolean> = ref(false);
  const tasks: Ref<Task[]> = ref([]);
  const dailyTask: Ref<TaskDaily | null> = ref(null);

  const setLoading = (loading: boolean) => {
    isLoading.value = loading;
  }

  const setTasks = (tasksData: Task[]) => {
    tasks.value.length = 0;
    tasks.value.push(...tasksData);
  }

  const setDailyTask = (dailyTaskData: TaskDaily) => {
    dailyTask.value = dailyTaskData;
  }

  const claimDailyTask = () => {
    if (dailyTask.value)
      dailyTask.value!.is_collect = true;
  }

  const taskCompleted = (taskId: number) => {
    const task = tasks.value.find(task => task.id === taskId);
    if (task) {
      task.completed = true;
    }
  }

  return {
    isLoading,
    setLoading,
    tasks,
    setTasks,
    dailyTask,
    setDailyTask,
    claimDailyTask,
    taskCompleted,
  }
});