<script setup lang="ts">
import {onMounted, onUnmounted, ref} from 'vue';
import Phaser from 'phaser';
import Gameplay from '@/views/game-view/phaser/gameplay';
import {useGameStore} from "@/shared/pinia/game-store.ts";
import ActionModal from "@/components/ActionModal.vue";
import {formatNumberWithSpaces} from "@/helpers/formats.ts";
import ModalActionButton from "@/components/ModalActionButton.vue";
import {useRouter} from "vue-router";

const phaserRef = ref<HTMLDivElement | null>(null);
let game: Phaser.Game | null = null;
const gameStore = useGameStore();
const router = useRouter();

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: window.innerWidth,
  height: window.innerHeight,
  scene: Gameplay,
  physics: {
    default: 'arcade',
    arcade: {
      debug: false,
    },
  },
};

const handleResumeGame = () => {
  gameStore.setPause(false);
  gameStore.setCurrentActiveModal('');
}

const handleExitGame = () => {
  Gameplay.instance?.scene.remove();
  Gameplay.instance = null;
  if (gameStore.transitionView === '') {
    router.push({name: 'Main'})
  } else {
    router.push({name: gameStore.transitionView})
  }
}

const handleRestart = () => {
  gameStore.initGameState();
  Gameplay.instance?.scene.restart();
}

onMounted(() => {
  if (phaserRef.value) {
    config.parent = phaserRef.value;
    game = new Phaser.Game(config);
    gameStore.initGameState();
  }
});

onUnmounted(() => {
  game?.destroy(true);
});

</script>

<template>
  <div class="game-container-wrapper">
    <div class="game-container-header">
      <span class="game-container-header-text" v-if="!gameStore.gameInitStarted">READY?</span>
      <div class="game-container-header-coin" v-else>
        <img src="@/assets/svg/coin.svg" alt="">
        <span class="game-container-header-text">{{ gameStore.score }}</span>
      </div>
    </div>
    <div ref="phaserRef" id="game-container"/>

    <ActionModal v-if="gameStore.currentActiveModal !== ''">
      <div class="game-modal-content-wrapper">
        <div class="content-header">
          <span v-if="gameStore.currentActiveModal === 'game-over'" class="header-text">Game over</span>
          <span v-if="gameStore.currentActiveModal === 'exit'" class="header-text">Вы уходите?</span>
          <div v-if="gameStore.currentActiveModal === 'pause'" class="pause-header">
            <img src="@/assets/img/game/modal-pause-icon.svg" alt="">
            <span class="header-text">Пауза</span>
          </div>
        </div>
        <div class="content-medium">
          <span class="sf-pro-font">Вы заработали</span>
          <div class="content-reward">
            <img src="@/assets/svg/coin.svg" alt="">
            <span class="sf-pro-font">{{ formatNumberWithSpaces(gameStore.score) }}</span>
          </div>
        </div>
      </div>
      <template #actions>
        <div class="modal-actions-wrapper" v-if="gameStore.currentActiveModal === 'pause' || gameStore.currentActiveModal === 'exit'">
          <ModalActionButton style="width: 133px; height: 67px" @click="handleResumeGame">
            <span class="action-button-title">Продолжить</span>
          </ModalActionButton>
          <ModalActionButton style="width: 133px; height: 67px" @click="handleExitGame">
            <span class="action-button-title">Выйти</span>
          </ModalActionButton>
        </div>
        <div class="modal-actions-wrapper" v-if="gameStore.currentActiveModal === 'game-over'">
          <ModalActionButton style="width: 133px; height: 67px" @click="handleRestart">
            <span class="action-button-title" @click="handleRestart">Сыграть еще</span>
          </ModalActionButton>
        </div>
      </template>
    </ActionModal>
  </div>
</template>

<style scoped>
.game-container-wrapper {
  width: 100%;
  height: 100%;

  #game-container {
    width: 100%;
    height: 100%;
  }

  .modal-actions-wrapper {
    display: flex;
    justify-content: center;
    gap: 15px;

    .action-button-title {
      font-family: 'SuperSquadRus', sans-serif;
      font-size: 14px;
      font-weight: 400;
      line-height: 21.62px;
      text-align: center;
      color: rgba(93, 56, 0, 1);
    }
  }

  .game-container-header {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 20px 0;
  }

  .game-container-header-coin {
    display: flex;
    justify-content: center;
    width: 100%;
    gap: 10px;

    img {
      width: 46px;
      height: 48px;
    }
  }

  .game-container-header-text {
    font-family: 'SuperSquadRus', sans-serif;
    font-size: 30px;
    font-weight: 400;
    line-height: 46.32px;
    text-align: left;
    color: white;
    display: flex;
    text-shadow: -3px 3px 0 rgba(57, 34, 0, 1),
    3px 3px 0 rgba(57, 34, 0, 1),
    3px -3px 0 rgba(57, 34, 0, 1),
    -3px -3px 0 rgba(57, 34, 0, 1);
  }

  .game-modal-content-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 40px;
    gap: 30px;


    .content-medium {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 5px;

      span {
        font-size: 12px;
        font-weight: 600;
        color: white;
      }

      .content-reward {
        display: flex;
        gap: 5px;
        justify-content: center;
        align-items: center;

        img {
          width: 25px;
          height: 25px;
        }

        span {
          font-size: 25px;
          font-weight: 700;
          color: white;
        }
      }
    }

    .pause-header {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    .header-text {
      font-family: 'SuperSquadRus', sans-serif;
      font-size: 34px;
      font-weight: 400;
      line-height: 52px;
      color: white;
    }
  }
}
</style>
