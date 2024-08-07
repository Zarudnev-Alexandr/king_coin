import BackgroundMusic from "@/assets/songs/bg-song.mp3"
import HitBoxSound from "@/assets/songs/box-hit.mp3"
import HitObstacle from "@/assets/songs/obstacle-hit.mp3"
import CoinSound from "@/assets/songs/coin-hit.mp3"
import TapSound from "@/assets/songs/tap-song.mp3"
import {useSettingsStore} from "@/shared/pinia/settings-store.ts";

class AudioManager {
  context: AudioContext;
  backgroundMusicBuffer: AudioBuffer | null;
  backgroundMusicSource: AudioBufferSourceNode | null;
  hitObstacleBuffer: AudioBuffer | null;
  hitObstacleMusicSource: AudioBufferSourceNode | null;
  coinMusicBuffer: AudioBuffer | null;
  coinMusicSource: AudioBufferSourceNode | null;
  tapSoundBuffer: AudioBuffer | null;
  tapSoundSource: AudioBufferSourceNode | null;
  hitBoxSoundBuffer: AudioBuffer | null;
  hitBoxSoundSource: AudioBufferSourceNode | null;
  settingStore = useSettingsStore();


  constructor() {
    this.context = new AudioContext();
    this.backgroundMusicBuffer = null;
    this.backgroundMusicSource = null;
    this.hitObstacleBuffer = null;
    this.hitObstacleMusicSource = null;
    this.coinMusicBuffer = null;
    this.coinMusicSource = null;
    this.tapSoundBuffer = null;
    this.tapSoundSource = null;
    this.hitBoxSoundBuffer = null;
    this.hitBoxSoundSource = null;

    this.loadBackgroundMusic(BackgroundMusic).catch(e => console.error(e));
    this.loadHitObstacleMusic(HitObstacle).catch(e => console.error(e));
    this.loadCoinMusic(CoinSound).catch(e => console.error(e));
    this.loadTapSound(TapSound).catch(e => console.error(e));
    this.loadHitBoxSound(HitBoxSound).catch(e => console.error(e));
  }

  async loadAudio(url: string) {
    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    return this.context.decodeAudioData(arrayBuffer);
  }

  async loadBackgroundMusic(url: string) {
    this.backgroundMusicBuffer = await this.loadAudio(url);
  }

  async loadHitObstacleMusic(url: string) {
    this.hitObstacleBuffer = await this.loadAudio(url);
  }

  async loadCoinMusic(url: string) {
    this.coinMusicBuffer = await this.loadAudio(url);
  }

  async loadTapSound(url: string) {
    this.tapSoundBuffer = await this.loadAudio(url);
  }

  async loadHitBoxSound(url: string) {
    this.hitBoxSoundBuffer = await this.loadAudio(url);
  }

  playBackgroundMusic() {
    if (!this.settingStore.soundOn) return;

    if (this.backgroundMusicBuffer) {
      this.backgroundMusicSource = this.context.createBufferSource();
      this.backgroundMusicSource.buffer = this.backgroundMusicBuffer;
      this.backgroundMusicSource.loop = true;
      this.backgroundMusicSource.connect(this.context.destination);
      this.backgroundMusicSource.start(0);
    }
  }

  stopBackgroundMusic() {
    if (this.backgroundMusicSource) {
      this.backgroundMusicSource.stop();
      this.backgroundMusicSource.disconnect();
      this.backgroundMusicSource = null;
    }
  }

  playGameOverMusic() {
    if (!this.settingStore.soundOn) return;

    if (this.hitObstacleBuffer) {
      this.hitObstacleMusicSource = this.context.createBufferSource();
      this.hitObstacleMusicSource.buffer = this.hitObstacleBuffer;
      this.hitObstacleMusicSource.connect(this.context.destination);
      this.hitObstacleMusicSource.start(0);
    }
  }

  playCoinMusic() {
    if (!this.settingStore.soundOn) return;

    if (this.coinMusicBuffer) {
      this.coinMusicSource = this.context.createBufferSource();
      this.coinMusicSource.buffer = this.coinMusicBuffer;
      this.coinMusicSource.connect(this.context.destination);
      this.coinMusicSource.start(0);
    }
  }

  playTapSound() {
    if (!this.settingStore.soundOn) return;

    if (this.tapSoundBuffer) {
      this.tapSoundSource = this.context.createBufferSource();
      this.tapSoundSource.buffer = this.tapSoundBuffer;
      this.tapSoundSource.connect(this.context.destination);
      this.tapSoundSource.start(0);
    }
  }

  playHitBoxSound() {
    if (!this.settingStore.soundOn) return;

    if (this.hitBoxSoundBuffer) {
      this.hitBoxSoundSource = this.context.createBufferSource();
      this.hitBoxSoundSource.buffer = this.hitBoxSoundBuffer;
      this.hitBoxSoundSource.connect(this.context.destination);
      this.hitBoxSoundSource.start(0);
    }
  }
}

export default AudioManager;