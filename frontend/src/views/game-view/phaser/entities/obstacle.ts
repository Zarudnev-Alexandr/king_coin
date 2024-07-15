import Phaser from "phaser";

export default class Obstacle extends Phaser.GameObjects.Container {
  private readonly topPipe: Phaser.Physics.Arcade.Image;
  private readonly bottomPipe: Phaser.Physics.Arcade.Image;

  constructor(scene: Phaser.Scene, x: number, y: number, gap: number) {
    super(scene, x, y);

    // Загрузка изображений труб
    this.topPipe = scene.physics.add.image(0, -gap / 2, 'topPipe');
    this.bottomPipe = scene.physics.add.image(0, gap / 2, 'bottomPipe');
    this.topPipe.setDisplaySize(78, 297);
    this.bottomPipe.setDisplaySize(75, 283);

    // Добавление труб в контейнер
    this.add(this.topPipe);
    this.add(this.bottomPipe);

    // Добавление контейнера на сцену
    scene.add.existing(this);
    scene.physics.world.enable(this);

    // Настройка физики для труб
    this.topPipe.setVelocityX(-200);
    this.bottomPipe.setVelocityX(-200);
  }

  public disablePhysics() {
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.topPipe.setVelocityX(0);
      this.bottomPipe.setVelocityX(0);
    }
  }

  public enablePhysics() {
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.topPipe.setVelocityX(-200);
      this.bottomPipe.setVelocityX(-200);
    }
  }

  update() {
    // Удаление препятствия, если оно выходит за пределы экрана
    if (this.x < -this.topPipe.width) {
      this.destroy();
    }
  }
}
