<script setup lang="ts">

</script>

<template>
  <div class="rating-header">
    <img src="@/assets/img/rating/left-bottom-coin.png" class="left-bottom-coin" alt="">
    <img src="@/assets/img/rating/left-top-coin.png" class="left-top-coin" alt="">
    <img src="@/assets/img/rating/right-top-coin.png" class="right-top-coin" alt="">
    <div class="rating-count-wrapper">
      <img src="@/assets/svg/friends/crown-icon.svg" alt="t">
      <span>Рейтинг</span>
    </div>
    <span class="friends-header-text-2 sf-pro-font">Лучшие из лучших обезьян</span>
  </div>
</template>

<style scoped>
.rating-header {
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

  .friends-header-text-2 {
    font-size: 12px;
    font-weight: 600;
    line-height: 14.32px;
    text-align: center;
    color: rgba(93, 56, 0, 1);
  }

  .rating-count-wrapper {
    display: flex;
    gap: 10px;
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

  .left-bottom-coin {
    position: absolute;
    bottom: -10px;
    left: 20px;
    width: 52px;
    height: 49px;
  }

  .left-top-coin {
    position: absolute;
    top: 30px;
    left: 0;
    width: 37px;
    height: 40px;
  }

  .right-top-coin {
    position: absolute;
    top: 10px;
    right: -10px;
    width: 41px;
    height: 43px;
  }

}

@keyframes slideIn {
  to {
    opacity: 1; /* Конечная прозрачность */
    transform: translateY(0); /* Конечное смещение */
  }
}
</style>