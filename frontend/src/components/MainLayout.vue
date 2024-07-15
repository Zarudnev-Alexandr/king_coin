<script setup lang="ts">
import BottomMenu from "@/components/BottomMenu.vue";
import CardImprovementsModalContent from "@/views/improvements-view/components/card-improvements-modal-content.vue";
import TaskFulfillModal from "@/views/income-view/components/task-fulfill-modal.vue";
</script>

<template>
  <div style="width: 100%; height: 100%; position: relative;">
    <router-view/>
    <BottomMenu/>
    <CardImprovementsModalContent/>
    <TaskFulfillModal/>
  </div>
</template>

<style scoped>

</style>