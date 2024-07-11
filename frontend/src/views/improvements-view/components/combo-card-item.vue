<script setup lang="ts">
import AppIconWithShadow from "@/components/AppIconWithShadow.vue";

interface Props {
  title: string
}

const props: Props = defineProps<Props>()
</script>

<template>
  <div class="combo-item-wrapper">
    <div class="combo-item">
      <div class="combo-item-content">
        <AppIconWithShadow style="gap: 5px;">
          <img src="@/assets/img/bad-coin-icon.png" alt="BadCoin" style="width: 35px; height: 35px;">
        </AppIconWithShadow>
        <span class="sf-pro-font">
          {{ props.title }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.combo-item-wrapper {
  flex: 1;
  background-color: rgba(57, 34, 0, 1);
  border-radius: 10px;
  padding: 4px;

  .combo-item {
    border: 1px solid rgba(131, 101, 51, 1);
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;

    .combo-item-content {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 10px;
      padding: 8px;

      img {
        width: 40px;
        height: 40px;
      }

      span {
        font-size: 8px;
        font-weight: 400;
        line-height: 9.55px;
        text-align: center;
        color: white;
      }
    }
  }
}
</style>