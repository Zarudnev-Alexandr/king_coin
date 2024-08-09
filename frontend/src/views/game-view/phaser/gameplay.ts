import BackgroundSprite from "@/views/game-view/phaser/entities/background-sprite.ts";
import BackgroundTile from "@/views/game-view/phaser/entities/background-sprite.ts";
import PlayerImage from "@/assets/img/game/player.png"
import Player from "@/views/game-view/phaser/entities/player.ts";
import TopPipeImage from "@/assets/img/game/top-pipe.png"
import BottomPipeImage from "@/assets/img/game/bottom-pipe.png"
import CoinRewardImage from "@/assets/img/game/coin.png"
import MysteryBoxImage from "@/assets/img/game/mystery-box.png"
import Background1 from "@/assets/img/game/background1.png"
import Background2 from "@/assets/img/game/background2.png"
import MonkeyMaket from "@/assets/img/game/monkey-maket.png";
import TouchImg from "@/assets/img/game/touch.png";
import Obstacle from "@/views/game-view/phaser/entities/obstacle.ts";
import {useGameStore} from "@/shared/pinia/game-store.ts";
import ObstacleManager from "@/views/game-view/phaser/entities/obstacle-manager.ts";
import CoinReward from "@/views/game-view/phaser/entities/coin-reward.ts";
import MysteryBox from "@/views/game-view/phaser/entities/mystery-box.ts";
import {MysteryBoxType} from "@/shared/api/types/enums.ts";

class Gameplay extends Phaser.Scene {
  private player?: Player;
  private gameStore = useGameStore();
  private obstacleManager: ObstacleManager | null = null;
  private timeoutIds: number[] = [];
  static instance: Gameplay | null = null;
  private backgroundManager: BackgroundTile | null = null;
  private maketMonkey: Phaser.GameObjects.Sprite | null = null;
  private touchSprite: Phaser.GameObjects.Sprite | null = null;

  constructor() {
    super('Gameplay');
    Gameplay.instance = this;
  }

  preload() {
    this.load.image('player', PlayerImage);
    this.load.image('topPipe', TopPipeImage);
    this.load.image('bottomPipe', BottomPipeImage);
    this.load.image('coin', CoinRewardImage);
    this.load.image('mystery-box', MysteryBoxImage);
    this.load.image('background1', Background1);
    this.load.image('background2', Background2);
    this.load.image('monkey-maket', MonkeyMaket);
    this.load.image('touch', TouchImg);

    this.load.on('complete', () => {
      this.gameStore.setLoading(false);
    });
  }

  create() {
    this.backgroundManager = new BackgroundSprite(this, 'background1', 'background2', 1);
    this.obstacleManager = new ObstacleManager(this);
    this.player = new Player(this, 100, this.scale.height / 2);
    this.maketMonkey = this.add.sprite(200, this.scale.height / 2 - 90, 'monkey-maket').setScale(0.36, 0.36);
    this.touchSprite = this.add.sprite(230, this.scale.height / 2 + 50, 'touch');

    // Обработка столкновений игрока с препятствиями
    this.physics.add.overlap(this.player, this.obstacleManager.obstacles, this.handleCollision, undefined, this);
    this.physics.add.overlap(this.player, this.obstacleManager.rewards, this.handleRewardCollision, undefined, this);
    this.physics.add.overlap(this.player, this.obstacleManager.mysteryBoxes, this.handleMysteryBoxCollision, undefined, this);

    this.disablePhysics();
  }

  update(time: number, delta: number) {
    if (this.gameStore.isPaused || !this.gameStore.gameInitStarted) return;

    this.backgroundManager?.update();
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
    this.clearAllTimeouts();
  }

  public enablePhysics() {
    this.player?.enablePhysics();
    this.obstacleManager?.setVelocityX(-120);
  }

  handleCollision() {
    if (this.gameStore.currentActiveModal !== 'game-over') {
      this.gameStore.audioManager.playGameOverMusic();
      this.gameStore.vibrationService.heavy();
    }
    this.gameStore.setPause(true);
    this.gameStore.setCurrentActiveModal('game-over');
    this.clearAllTimeouts();
    this.gameStore.setMysteryBox(null);
  }

  public setSpeed(velocity: number) {
    this.obstacleManager?.setVelocityX(velocity);
  }

  handleRewardCollision(_: (Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Tilemaps.Tile),
                        object2: (Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Tilemaps.Tile)) {
    if (object2 instanceof CoinReward) {
      this.gameStore.audioManager.playCoinMusic();
      this.gameStore.vibrationService.medium();
      object2.destroy();
      this.gameStore.setScore(this.gameStore.score + object2.reward);
    }
  }

  handleMysteryBoxCollision(_: (Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Tilemaps.Tile),
                            object2: (Phaser.Types.Physics.Arcade.GameObjectWithBody | Phaser.Tilemaps.Tile)) {
    if (object2 instanceof MysteryBox) {
      object2.destroy();
      this.gameStore.audioManager.playHitBoxSound();
      this.gameStore.vibrationService.medium();
      this.gameStore.setMysteryBox(object2.type);

      if (object2.type === MysteryBoxType['100COIN']) {
        this.gameStore.setScore(this.gameStore.score + 100);

        const timeoutId = window.setTimeout(() => {
          this.gameStore.setMysteryBox(null);
        }, 2000);

        this.addTimeout(timeoutId);

        return;
      } else if (object2.type === MysteryBoxType['SPEED_X2.5']) {
        Gameplay.instance?.setSpeed(-300);

        const timeoutId = window.setTimeout(() => {
          if (!this.gameStore.isPaused) Gameplay.instance?.setSpeed(-120);
          this.gameStore.setMysteryBox(null);
        }, 5000);

        this.addTimeout(timeoutId);

        return;
      }

      const timeoutId = window.setTimeout(() => {
        this.gameStore.setMysteryBox(null);
      }, 5000);

      this.addTimeout(timeoutId);
    }
  }

  private addTimeout(timeoutId: number) {
    this.timeoutIds.push(timeoutId);
  }

  public clearAllTimeouts() {
    this.timeoutIds.forEach(clearTimeout);
    this.timeoutIds = [];
  }

  public removePresentationSprites() {
    if (this.maketMonkey && this.touchSprite) {
      this.maketMonkey.destroy();
      this.touchSprite.destroy();
      this.maketMonkey = null;
      this.touchSprite = null;
    }
  }
}

export default Gameplay;