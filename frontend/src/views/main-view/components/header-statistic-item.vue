<script setup lang="ts">
interface Props {
  title: string;
  value: string | number;
}

const props: Props = defineProps<Props>();
</script>

<template>
  <div class="statistic-item-wrapper">
    <span class="sf-pro-font">{{ props.title }}</span>
    <div class="statistic-item-value">
      <img src="../../../assets/svg/coin.svg" alt="">
      <span class="sf-pro-font">{{ props.value }}</span>
    </div>
  </div>
</template>

<style scoped>
.statistic-item-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 3px;
  padding: 5px 11px 5px 11px;
  border-radius: 10px;
  background-color: rgba(57, 34, 0, 1);
  min-width: 50px;

  span {
    font-size: 10px;
    font-weight: 400;
    line-height: 11.93px;
    text-align: center;
    color: rgba(194, 163, 117, 1);
  }

  .statistic-item-value {
    display: flex;
    justify-content: center;
    gap: 2px;

    img {
      width: 14px;
      height: 14px;
    }

    span {
      font-size: 12px;
      font-weight: 600;
      line-height: 14.32px;
      text-align: center;
      color: white;
    }
  }
}
</style>