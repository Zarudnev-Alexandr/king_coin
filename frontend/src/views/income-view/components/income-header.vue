<script setup lang="ts">

</script>

<template>
  <div class="income-header-wrapper">
    <img src="@/assets/svg/friends/invite-card-up-coin.png" alt="" class="up-left-coin">
    <img src="@/assets/svg/friends/invite-friends-card-down-coin.png" alt="" class="up-right-coin">
    <h2 class="sf-pro-font">Хаслим монеты</h2>
    <span class="sf-pro-font">Выполняйте задания и зарабатывайте монеты</span>
  </div>
</template>

<style scoped>
.income-header-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 30px 0;
  position: relative;
  box-sizing: border-box;
  opacity: 0;
  transform: translateY(-50px);
  animation: slideIn 0.5s ease-in-out forwards;

  .up-left-coin {
    width: 46px;
    height: 48px;
    position: absolute;
    top: 30px;
    left: 0;
  }

  .up-right-coin {
    width: 29px;
    height: 31px;
    position: absolute;
    top: 15px;
    right: 0;
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

  span {
    font-size: 12px;
    font-weight: 600;
    line-height: 14.32px;
    text-align: center;
    color: rgba(93, 56, 0, 1);
  }
}

@keyframes slideIn {
  to {
    opacity: 1; /* Конечная прозрачность */
    transform: translateY(0); /* Конечное смещение */
  }
}
</style>