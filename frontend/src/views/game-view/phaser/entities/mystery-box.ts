import {MysteryBoxType} from "@/shared/api/types/enums.ts";

class MysteryBox extends Phaser.Physics.Arcade.Sprite {
  type: MysteryBoxType = MysteryBoxType['5X'];

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x + 40, y, 'mystery-box');
    this.setDisplaySize(94, 94);
    this.type = this.getRandomMysteryBoxType();

    scene.add.existing(this);
    scene.physics.add.existing(this);
  }

  update() {
    if (this.x < -this.width) {
      this.destroy();
    }
  }

  getRandomMysteryBoxType = (): MysteryBoxType => {
    const types = Object.values(MysteryBoxType);
    const randomIndex = Math.floor(Math.random() * types.length);
    return types[randomIndex];
  }
}

export default MysteryBox;