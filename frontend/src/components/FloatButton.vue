<script setup lang="ts">

</script>

<template>
  <div class="float-button-wrap">
    <svg
        width="46"
        height="46"
        viewBox="0 0 46 46"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style="position: absolute; bottom: 0; right: 0"
    >
      <path fill-rule="evenodd" clip-rule="evenodd"
            d="M45.6896 1.39934C45.6896 0.188066 43.3553 -0.118685 42.9489 1.02236C35.9481 20.6762 20.3659 36.2584 0.712056 43.2592C-0.428989 43.6656 -0.122234 45.9999 1.08904 45.9999H35.6896C41.2124 45.9999 45.6896 41.5227 45.6896 35.9999V1.39934Z"
            fill="#703500" fill-opacity="0.2"/>
    </svg>

    <svg
        width="17"
        height="13"
        viewBox="0 0 17 13"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style="position: absolute; top: 5px; left: 5px;"
    >
      <path
          d="M15.2661 1.63794C16.4021 1.41585 16.6071 -0.0015942 15.4495 1.34597e-06C10.7303 0.00650752 6.05569 2.07262 2.87218 6.03983C1.57354 7.65816 0.637487 9.45019 0.0532487 11.3178C-0.294485 12.4293 1.15384 12.6402 1.70541 11.6144C2.26422 10.5752 2.92494 9.57273 3.68913 8.6204C6.70832 4.85797 10.8409 2.50309 15.2661 1.63794Z"
          fill="white"/>
    </svg>

    <slot></slot>
  </div>
</template>

<style scoped>
.float-button-wrap {
  background: radial-gradient(120.14% 120.14% at 50% -11.81%, #FFFFFF 0%, #FFE531 20%, #FFA531 74.03%, #FF8200 100%);
  border-radius: 10px;
  border: 2px solid white;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
</style>