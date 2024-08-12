import Gameplay from "../gameplay.ts";
import {useGameStore} from "@/shared/pinia/game-store.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";
import {MysteryBoxType} from "@/shared/api/types/enums.ts";

class ObstacleBottomPipe extends Phaser.Physics.Arcade.Sprite {
  scene: Gameplay
  gameStore = useGameStore();
  rewardIsGiven = false;
  userStore = useUserStore();

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x + 40, y, 'bottomPipe');

    this.setOrigin(0.5, 0);
    this.scene = scene as Gameplay
    scene.add.existing(this);
    scene.physics.add.existing(this);
    this.setDisplaySize(74, 451);
  }

  update() {
    if (this.x < 100 && !this.rewardIsGiven && this.userStore.user) {
      let one_tap = (this.userStore.user.boost.one_tap + this.userStore.user.taps_for_level);
      if (this.gameStore.mysteryBox === MysteryBoxType['10X']) {
        one_tap *= 10;
      } else if (this.gameStore.mysteryBox === MysteryBoxType['5X']) {
        one_tap *= 5;
      }

      this.gameStore.setScore(this.gameStore.score + one_tap);
      this.rewardIsGiven = true;
      this.gameStore.vibrationService.light();
    }

    if (this.x < -this.width) {
      this.destroy();
    }
  }
}

export default ObstacleBottomPipe;