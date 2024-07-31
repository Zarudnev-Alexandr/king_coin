import BackgroundImage from "@/assets/img/game/background.png"
import BackgroundSprite from "@/views/game-view/phaser/entities/background-sprite.ts";
import PlayerImage from "@/assets/img/game/player.png"
import Player from "@/views/game-view/phaser/entities/player.ts";
import TopPipeImage from "@/assets/img/game/top-pipe.png"
import BottomPipeImage from "@/assets/img/game/bottom-pipe.png"
import CoinRewardImage from "@/assets/img/game/coin.png"
import MysteryBoxImage from "@/assets/img/game/mystery-box.png"
import Obstacle from "@/views/game-view/phaser/entities/obstacle.ts";
import {useGameStore} from "@/shared/pinia/game-store.ts";
import ObstacleManager from "@/views/game-view/phaser/entities/obstacle-manager.ts";
import CoinReward from "@/views/game-view/phaser/entities/coin-reward.ts";
import MysteryBox from "@/views/game-view/phaser/entities/mystery-box.ts";
import {MysteryBoxType} from "@/shared/api/types/enums.ts";

class Gameplay extends Phaser.Scene {
  private background?: BackgroundSprite;
  private player?: Player;
  private gameStore = useGameStore();
  private obstacleManager: ObstacleManager | null = null;
  static instance: Gameplay | null = null;

  constructor() {
    super('Gameplay');
    Gameplay.instance = this;
  }

  preload() {
    this.load.image('background', BackgroundImage);
    this.load.image('player', PlayerImage);
    this.load.image('topPipe', TopPipeImage);
    this.load.image('bottomPipe', BottomPipeImage);
    this.load.image('coin', CoinRewardImage);
    this.load.image('mystery-box', MysteryBoxImage);
  }

  create() {
    this.background = new BackgroundSprite(this, 0, 0, this.scale.height);
    this.obstacleManager = new ObstacleManager(this);
    this.background.setOrigin(0, 0);
    this.player = new Player(this, 100, this.scale.height / 2);

    // Обработка столкновений игрока с препятствиями
    this.physics.add.overlap(this.player, this.obstacleManager.obstacles, this.handleCollision, undefined, this.player);
    this.physics.add.overlap(this.player, this.obstacleManager.rewards, this.handleRewardCollision, undefined, this.player);
    this.physics.add.overlap(this.player, this.obstacleManager.mysteryBoxes, this.handleMysteryBoxCollision, undefined, this.player);

    this.disablePhysics();
  }

  update(time: number, delta: number) {
    if (this.gameStore.isPaused || !this.gameStore.gameInitStarted) return;

    this.background?.update();
    this.player?.update();

    this.obstacleManager?.obstacles?.getChildren().forEach((obstacle: Phaser.GameObjects.GameObject) => {
      (obstacle as Obstacle).update();
    });
    this.obstacleManager?.update(time, delta);
    console.log(this.obstacleManager?.obstacles?.getChildren().length)
  }

  public disablePhysics() {
    this.player?.disablePhysics();
    this.obstacleManager?.setVelocityX(0);
  }

  public enablePhysics() {
    this.player?.enablePhysics();
    this.obstacleManager?.setVelocityX(-120);
  }

  handleCollision() {
    this.gameStore.setPause(true);
    this.gameStore.setCurrentActiveModal('game-over');
  }

  public setSpeed(velocity: number) {
    this.obstacleManager?.setVelocityX(velocity);
  }

  handleRewardCollision(_: (Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Tilemaps.Tile),
                        object2: (Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Tilemaps.Tile)) {
    if (object2 instanceof CoinReward) {
      object2.destroy();
      this.gameStore.setScore(this.gameStore.score + object2.reward);
    }
  }

  handleMysteryBoxCollision(_: (Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Tilemaps.Tile),
                            object2: (Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Tilemaps.Tile)) {
    if (object2 instanceof MysteryBox) {
      object2.destroy();
      this.gameStore.setMysteryBox(object2.type);

      if (object2.type === MysteryBoxType['100COIN']) {
        this.gameStore.setScore(this.gameStore.score + 100);

        setTimeout(() => {
          this.gameStore.setMysteryBox(null);
        }, 2000);

        return;
      } else if (object2.type === MysteryBoxType['SPEED_X2.5']) {

        Gameplay.instance?.setSpeed(-300);

        setTimeout(() => {
          if (!this.gameStore.isPaused) Gameplay.instance?.setSpeed(-120);
          this.gameStore.setMysteryBox(null);
        }, 5000);

        return;
      }

      setTimeout(() => {
        this.gameStore.setMysteryBox(null);
      }, 5000);
    }
  }
}

export default Gameplay;