import {defineStore} from "pinia";
import {ref, Ref} from "vue";
import Task from "@/shared/api/types/task.ts";
import TaskDaily from "@/shared/api/types/task-daily.ts";
import FeedItem from "@/shared/api/types/feed-item.ts";

export const useIncomeStore = defineStore('incomeStore', () => {
  const isLoading: Ref<boolean> = ref(false);
  const tAppTaskLoading = ref(false);
  const tasks: Ref<Task[]> = ref([]);
  const tAppTasks: Ref<FeedItem[]> = ref([]);
  const dailyTask: Ref<TaskDaily | null> = ref(null);

  const setLoading = (loading: boolean) => {
    isLoading.value = loading;
  }

  const setTAppTaskLoading = (loading: boolean) => {
    tAppTaskLoading.value = loading;
  }

  const setTasks = (tasksData: Task[]) => {
    tasks.value.length = 0;
    tasks.value.push(...tasksData);
  }

  const setTAppTasks = (tasks: FeedItem[]) => {
    tAppTasks.value.length = 0;
    tAppTasks.value.push(...tasks);
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
    tAppTaskLoading,
    setTAppTaskLoading,
    tAppTasks,
    setTAppTasks,
  }
});