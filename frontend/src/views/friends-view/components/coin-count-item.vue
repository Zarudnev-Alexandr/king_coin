<script setup lang="ts">
import {formatNumber, formatNumberWithSpaces} from "@/helpers/formats.ts";

interface Props {
  count: number;
  formatNumber?: string;
}

const props: Props = defineProps<Props>();

const getNumber = () => {
  if (props.formatNumber === 'withSpace') {
    return formatNumberWithSpaces(props.count)
  }

  return formatNumber(props.count)
}
</script>

<template>
  <div class="coin-count-wrap">
    <img src="@/assets/svg/coin.svg" alt="">
    <span class="sf-pro-font">+ {{ getNumber() }}</span>
  </div>
</template>

<style scoped>
.coin-count-wrap {
  display: flex;
  gap: 5px;

  img {
    width: 14px;
    height: 14px;
  }

  span {
    font-size: 12px;
    font-weight: 600;
    line-height: 14.32px;
    text-align: right;
    color: white;
  }
}
</style>