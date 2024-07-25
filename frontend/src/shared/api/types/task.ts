interface Task {
  name: string;
  description: string;
  type: string;
  reward: number;
  requirement: number;
  link: string | null;
  id: number;
  completed: boolean;
  end_time: string | null;
}

export default Task;