import Phaser from "phaser";
import {useGameStore} from "@/shared/pinia/game-store.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import {MysteryBoxType} from "@/shared/api/types/enums.ts";
import Gameplay from "@/views/game-view/phaser/gameplay.ts";

export default class Player extends Phaser.GameObjects.Sprite {
  gameStore = useGameStore();
  userStore = useUserStore();
  private blinkTimer?: Phaser.Time.TimerEvent;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'player');

    scene.add.existing(this);
    scene.physics.world.enable(this);

    this.setDisplaySize(106, 85);
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.body.setGravityY(500);
      this.body.setCollideWorldBounds(true);

      const radius = 350;
      this.body.setCircle(radius, 200, 120);

      this.body.debugBodyColor = 0xff0000;

      this.body.onWorldBounds = true;
      scene.physics.world.on('worldbounds', this.handleWorldBoundsCollision, this);
    }

    scene.input.on('pointerdown', this.handleJump, this);

    // Начинаем моргание, если персонаж неуязвим
    this.scene.events.on('update', this.update, this);
  }

  private handleJump() {
    if (this.userStore.user) {
      this.gameStore.audioManager.playTapSound();
      let one_tap = (this.userStore.user.boost.one_tap + this.userStore.user.taps_for_level);
      if (this.gameStore.mysteryBox === MysteryBoxType['10X']) {
        one_tap *= 10;
      } else if (this.gameStore.mysteryBox === MysteryBoxType['5X']) {
        one_tap *= 5;
      }

      this.gameStore.setScore(this.gameStore.score + one_tap);
    }

    if (this.gameStore.gameInitStarted === false) {
      this.gameStore.setGameInitStarted();
      this.gameStore.setPause(false);
      Gameplay.instance?.removePresentationSprites();
    }

    if (this.gameStore.isPaused) return;
    (this.body as Phaser.Physics.Arcade.Body).setVelocityY(-300);
  }

  private handleWorldBoundsCollision() {
    if (this.gameStore.isInvulnerable) return;

    if (this.gameStore.currentActiveModal !== 'game-over') {
      this.gameStore.audioManager.playGameOverMusic();
      this.gameStore.vibrationService.heavy();
    }

    this.gameStore.setPause(true);
    this.gameStore.setCurrentActiveModal('game-over');
    this.gameStore.setMysteryBox(null);
    Gameplay.instance?.clearAllTimeouts();
  }

  private startBlinking() {
    if (this.blinkTimer) return;

    this.blinkTimer = this.scene.time.addEvent({
      delay: 100, // Задержка между переключениями видимости
      callback: () => {
        this.visible = !this.visible;
      },
      loop: true,
    });
  }

  private stopBlinking() {
    if (this.blinkTimer) {
      this.blinkTimer.remove();
      this.blinkTimer = undefined;
      this.visible = true; // Убедитесь, что спрайт видим после остановки моргания
    }
  }

  update() {
    if (this.gameStore.isInvulnerable) {
      this.startBlinking();
    } else {
      this.stopBlinking();
    }
  }

  public stopMovement() {
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.body.setVelocity(0, 0);
      this.body.setAcceleration(0, 0);
      this.body.setGravityY(0);
    }
  }

  public disablePhysics() {
    this.stopMovement();
  }

  public enablePhysics() {
    if (this.body && this.body instanceof Phaser.Physics.Arcade.Body) {
      this.body.setGravityY(600);
    }
  }
}
