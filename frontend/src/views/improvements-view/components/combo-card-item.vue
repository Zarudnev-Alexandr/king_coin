<script setup lang="ts">

interface Props {
  title: string,
  img_url: string,
  isSpecial: boolean,
}

const props: Props = defineProps<Props>()
</script>

<template>
  <div class="combo-item-wrapper">
    <div class="combo-item" v-if="!props.isSpecial">
      <div class="combo-item-content">
        <img :src="props.img_url" alt="BadCoin" style="width: 35px;">
        <span class="sf-pro-font">
          {{ props.title }}
        </span>
      </div>
    </div>
    <div class="combo-item-special" :style="`background-image: url(${props.img_url})`" v-else>
      <div class="gradient"/>
      <div class="combo-item-content">
        <div style="flex: 1"/>
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
    height: 100%;
    box-sizing: border-box;

    .combo-item-content {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 10px;
      padding: 8px;

      img {
        width: 40px;
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

  .combo-item-special {
    border: 1px solid rgba(131, 101, 51, 1);
    display: flex;
    justify-content: center;
    align-items: flex-end;
    border-radius: 10px;
    height: 100%;
    box-sizing: border-box;
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    position: relative;

    .gradient {
      position: absolute;
      height: 75%;
      width: 100%;
      bottom: 0;
      left: 0;
      background: linear-gradient(180deg, rgba(57, 34, 0, 0) 0%, #392200 100%);
    }

    .combo-item-content {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 10px;
      padding: 8px;

      img {
        width: 40px;
      }

      span {
        font-size: 8px;
        font-weight: 400;
        line-height: 9.55px;
        text-align: center;
        color: white;
        position: relative;
        z-index: 15;
      }
    }
  }
}
</style>