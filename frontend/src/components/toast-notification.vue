<script setup lang="ts">
import {useAppStore} from "@/shared/pinia/app-store.ts";
import {ToastType} from "@/shared/api/types/toast.ts";

const appStore = useAppStore();
</script>

<template>
  <div class="toast-wrap">
    <transition-group name="toast" tag="div" style="display: flex; flex-direction: column; gap: 5px">
      <div class="toast-item" v-for="(item, index) in appStore.toasts" :key="index">
        <img src="@/assets/svg/toast/success.svg" alt="success" v-if="item.type === ToastType.SUCCESS">
        <img src="@/assets/svg/toast/error.svg" alt="error" v-if="item.type === ToastType.ERROR">
        <img src="@/assets/svg/toast/warning.svg" alt="warning" v-if="item.type === ToastType.WARNING">
        <span class="sf-pro-font">{{ item.message }}</span>
        <div style="width: 30px"/>
        <img src="@/assets/svg/toast/close.svg" alt="close" @click="() => appStore.removeToast(index)">
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.toast-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  position: absolute;
  top: 20px;
  left: 0;
  z-index: 20;
  width: 100%;

  .toast-item {
    display: flex;
    align-items: center;
    padding: 8px 14px;
    background-color: rgba(93, 56, 0, 1);
    border-radius: 9px;
    transition: all 0.3s ease;
    gap: 10px;

    span {
      font-size: 12px;
      font-weight: 600;
      line-height: 17.38px;
      text-align: left;
      color: white;
    }

    img {
      width: 20px;
      height: 20px;
    }
  }
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.toast-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.toast-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
