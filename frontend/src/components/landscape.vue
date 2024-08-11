<script setup lang="ts">

</script>

<template>
  <div class="landscape-wrap">
    <img src="@/assets/svg/landscape.svg" alt="">
    <span class="sf-pro-font">Поверните телефон, чтобы продолжить</span>
  </div>
</template>

<style scoped>
.landscape-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 55;
  background-color: rgba(57, 34, 0, 1);
  gap: 10px;

  img {
    width: 74px;
  }

  span {
    width: 160px;
    font-size: 14px;
    font-weight: 700;
    line-height: 20.27px;
    text-align: center;
    color: white;
  }
}
</style>