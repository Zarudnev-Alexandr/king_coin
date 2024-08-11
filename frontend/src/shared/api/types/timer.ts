class Timer {
  private remainingTime: number;
  private callback: () => void;
  private isActive: boolean;

  constructor(delay: number, callback: () => void) {
    this.remainingTime = delay;
    this.callback = callback;
    this.isActive = true;
  }

  update(delta: number) {
    if (!this.isActive) return;

    this.remainingTime -= delta;
    if (this.remainingTime <= 0) {
      this.callback();
      this.isActive = false;
    }
  }

  stop() {
    this.isActive = false;
  }
}

export default Timer;