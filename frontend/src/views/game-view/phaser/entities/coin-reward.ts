class CoinReward extends Phaser.Physics.Arcade.Sprite {
  reward: number = 1;

  constructor(scene: Phaser.Scene, x: number, y: number, reward: number) {
    super(scene, x + 40, y, 'coin');
    this.setDisplaySize(68, 68);
    this.reward = reward;

    scene.add.existing(this);
    scene.physics.add.existing(this);
  }

  update() {
    if (this.x < -this.width) {
      this.destroy();
    }
  }
}

export default CoinReward;