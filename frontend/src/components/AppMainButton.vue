<script setup lang="ts">
interface Props {
  title: string;
}

const props: Props = defineProps<Props>();
const emit = defineEmits(['onClick']);

const handleClick = () => {
  emit('onClick');
};
</script>

<template>
  <div class="main-button-wrapper" @click="handleClick">
    <slot name="default">
      <span>{{ props.title }}</span>
    </slot>
  </div>
</template>

<style scoped>
.main-button-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/svg/main-button-bg.svg");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
}

span {
  font-family: 'SuperSquadRus', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: rgba(88, 54, 0, 1);
}
</style>
