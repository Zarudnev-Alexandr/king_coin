class ObstacleTopPipe extends Phaser.Physics.Arcade.Sprite {
  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x + 40, y, 'topPipe');
    this.setDisplaySize(74, 451);

    this.setOrigin(0.5, 1);
    scene.add.existing(this);
    scene.physics.add.existing(this);
  }

  update() {
    if (this.x < -this.width) {
      this.destroy();
    }
  }
}

export default ObstacleTopPipe;