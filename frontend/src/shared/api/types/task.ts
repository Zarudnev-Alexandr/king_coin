interface Task {
  name: string;
  english_description: string;
  description: string;
  type: string;
  reward: number;
  image_url: string;
  requirement: number;
  link: string | null;
  id: number;
  completed: boolean;
  end_time: string | null;
}

export default Task;