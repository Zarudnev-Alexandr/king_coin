<script setup lang="ts">
const emit = defineEmits(['onClick']);

const onClick = () => {
  emit('onClick');
};
</script>

<template>
  <div class="bg-icon" @click="onClick">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none"
         xmlns="http://www.w3.org/2000/svg"
         style="position: absolute; top: 2px; left: 2px"
    >
      <path fill-rule="evenodd" clip-rule="evenodd"
            d="M0.894775 23.0526C0.894775 23.8853 1.99768 23.8609 2.17679 23.0478C4.49561 12.5204 12.7836 4.23244 23.311 1.91363C24.1241 1.73452 24.1485 0.631592 23.3158 0.631592C10.933 0.631592 0.894775 10.6698 0.894775 23.0526Z"
            fill="white" fill-opacity="0.5"/>
    </svg>

    <svg width="37" height="31" viewBox="0 0 37 31" fill="none"
         xmlns="http://www.w3.org/2000/svg"
         style="position: absolute; bottom: 2px; right: 2px;"
    >
      <path fill-rule="evenodd" clip-rule="evenodd"
            d="M35.7281 1.01862C35.4206 0.0229844 34.0391 0.2772 33.8789 1.30685C31.8091 14.6094 20.304 24.7895 6.4211 24.7895C4.67669 24.7895 2.96982 24.6288 1.3145 24.3214C0.289487 24.131 -0.411803 25.3543 0.424035 25.9774C4.21272 28.8018 8.91117 30.4737 14.0001 30.4737C26.5573 30.4737 36.737 20.294 36.737 7.73684C36.737 5.39816 36.3839 3.14195 35.7281 1.01862Z"
            fill="#703500" fill-opacity="0.2"/>
    </svg>


    <slot></slot>
  </div>
</template>

<style scoped>
.bg-icon {
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  background: radial-gradient(120.14% 120.14% at 50% -11.81%, #FFFFFF 0%, #FFE531 20%, #FFA531 74.03%, #FF8200 100%);
  border-radius: 50%;
  position: relative;
}
</style>