import {defineStore} from "pinia";
import {ref, Ref} from "vue";
import Task from "@/shared/api/types/task.ts";

export const useIncomeStore = defineStore('incomeStore', () => {
  const isLoading: Ref<boolean> = ref(false);
  const tasks: Ref<Task[]> = ref([]);

  const setLoading = (loading: boolean) => {
    isLoading.value = loading;
  }

  const setTasks = (tasksData: Task[]) => {
    tasks.value.length = 0;
    tasks.value.push(...tasksData);
  }

  return {
    isLoading,
    setLoading,
    tasks,
    setTasks,
  }
});