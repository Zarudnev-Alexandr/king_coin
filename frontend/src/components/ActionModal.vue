<script setup lang="ts">

interface Props {
  mainButtonText?: string,
}

const props = defineProps<Props>();

const emit = defineEmits(['close', 'onAccept']);

const closeActionModal = () => {
  emit('close');
}

const handleOnAccept = () => {
  emit('onAccept')
}
</script>

<template>
  <div class="action-modal-wrapper">
    <div class="action-modal">
      <svg
          viewBox="0 0 206 206"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          style="position: absolute; z-index: 1; top: 0; left: 0; width: 50%"
      >
        <path d="M205.713 0L0 205.713V10C0 4.47715 4.47715 0 10 0H205.713Z" fill="#482B00"/>
      </svg>

      <svg viewBox="0 0 339 340"
           fill="none"
           xmlns="http://www.w3.org/2000/svg"
           style="position: absolute; z-index: 1; bottom: 0; right: 0; max-width: 97%; max-height: 100%; overflow: hidden"
      >
        <path
            d="M0.378845 338.621L339 0V329.297C339 334.82 334.523 339.297 329 339.297H4.00003C2.72291 339.297 1.5017 339.058 0.378845 338.621Z"
            fill="#321E00"/>
      </svg>


      <span class="close-icon" @click="closeActionModal">
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
              d="M9.72067 0.279326C9.34823 -0.0931191 8.74434 -0.0930985 8.37191 0.279326L5 3.65124L1.62809 0.279326C1.25564 -0.0931191 0.651751 -0.0930985 0.279326 0.279326C-0.0930985 0.651751 -0.0931191 1.25564 0.279326 1.62809L3.65124 5L0.279326 8.37191C-0.0930985 8.74434 -0.0931191 9.34823 0.279326 9.72067C0.651772 10.0931 1.25567 10.0931 1.62809 9.72067L5 6.34876L8.37191 9.72067C8.74436 10.0931 9.34825 10.0931 9.72067 9.72067C10.0931 9.34825 10.0931 8.74436 9.72067 8.37191L6.34876 5L9.72067 1.62809C10.0931 1.25567 10.0931 0.651772 9.72067 0.279326Z"
              fill="#392200"/>
          </svg>
      </span>
      <span style="position: relative; z-index: 5">
        <slot></slot>
      </span>

      <div class="accept-action">
        <slot name="actions">
          <div class="accept-button-wrapper" @click="handleOnAccept">
            <span>{{ props.mainButtonText ? props.mainButtonText : 'Получить' }}</span>
          </div>
        </slot>
      </div>
    </div>
  </div>
</template>

<style scoped>
.action-modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 30;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow-y: auto;

  .action-modal {
    width: 92%;
    border-radius: 10px;
    border: 2px solid white;
    background-color: rgba(57, 34, 0, 1);
    position: relative;

    .close-icon {
      position: absolute;
      top: 10px;
      right: 10px;
      width: 26px;
      height: 26px;
      cursor: pointer;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: rgba(160, 116, 50, 1);
      border-radius: 50%;
      z-index: 5;
    }

    .accept-action {
      display: flex;
      justify-content: center;
      width: 100%;
      position: relative;
      z-index: 5;

      .accept-button-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 133px;
        height: 67px;
        background-image: url("@/assets/svg/modal-main-button-bg.svg");
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center;

        span {
          font-family: 'SuperSquadRus', sans-serif;
          font-size: 14px;
          font-weight: 400;
          line-height: 21.62px;
          text-align: center;
          color: rgba(93, 56, 0, 1);
        }
      }
    }
  }
}
</style>