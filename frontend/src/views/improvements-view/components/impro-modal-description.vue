<script setup lang="ts">
import {useImprovementsStore} from "@/shared/pinia/improvements-store.ts";
import FloatButton from "@/components/FloatButton.vue";
import {computed} from "vue";

const improStore = useImprovementsStore();

const getDescription = () => {
  if (improStore.selectCoinForImpro?.conditions_met) return improStore.selectCoinForImpro?.description;

  const type = improStore.selectCoinForImpro?.unmet_conditions[0].type;
  const name = improStore.selectCoinForImpro?.unmet_conditions[0].name_of_condition_upgrade;

  if (type === 'subscribe_telegram') {
    return `Чтобы разблокировать эту карточку сначала подпишитесь на Telegram канал ${name}`;
  }
  return improStore.selectCoinForImpro?.description
}

const goToSubscribe = () => {
  window.open(improStore.selectCoinForImpro?.unmet_conditions[0].description, '_blank');
}

const isSubscribeType = computed(() => {
  const type = improStore.selectCoinForImpro?.unmet_conditions[0].type;
  return !improStore.selectCoinForImpro?.conditions_met && type === 'subscribe_telegram';
})
</script>

<template>
  <div class="impro-modal-description-wrap">
    <span class="sf-pro-font z-10 impro-description">{{ getDescription() }}</span>
    <FloatButton v-if="isSubscribeType" @click="goToSubscribe" style="width: 128px; height: 55.69px">
      <h3>{{ $t('subscribe') }}</h3>
    </FloatButton>
  </div>
</template>

<style scoped>
.impro-modal-description-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;

  h3 {
    font-family: 'SuperSquadRus', sans-serif;
    font-size: 14px;
    font-weight: 400;
    line-height: 21.62px;
    text-align: center;
    color: rgba(93, 56, 0, 1);
  }

  .impro-description {
    font-size: 10px;
    font-weight: 400;
    line-height: 11.93px;
    text-align: center;
    color: rgba(194, 163, 117, 1);
    width: 80%;
  }
}

.z-10 {
  position: relative;
  z-index: 10;
}
</style>