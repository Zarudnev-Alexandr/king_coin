<script setup lang="ts">

</script>

<template>
  <div class="levels-header-wrapper">
    <div class="levels-header-text-wrapper">
      <img src="@/assets/svg/friends/crown-icon.svg" alt="t">
      <span>{{ $t('levels') }}</span>
    </div>
  </div>
</template>

<style scoped>
.levels-header-wrapper {
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

  .levels-header-text-wrapper {
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
}

@keyframes slideIn {
  to {
    opacity: 1; /* Конечная прозрачность */
    transform: translateY(0); /* Конечное смещение */
  }
}
</style>