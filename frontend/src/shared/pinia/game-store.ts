import {defineStore} from "pinia";
import {Ref, ref} from "vue";
import Gameplay from "@/views/game-view/phaser/gameplay.ts";
import {MysteryBoxType} from "@/shared/api/types/enums.ts";
import AudioManager from "@/views/game-view/phaser/audio-manager.ts";
import VibrationService from "@/shared/api/services/vibration-service.ts";


export const useGameStore = defineStore('gameStore', () => {
  const score = ref(0);
  const columnsCount = ref(0);
  const isPaused = ref(false);
  const gameInitStarted = ref(false);
  const currentActiveModal: Ref<'game-over' | 'pause' | 'exit' | ''> = ref('');
  const transitionView = ref('');
  const mysteryBox: Ref<MysteryBoxType | null> = ref(null);
  const isLoading: Ref<boolean> = ref(false);
  const isInvulnerable = ref(false);
  const adIsWatched = ref(false);
  const audioManager = new AudioManager();
  const vibrationService = new VibrationService();

  const setScore = (value: number) => {
    score.value = value;
  };

  const setPause = (value: boolean) => {
    isPaused.value = value;
    currentActiveModal.value = value ? 'pause' : '';
    if (value) {
      audioManager.stopBackgroundMusic();
      Gameplay.instance?.disablePhysics()
    } else {
      audioManager.playBackgroundMusic();
      Gameplay.instance?.enablePhysics();
    }
  };

  const setGameInitStarted = () => {
    gameInitStarted.value = true;
    audioManager.playBackgroundMusic();
  }

  const initGameState = () => {
    score.value = 0;
    columnsCount.value = 0;
    isPaused.value = false;
    gameInitStarted.value = false;
    currentActiveModal.value = '';
    transitionView.value = '';
  }

  const setTransitionView = (value: string) => {
    transitionView.value = value;
  }

  const setCurrentActiveModal = (value: 'game-over' | 'pause' | 'exit' | '') => {
    currentActiveModal.value = value
  }

  const setMysteryBox = (value: MysteryBoxType | null) => {
    mysteryBox.value = value;
  }

  const setLoading = (value: boolean) => {
    isLoading.value = value;
  }

  const setInvulnerable = (value: boolean) => {
    isInvulnerable.value = value;
  }

  const setAdIsWatched = (value: boolean) => {
    adIsWatched.value = value;
  }

  const setColumnsCount = (value: number) => {
    columnsCount.value = value;
  }

  return {
    score,
    setScore,
    isPaused,
    setPause,
    gameInitStarted,
    setGameInitStarted,
    initGameState,
    currentActiveModal,
    setCurrentActiveModal,
    transitionView,
    setTransitionView,
    mysteryBox,
    setMysteryBox,
    isLoading,
    setLoading,
    audioManager,
    vibrationService,
    setInvulnerable,
    isInvulnerable,
    setAdIsWatched,
    adIsWatched,
    setColumnsCount,
    columnsCount,
  };
});