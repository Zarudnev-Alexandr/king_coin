import {Levels} from "@/shared/constants/levels.ts";

function getLevelByIndex(index: number): { lvl: number, name: string, reward: number, image: string } {
  return Levels[index - 1];
}

function getIncomeSumByLevel(level: number): number {
  let sum = 0;
  for (let i = 0; i < level; i++) {
    sum += Levels[i].reward;
  }
  return sum;
}

export {
  getLevelByIndex,
  getIncomeSumByLevel
}