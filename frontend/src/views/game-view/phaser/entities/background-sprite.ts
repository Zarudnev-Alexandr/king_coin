import Gameplay from "@/views/game-view/phaser/gameplay.ts";
import Phaser from "phaser";

class BackgroundTile extends Phaser.GameObjects.TileSprite {
  scene: Gameplay;

  constructor(scene: Phaser.Scene, x: number, y: number, height: number) {
    // Ширина задается по ширине экрана, высота по высоте экрана
    const width = scene.scale.width;
    super(scene, x, y, width, height, 'background');
    this.scene = scene as Gameplay;
    scene.add.existing(this);

    // Масштабируем изображение по высоте
    const originalHeight = 650;
    this.setScale(height / originalHeight);
  }

  update() {
    this.tilePositionX += 1; // Скорость прокрутки фона
  }
}

export default BackgroundTile;
