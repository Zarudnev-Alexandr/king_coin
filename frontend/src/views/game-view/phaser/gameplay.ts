import BackgroundImage from "@/assets/img/game/background.png"
import BackgroundSprite from "@/views/game-view/phaser/entities/background-sprite.ts";
import PlayerImage from "@/assets/img/game/player.png"
import Player from "@/views/game-view/phaser/entities/player.ts";
import TopPipeImage from "@/assets/img/game/top-pipe.png"
import BottomPipeImage from "@/assets/img/game/bottom-pipe.png"
import Obstacle from "@/views/game-view/phaser/entities/obstacle.ts";
import {useGameStore} from "@/shared/pinia/game-store.ts";

class Gameplay extends Phaser.Scene {
  private background?: BackgroundSprite;
  private player?: Player;
  private obstacles?: Phaser.Physics.Arcade.Group;
  private gameStore = useGameStore();
  static instance: Gameplay | null = null;

  constructor() {
    super('Gameplay');
    console.log("########################")
    Gameplay.instance = this;
  }

  preload() {
    this.load.image('background', BackgroundImage);
    this.load.image('player', PlayerImage);
    this.load.image('topPipe', TopPipeImage);
    this.load.image('bottomPipe', BottomPipeImage);
  }

  create() {
    this.background = new BackgroundSprite(this, 0, 0, this.scale.height);
    this.background.setOrigin(0, 0);
    this.player = new Player(this, 100, this.scale.height / 2);

    this.obstacles = this.physics.add.group({
      classType: Obstacle,
      runChildUpdate: true // Включаем автоматическое обновление для всех детей группы
    });

    // Периодическое создание препятствий
    this.time.addEvent({
      delay: 2000, // Интервал между препятствиями в миллисекундах
      callback: this.addObstacle,
      callbackScope: this,
      loop: true
    });

    // Обработка столкновений игрока с препятствиями
    this.physics.add.overlap(this.player, this.obstacles, this.handleCollision, undefined, this.player);
    this.disablePhysics();
  }

  update() {
    if (this.gameStore.isPaused || !this.gameStore.gameInitStarted) return;

    this.background?.update();
    this.player?.update();

    this.obstacles?.getChildren().forEach((obstacle: Phaser.GameObjects.GameObject) => {
      (obstacle as Obstacle).update();
    });
    console.log(this.obstacles?.getChildren().length)
  }

  public disablePhysics() {
    this.player?.disablePhysics();

    this.obstacles?.getChildren().forEach((obstacle: Phaser.GameObjects.GameObject) => {
      (obstacle as Obstacle).disablePhysics();
    });
  }

  public enablePhysics() {
    this.player?.enablePhysics();
    this.obstacles?.getChildren().forEach((obstacle: Phaser.GameObjects.GameObject) => {
      (obstacle as Obstacle).enablePhysics();
    });
  }

  addObstacle() {
    if (this.gameStore.isPaused || !this.gameStore.gameInitStarted) return;

    const gap = 150; // Размер зазора между верхней и нижней трубой
    const x = this.scale.width;
    const y = Phaser.Math.Between(50, this.scale.height - 50 - gap);

    const obstacle = new Obstacle(this, x, y, gap);
    this.obstacles?.add(obstacle);
  }

  handleCollision() {
    // Обработка столкновения игрока с препятствием
    this.scene.restart();
  }
}

export default Gameplay;