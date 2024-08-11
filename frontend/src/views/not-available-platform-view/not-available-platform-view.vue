<script setup lang="ts">
import DesktopBg from "@/assets/img/not-available-platform/bg.png";
import MobileBg from "@/assets/img/main-view-bg.webp";

const backgroundImage = window.innerHeight > window.innerWidth ? MobileBg : DesktopBg;
</script>

<template>
  <div class="not-available-platform-wrap" :style="{ backgroundImage: `url(${backgroundImage})` }">
    <div class="top-gradient" />
    <div class="bottom-gradient" />
    <div class="platform-content">
      <img class="logo" src="@/assets/img/not-available-platform/logo.png" alt="">
      <img class="qr" src="@/assets/img/not-available-platform/qr.png" alt="">
      <span>Play on your phone</span>
    </div>
  </div>
</template>

<style scoped>
.not-available-platform-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  margin: 0 auto;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  position: relative;

  .bottom-gradient {
    background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, #000000 58.43%);
    position: absolute;
    bottom: 0;
    left: 0;
    height: 30vh;
    width: 100%;
    z-index: 1;
  }

  .top-gradient {
    background: linear-gradient(0deg, rgba(0, 0, 0, 0) 0%, #000000 58.43%);
    position: absolute;
    top: 0;
    left: 0;
    height: 30vh;
    width: 100%;
    z-index: 1;
  }

  .platform-content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    position: relative;
    z-index: 5;

    span {
      font-size: 24px;
      font-weight: 700;
      line-height: 34.75px;
      text-align: center;
      color: white;
    }

    .qr {
      width: 280px;
    }

    .logo {
      width: 157px;
    }
  }
}
</style>
