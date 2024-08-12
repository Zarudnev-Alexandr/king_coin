import Phaser from 'phaser';
import ObstacleTopPipe from "@/views/game-view/phaser/entities/obstacle-top-pipe.ts";
import ObstacleBottomPipe from "@/views/game-view/phaser/entities/obstacle-bottom-pipe.ts";
import {useGameStore} from "@/shared/pinia/game-store.ts";
import CoinReward from "@/views/game-view/phaser/entities/coin-reward.ts";
import MysteryBox from "@/views/game-view/phaser/entities/mystery-box.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";


class ObstacleManager {
  gameStore = useGameStore();
  userStore = useUserStore();
  private readonly scene: Phaser.Scene;
  public obstacles: Phaser.Physics.Arcade.Group;
  public rewards: Phaser.Physics.Arcade.Group;
  public mysteryBoxes: Phaser.Physics.Arcade.Group;
  private level: number;
  private obstacleCount: number;
  private distanceBetweenPipesY: number;
  private distanceBetweenPipesX: number;
  private distanceBetweenPairs: number;
  private timeSinceLastObstacle: number;
  private speed: number;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.obstacles = this.scene.physics.add.group();
    this.rewards = this.scene.physics.add.group();
    this.mysteryBoxes = this.scene.physics.add.group();
    this.level = 1;
    this.obstacleCount = 0;
    this.distanceBetweenPipesY = 350;
    this.distanceBetweenPipesX = 150;
    this.distanceBetweenPairs = 500;
    this.timeSinceLastObstacle = 0;
    this.speed = -120;
  }

  private createObstaclePair() {
    let randomStart = ((this.scene.scale.height - this.distanceBetweenPipesY) / 2) - 50;
    const pipeTopY = Phaser.Math.Between(randomStart, randomStart + 100);
    const pipeBottomY = pipeTopY + this.distanceBetweenPipesY;
    const rewardY = pipeTopY + ((pipeBottomY - pipeTopY) / 2);

    const pipeTop = new ObstacleTopPipe(this.scene, this.scene.scale.width, pipeTopY)
    const pipeBottom = new ObstacleBottomPipe(this.scene, this.scene.scale.width, pipeBottomY)
    let rewardCoin = null;
    let mysteryBox = null;

    if (this.obstacleCount === 1 || this.obstacleCount === 9 || this.obstacleCount === 29 || this.obstacleCount === 99) {
      let reward = 200;

      if (this.obstacleCount === 9 && this.userStore.user) {
        reward = this.userStore.user?.boost.pillars_10;
      } else if (this.obstacleCount === 29 && this.userStore.user) {
        reward = this.userStore.user?.boost.pillars_30;
      } else if (this.obstacleCount === 99 && this.userStore.user) {
        reward = this.userStore.user?.boost.pillars_100;
      }

      rewardCoin = new CoinReward(this.scene, this.scene.scale.width + (this.distanceBetweenPipesX / 2), rewardY, reward);
    }

    if (this.obstacleCount === 15 || this.obstacleCount === 33 || this.obstacleCount === 78) {
      mysteryBox = new MysteryBox(this.scene, this.scene.scale.width + (this.distanceBetweenPipesX / 2), rewardY);
    }

    this.obstacles.add(pipeTop);
    this.obstacles.add(pipeBottom);

    if (rewardCoin)
      this.rewards.add(rewardCoin);

    if (mysteryBox)
      this.mysteryBoxes.add(mysteryBox);

    if (!this.gameStore.isPaused) {
      pipeTop.setVelocityX(this.speed);
      pipeBottom.setVelocityX(this.speed);

      if (rewardCoin)
        rewardCoin.setVelocityX(this.speed);

      if (mysteryBox)
        mysteryBox.setVelocityX(this.speed);
    }

    this.obstacleCount++;
    this.checkLevelUp();
  }

  private checkLevelUp() {
    if (this.obstacleCount === 0) {
      this.distanceBetweenPairs = 500
    } else if (this.level === 1 && this.obstacleCount < 5) {
      this.distanceBetweenPairs = 3000;
    } else if (this.level === 1 && this.obstacleCount >= 5) {
      this.level = 2;
      this.distanceBetweenPipesY = 350;
    } else if (this.level === 2 && this.obstacleCount >= 10) {
      this.level = 3;
      this.distanceBetweenPipesY = 300;
      this.distanceBetweenPairs = 2500;
    } else if (this.level === 3 && this.obstacleCount >= 16) {
      this.level = 4;
      this.distanceBetweenPipesY = 250;
      this.distanceBetweenPairs = 2000;
    } else if (this.level === 4 && this.obstacleCount >= 20) {
      this.level = 5;
      this.distanceBetweenPipesY = 200;
      this.distanceBetweenPairs = 1500;
    }
  }

  setVelocityX(velocity: number) {
    this.speed = velocity;

    if (this.speed === -300) {
      this.distanceBetweenPairs = 1200;
    } else {
      this.checkLevelUp();
    }

    this.obstacles.setVelocityX(this.speed);
    this.rewards.setVelocityX(this.speed);
    this.mysteryBoxes.setVelocityX(this.speed);
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
