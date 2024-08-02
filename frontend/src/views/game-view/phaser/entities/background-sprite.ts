import Phaser from "phaser";

class BackgroundTile extends Phaser.GameObjects.Container {
  scene: Phaser.Scene;
  canvas: HTMLCanvasElement;
  context: CanvasRenderingContext2D;
  image: HTMLImageElement;
  tileWidth: number;
  tileHeight: number;
  speed: number;
  xOffset: number;
  bgSprites: Phaser.GameObjects.Sprite[];
  screenHeight: number;

  constructor(scene: Phaser.Scene, x: number, y: number, height: number) {
    super(scene, x, y);
    this.scene = scene;
    this.speed = 0.2;
    this.xOffset = 0;
    this.screenHeight = height;

    const texture = scene.textures.get('background');
    const source = texture.getSourceImage();

    if (!(source instanceof HTMLImageElement)) {
      throw new Error('Expected image source to be an HTMLImageElement');
    }

    this.image = source;
    this.tileWidth = this.image.width;
    this.tileHeight = this.image.height;

    // Используем максимальный размер текстуры 4096
    const maxTextureSize = 4096;
    console.log('Max texture size:', maxTextureSize);

    // Размеры канваса для части изображения
    this.canvas = document.createElement('canvas');
    this.context = this.canvas.getContext('2d')!;
    this.canvas.width = Math.min(maxTextureSize, this.tileWidth);
    this.canvas.height = this.screenHeight;

    this.bgSprites = [];

    // Удаляем старые текстуры, если они существуют
    if (scene.textures.exists('backgroundCanvas')) {
      scene.textures.remove('backgroundCanvas');
    }

    // Отрисовываем изображение на канвасе
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.context.drawImage(
      this.image,
      0, 0, this.tileWidth, Math.min(this.screenHeight, this.tileHeight),
      0, 0, this.canvas.width, this.canvas.height
    );

    const textureCanvas = scene.textures.createCanvas('backgroundCanvas', this.canvas.width, this.canvas.height);
    textureCanvas?.context.drawImage(this.canvas, 0, 0);
    textureCanvas?.refresh();

    // Создаем два спрайта для плавного перехода
    for (let i = 0; i < 2; i++) {
      const sprite = scene.add.sprite(x + i * this.canvas.width, y, 'backgroundCanvas').setOrigin(0, 0);
      sprite.setDisplaySize(this.canvas.width, this.canvas.height);
      this.bgSprites.push(sprite);
      this.add(sprite);
    }

    scene.add.existing(this);
  }

  update() {
    this.xOffset -= this.speed;
    if (this.xOffset <= -this.canvas.width) {
      this.xOffset += this.canvas.width;
    }

    // Обновляем позиции всех спрайтов
    this.bgSprites.forEach((sprite, index) => {
      sprite.setX(this.xOffset + index * this.canvas.width);
    });
  }
}

export default BackgroundTile;

