import Phaser from "phaser";
import {useGameStore} from "@/shared/pinia/game-store.ts";

export default class Player extends Phaser.GameObjects.Sprite {
  gameStore = useGameStore();

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'player');

    // Добавляем игрока на сцену
    scene.add.existing(this);

    // Включаем физику
    scene.physics.world.enable(this);
    this.setDisplaySize(106, 106);
    // Настраиваем физические свойства игрока00ы
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.body.setGravityY(500);
      this.body.setCollideWorldBounds(true);
    }

    scene.input.on('pointerdown', this.handleJump, this);
  }

  private handleJump() {
    if (this.gameStore.gameInitStarted === false) {
      this.gameStore.setGameInitStarted();
      this.gameStore.setPause(false);
    }

    if (this.gameStore.isPaused) return;
    (this.body as Phaser.Physics.Arcade.Body).setVelocityY(-250);
  }

  public stopMovement() {
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.body.setVelocity(0, 0); // Сбрасываем скорость
      this.body.setAcceleration(0, 0); // Сбрасываем ускорение
      this.body.setGravityY(0); // Отключаем гравитацию
    }
  }

  public disablePhysics() {
    this.stopMovement();
  }

  public enablePhysics() {
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.body.setGravityY(500);
      // Можно установить начальную скорость или оставить как есть
    }
  }
}
