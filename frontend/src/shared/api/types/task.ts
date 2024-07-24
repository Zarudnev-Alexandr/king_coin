interface Task {
  name: string;
  description: string;
  type: string;
  reward: number;
  requirement: number;
  link: string | null;
  id: number;
  completed: boolean;
}

export default Task;