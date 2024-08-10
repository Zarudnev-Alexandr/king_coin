<script setup lang="ts">
import {useFriendsStore} from "@/shared/pinia/friends-store.ts";
import {formatNumberWithSpaces} from "@/helpers/formats.ts";
import {ref, watch} from "vue";

const friendsStore = useFriendsStore();
const isAnimating = ref(false);
const displayedFriendsCount = ref(friendsStore.friendsList?.length ?? 0);

function startAnimation() {
  isAnimating.value = true;
  setTimeout(() => {
    isAnimating.value = false;
  }, 500);
}

const animationPlusCount = (val: number) => {
  startAnimation();
  const startTime = performance.now();
  const duration = 500;
  const startVal = 0
  const updateInterval = 50;

  function updateValue() {
    const currentTime = performance.now();
    const elapsedTime = currentTime - startTime;
    const progress = Math.min(elapsedTime / duration, 1);
    displayedFriendsCount.value = startVal + (val * progress);

    if (progress < 1) {
      setTimeout(updateValue, updateInterval);
    }
  }

  updateValue();
};

watch(() => friendsStore.friendsList, () => {
  if (friendsStore.friendsList && friendsStore.friendsList?.length !== 0)
    animationPlusCount(friendsStore.friendsList?.length);
});
</script>

<template>
  <div class="friends-header">
    <img src="@/assets/svg/friends/header-rt-top-monkey.png" alt="" class="header-rt-top-img">
    <img src="@/assets/svg/friends/header-top-lf-monkey.png" alt="" class="header-top-lf-img">
    <img src="@/assets/svg/friends/header-rt-monkey.png" alt="" class="header-rt-img">
    <img src="@/assets/svg/friends/header-bottom-rt.png" alt="" class="header-bt-rt-img">
    <div class="friends-count-wrapper" :class="{ 'pulse-animation': isAnimating }">
      <span>{{ formatNumberWithSpaces(displayedFriendsCount) }}</span>
      <img src="@/assets/svg/friends/crown-icon.svg" alt="t">
    </div>
    <span class="sf-pro-font friends-header-text-1">друзей обезьян</span>
    <span class="friends-header-text-2 sf-pro-font">Приглашайте друзей и получайте бонусы</span>
  </div>
</template>

<style scoped>
.friends-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 92%;
  margin: 0 auto;
  padding-top: 40px;
  position: relative;
  opacity: 0;
  transform: translateY(-50px);
  animation: slideIn 0.5s ease-in-out forwards;

  .friends-header-text-1 {
    font-size: 28px;
    font-weight: 800;
    line-height: 33.41px;
    text-align: center;
    color: rgba(93, 56, 0, 1);
  }

  .friends-header-text-2 {
    font-size: 12px;
    font-weight: 600;
    line-height: 14.32px;
    text-align: center;
    color: rgba(93, 56, 0, 1);
  }

  .friends-count-wrapper {
    display: flex;
    gap: 7px;
    align-items: center;
    justify-content: center;
    width: 100%;

    span {
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

    img {
      width: 53px;
      height: 52px;
    }
  }

  .header-rt-top-img {
    position: absolute;
    top: 15px;
    right: 20px;
    width: 55px;
    height: 55px;
  }

  .header-top-lf-img {
    position: absolute;
    top: 10px;
    left: 20%;
    width: 35px;
    height: 35px;
  }

  .header-rt-img {
    position: absolute;
    top: 40%;
    left: 15px;
    width: 35px;
    height: 35px;
  }

  .header-bt-rt-img {
    position: absolute;
    right: 0;
    bottom: 10px;
    width: 35px;
    height: 35px;
  }
}

.pulse-animation {
  animation: pulse 0.3s infinite;
}

@keyframes slideIn {
  to {
    opacity: 1; /* Конечная прозрачность */
    transform: translateY(0); /* Конечное смещение */
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}
</style>