import Phaser from 'phaser';

export default class BackgroundSprite {
  private scene: Phaser.Scene;
  private backgrounds: Phaser.GameObjects.Image[] = [];
  private readonly speed: number;
  private readonly screenHeight: number;

  constructor(scene: Phaser.Scene, backgroundKey1: string, backgroundKey2: string, speed: number) {
    this.scene = scene;
    this.speed = speed;
    this.screenHeight = this.scene.scale.height;

    const scaleFactor1 = this.getScaleFactor(backgroundKey1);
    const scaleFactor2 = this.getScaleFactor(backgroundKey2);

    const background1 = this.scene.add.image(0, 0, backgroundKey1).setOrigin(0, 0).setScale(scaleFactor1);
    const background2 = this.scene.add.image(background1.displayWidth - 2, 0, backgroundKey2).setOrigin(0, 0).setScale(scaleFactor2);

    this.backgrounds.push(background1, background2);
  }

  private getScaleFactor(backgroundKey: string): number {
    const originalHeight = this.scene.textures.get(backgroundKey).getSourceImage().height;
    return this.screenHeight / originalHeight;
  }

  public update(): void {
    this.backgrounds.forEach((background, index) => {
      background.x -= this.speed;

      if (background.x + background.displayWidth <= 0) {
        const otherBackground = this.backgrounds[(index + 1) % this.backgrounds.length];
        background.x = otherBackground.x + otherBackground.displayWidth - 5;
      }
    });
  }
}