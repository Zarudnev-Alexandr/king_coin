import Gameplay from "@/views/game-view/phaser/gameplay.ts";
import Phaser from "phaser";

class BackgroundSprite extends Phaser.GameObjects.Sprite {
    scene: Gameplay;

    constructor(scene: Phaser.Scene, x: number, y: number, height: number) {
        super(scene, x, y, 'background');
        this.scene = scene as Gameplay;
        scene.add.existing(this);

        this.displayHeight = height;
    }

    update() {
        console.log("update Background")
        super.update();
        this.x -= 1;
    }
}

export default BackgroundSprite;
