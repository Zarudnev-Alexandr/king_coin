export class LocalStorageService<T> {
  private readonly storageKey: string;

  constructor(storageKey: string) {
    this.storageKey = storageKey;
  }

  setItem(item: T): void {
    try {
      const serializedItem = JSON.stringify(item);
      localStorage.setItem(this.storageKey, serializedItem);
    } catch (error) {
      console.error(`Error setting item in localStorage: ${error}`);
    }
  }

  getItem(): T | null {
    try {
      const serializedItem = localStorage.getItem(this.storageKey);
      if (serializedItem === null) {
        return null;
      }
      return JSON.parse(serializedItem) as T;
    } catch (error) {
      console.error(`Error getting item from localStorage: ${error}`);
      return null;
    }
  }

  removeItem(): void {
    try {
      localStorage.removeItem(this.storageKey);
    } catch (error) {
      console.error(`Error removing item from localStorage: ${error}`);
    }
  }

  clear(): void {
    try {
      localStorage.clear();
    } catch (error) {
      console.error(`Error clearing localStorage: ${error}`);
    }
  }
}
