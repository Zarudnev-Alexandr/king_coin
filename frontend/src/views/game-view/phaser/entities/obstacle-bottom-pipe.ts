import Gameplay from "../gameplay.ts";

class ObstacleBottomPipe extends Phaser.Physics.Arcade.Sprite {
  scene: Gameplay

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x + 40, y, 'bottomPipe');

    this.setOrigin(0.5, 0);
    this.scene = scene as Gameplay
    scene.add.existing(this);
    scene.physics.add.existing(this);
    this.setDisplaySize(74, 451);
  }

  update() {
    if (this.x < -this.width) {
      this.destroy();
    }
  }
}

export default ObstacleBottomPipe;