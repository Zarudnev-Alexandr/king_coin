<script setup lang="ts">

</script>

<template>
  <div class="game-loader-wrapper">
    <div class="game-loader-content">
      <h2>Взлетаем!</h2>

      <div class="loading-indicator">
        <h3 class="sf-pro-font loading-text">Загрузка</h3>

        <div class="game-loader-content-indicator-group">
          <span class="game-loader-content-indicator-item"></span>
          <span class="game-loader-content-indicator-item"></span>
          <span class="game-loader-content-indicator-item"></span>
          <span class="game-loader-content-indicator-item"></span>
          <span class="game-loader-content-indicator-item"></span>
          <span class="game-loader-content-indicator-item"></span>
          <span class="game-loader-content-indicator-item"></span>
        </div>
      </div>
    </div>

    <img src="@/assets/img/game/loading-bg-player.png" alt="">
  </div>
</template>

<style scoped>
.game-loader-wrapper {
  display: flex;
  justify-content: end;
  position: absolute;
  z-index: 15;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/img/game/loading-bg.jpg');
  background-repeat: no-repeat;
  background-size: cover; /* Изображение масштабируется, чтобы полностью покрыть контейнер */
  background-position: center; /* Изображение центрируется */

  img {
    position: absolute;
    z-index: 15;
    bottom: 35px;
    left: 0;
    width: 100%;
  }

  h2 {
    font-family: 'SuperSquadRus', sans-serif;
    font-size: 30px;
    font-weight: 400;
    line-height: 46.32px;
    text-align: center;
    color: white;
    text-shadow: -3px 3px 0 rgba(57, 34, 0, 1),
    3px 3px 0 rgba(57, 34, 0, 1),
    3px -3px 0 rgba(57, 34, 0, 1),
    -3px -3px 0 rgba(57, 34, 0, 1);
  }

  .game-loader-content {
    display: flex;
    justify-content: space-around;
    flex-direction: column;
    align-items: center;
    z-index: 16;
    position: absolute;
    width: 100%;
    height: 100%;

    .loading-indicator {
      display: flex;
      flex-direction: column;

      .loading-text {
        font-size: 28px;
        font-weight: 700;
        line-height: 40.54px;
        text-align: center;
        color: white;
        margin: 10px 0;
      }


      .game-loader-content-indicator-group {
        display: flex;
        justify-content: center;
        gap: 8px;

        .game-loader-content-indicator-item {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background-color: white;
          animation: loader 1.4s infinite;
        }

        .game-loader-content-indicator-item:nth-child(1) {
          animation-delay: 0s;
        }

        .game-loader-content-indicator-item:nth-child(2) {
          animation-delay: 0.2s;
        }

        .game-loader-content-indicator-item:nth-child(3) {
          animation-delay: 0.4s;
        }

        .game-loader-content-indicator-item:nth-child(4) {
          animation-delay: 0.6s;
        }

        .game-loader-content-indicator-item:nth-child(5) {
          animation-delay: 0.8s;
        }

        .game-loader-content-indicator-item:nth-child(6) {
          animation-delay: 1s;
        }

        .game-loader-content-indicator-item:nth-child(7) {
          animation-delay: 1.2s;
        }
      }
    }
  }
}

@keyframes loader {
  0%, 20%, 100% {
    background-color: white;
  }
  10% {
    background-color: orange;
  }
}
</style>
