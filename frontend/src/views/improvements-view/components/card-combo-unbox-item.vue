<script setup lang="ts">
</script>

<template>
  <div class="combo-unbox-item-wrapper">
    <div class="combo-unbox-item">
      <svg width="37" height="37"
           viewBox="0 0 37 37"
           fill="none"
           xmlns="http://www.w3.org/2000/svg"
           style="position: absolute; top: 0; left: 0"
      >
        <path fill-rule="evenodd" clip-rule="evenodd"
              d="M-2.45397 35.8312C-2.45397 37.0425 -0.0446968 37.3702 0.383961 36.2373C6.62536 19.7421 19.742 6.62548 36.2371 0.384071C37.37 -0.0445862 37.0424 -2.45381 35.8311 -2.45381H7.54603C2.02318 -2.45381 -2.45397 2.02334 -2.45397 7.54619V35.8312Z"
              fill="#AA5100" fill-opacity="0.2"/>
      </svg>

      <svg
          width="56"
          height="56"
          viewBox="0 0 56 56"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          style="position: absolute; bottom: 0; right: 0"
      >
        <path fill-rule="evenodd" clip-rule="evenodd"
              d="M58.454 1.06841C58.454 -0.142861 56.2287 -0.418675 55.8548 0.733446C47.3957 26.7992 26.7992 47.3957 0.733445 55.8548C-0.418675 56.2287 -0.142867 58.4541 1.06841 58.4541H48.454C53.9769 58.4541 58.454 53.9769 58.454 48.454V1.06841Z"
              fill="#2A1900"/>
      </svg>

      <img src="@/assets/img/specific/combo-unbox-item-rt-bm-coin.png" alt=""
           style="position:absolute; bottom: 10px; left: 7px; width: 28px; height: 26px;"
      >
      <img src="@/assets/img/specific/combo-unbox-item-top-rt-coin.png"
           alt=""
           style="position: absolute; top: 0; right: 0; width: 40px; height: 37px"
      >

      <img src="@/assets/img/specific/combo-unbox-item-bottom-rt-coin.png"
           alt=""
           style="position: absolute; bottom: 0; right: 3px; width: 45px; aspect-ratio: 94/68"
      >

      <img src="@/assets/img/specific/combo-unbox-question.png"
           alt=""
           style="width: 20px; height: 46px; position:absolute; top: 50%; right: 50%; transform: translate(50%, -50%)"
      >
    </div>
  </div>
</template>

<style scoped>
.combo-unbox-item-wrapper {
  flex: 1;
  background-color: rgba(57, 34, 0, 1);
  border-radius: 10px;
  padding: 4px;
  height: 100%;
  box-sizing: border-box;

  .combo-unbox-item {
    border: 1px solid rgba(131, 101, 51, 1);
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    height: 100%;
    position: relative;

  }
}
</style>