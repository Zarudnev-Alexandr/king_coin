import Phaser from 'phaser';
import ObstacleTopPipe from "@/views/game-view/phaser/entities/obstacle-top-pipe.ts";
import ObstacleBottomPipe from "@/views/game-view/phaser/entities/obstacle-bottom-pipe.ts";
import {useGameStore} from "@/shared/pinia/game-store.ts";

class ObstacleManager {
  gameStore = useGameStore();
  private readonly scene: Phaser.Scene;
  public obstacles: Phaser.Physics.Arcade.Group;
  private level: number;
  private obstacleCount: number;
  private distanceBetweenPipesY: number;
  private distanceBetweenPipesX: number;
  private distanceBetweenPairs: number;
  private timeSinceLastObstacle: number;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.obstacles = this.scene.physics.add.group();
    this.level = 1;
    this.obstacleCount = 0;
    this.distanceBetweenPipesY = 350;
    this.distanceBetweenPipesX = 150;
    this.distanceBetweenPairs = 3000;
    this.timeSinceLastObstacle = 0;
  }

  private createObstaclePair() {
    const pipeTopY = Phaser.Math.Between(50, 100);
    const pipeBottomY = pipeTopY + this.distanceBetweenPipesY;

    const pipeTop = new ObstacleTopPipe(this.scene, this.scene.scale.width, pipeTopY)
    const pipeBottom = new ObstacleBottomPipe(this.scene, this.scene.scale.width + this.distanceBetweenPipesX, pipeBottomY)

    this.obstacles.add(pipeTop);
    this.obstacles.add(pipeBottom);

    if (!this.gameStore.isPaused) {
      pipeTop.setVelocityX(-120);
      pipeBottom.setVelocityX(-120);
    }

    this.obstacleCount++;
    this.checkLevelUp();
  }

  private checkLevelUp() {
    if (this.level === 1 && this.obstacleCount >= 5) {
      this.level = 2;
      this.distanceBetweenPipesY = 350;
    } else if (this.level === 2 && this.obstacleCount >= 10) {
      this.level = 3;
      this.distanceBetweenPipesY = 300;
      this.distanceBetweenPairs = 2500;
    } else if (this.level === 3 && this.obstacleCount >= 15) {
      this.level = 4;
      this.distanceBetweenPipesY = 250;
      this.distanceBetweenPairs = 2000;
      this.distanceBetweenPipesX = 0;
    } else if (this.level === 4 && this.obstacleCount >= 20) {
      this.level = 5;
      this.distanceBetweenPipesY = 200;
      this.distanceBetweenPairs = 1500;
    }
  }

  setVelocityX(velocity: number) {
    this.obstacles.setVelocityX(velocity);
  }

  update(_: number, delta: number) {
    this.timeSinceLastObstacle += delta;

    if (this.timeSinceLastObstacle >= this.distanceBetweenPairs) {
      this.createObstaclePair();
      this.timeSinceLastObstacle = 0;
    }
  }
}

export default ObstacleManager;
