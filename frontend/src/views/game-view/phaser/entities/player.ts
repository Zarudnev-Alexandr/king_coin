import Phaser from "phaser";
import {useGameStore} from "@/shared/pinia/game-store.ts";

export default class Player extends Phaser.GameObjects.Sprite {
  gameStore = useGameStore();

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'player');

    scene.add.existing(this);
    scene.physics.world.enable(this);

    this.setDisplaySize(106, 85);
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
    (this.body as Phaser.Physics.Arcade.Body).setVelocityY(-300);
  }

  public stopMovement() {
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.body.setVelocity(0, 0);
      this.body.setAcceleration(0, 0);
      this.body.setGravityY(0);
    }
  }

  public disablePhysics() {
    this.stopMovement();
  }

  public enablePhysics() {
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.body.setGravityY(600);
    }
  }
}
