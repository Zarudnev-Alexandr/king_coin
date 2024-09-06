<script setup lang="ts">
interface Props {
  buttonText?: string;
  disabledText?: string;
  isDisabled?: boolean;
  isLoading?: boolean
}

const props = defineProps<Props>();
const emits = defineEmits(['onAccept']);

const handleOnAccept = () => {
  if (props.isDisabled || props.isLoading) return;

  emits('onAccept');
}
</script>

<template>
  <div class="modal-action-button-wrapper"
       :class="{ 'active-bg': !props.isDisabled && !props.isLoading, 'loading-bg': props.isLoading ,'disabled-bg': props.isDisabled && !props.isLoading }"
       @click="handleOnAccept"
  >
    <svg width="93" height="47" viewBox="0 0 93 47" fill="none" xmlns="http://www.w3.org/2000/svg"
         style="position: absolute; right: 0; bottom: 0"
    >
      <path
          d="M93 1.11163C93 -0.0742122 90.9562 -0.366299 90.5488 0.747387C83.1305 21.0302 67.0301 37.1305 46.7474 44.5489C45.6337 44.9562 45.9258 47.0001 47.1116 47.0001H92C92.5523 47.0001 93 46.5523 93 46.0001V1.11163Z"
          fill="#703500" fill-opacity="0.2"/>
      <path
          d="M0.462709 47.0001C1.01088 47.0001 1.12169 46.1405 0.596081 45.9848C0.298249 45.8966 0 46.1195 0 46.4301V46.5376C0 46.793 0.207277 47.0001 0.462709 47.0001Z"
          fill="#703500" fill-opacity="0.2"/>
    </svg>
    <svg width="17" height="13" viewBox="0 0 17 13" fill="none" xmlns="http://www.w3.org/2000/svg"
         style="position: absolute; top: 5px; left: 5px;"
    >
      <path
          d="M15.2661 1.63794C16.4021 1.41585 16.6071 -0.0015942 15.4495 1.34597e-06C10.7303 0.00650752 6.05569 2.07262 2.87218 6.03983C1.57354 7.65816 0.637487 9.45019 0.0532487 11.3178C-0.294485 12.4293 1.15384 12.6402 1.70541 11.6144C2.26422 10.5752 2.92494 9.57273 3.68913 8.6204C6.70832 4.85797 10.8409 2.50309 15.2661 1.63794Z"
          fill="white"/>
    </svg>
    <slot>
      <span v-if="!isLoading" class="action-button-title">{{
          props.isDisabled ? props.disabledText : props.buttonText
        }}</span>
      <div v-else class="loading-indicator">
        <span class="indicator-item"/>
        <span class="indicator-item"/>
        <span class="indicator-item"/>
      </div>
    </slot>
  </div>
</template>

<style scoped>
.modal-action-button-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  box-sizing: border-box;
  border-radius: 10px 10px 0 0;
  border-left: 2px solid white;
  border-right: 2px solid white;
  border-top: 2px solid white;

  .action-button-title {
    font-family: 'SuperSquadRus', sans-serif;
    font-size: 14px;
    font-weight: 400;
    line-height: 21.62px;
    text-align: center;
    color: rgba(93, 56, 0, 1);
  }
}

.active-bg {
  background: radial-gradient(120.14% 120.14% at 50% -11.81%, #FFFFFF 0%, #FFE531 20%, #FFA531 74.03%, #FF8200 100%);
}

.loading-bg {
  background: radial-gradient(120.14% 120.14% at 50% -11.81%, #FFFFFF 0%, #EFD41C 20%, #EB8D14 74.03%, #DD7100 100%);
}

.disabled-bg {
  background-color: rgba(160, 116, 50, 1);
}

.loading-indicator {
  display: flex;
  justify-content: center;
  gap: 8px;

  .indicator-item {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    animation: loader 0.6s infinite;
  }

  .indicator-item:nth-child(1) {
    animation-delay: 0s;
  }

  .indicator-item:nth-child(2) {
    animation-delay: 0.2s;
  }

  .indicator-item:nth-child(3) {
    animation-delay: 0.4s;
  }
}

@keyframes loader {
  0%, 20%, 100% {
    background-color: rgba(93, 56, 0, 0.5);
  }
  10% {
    background-color: rgba(93, 56, 0, 1);
  }
}
</style>