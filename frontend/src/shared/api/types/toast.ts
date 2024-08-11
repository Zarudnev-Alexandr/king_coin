enum ToastType {
  SUCCESS = 'success',
  ERROR = 'error',
  WARNING = 'warning',
}

class Toast {
  type: ToastType;
  message: string;

  constructor(type: ToastType, message: string) {
    this.type = type;
    this.message = message;
  }
}

export { Toast, ToastType };