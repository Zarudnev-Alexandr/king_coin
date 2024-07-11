<script setup lang="ts">
import CoinCardGridSimpleItem from "@/views/improvements-view/components/coin-card-grid-simple-item.vue";
import CoinCardGridSpecialItem from "@/views/improvements-view/components/coin-card-grid-special-item.vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";

interface Props {
  cardList: any[],
  currentTab: string,
}

const props: Props = defineProps<Props>();
const appStore = useAppStore();

const onSelectCardForImpro = (card: any) => {
  appStore.setSelectCoinForImpro(card);
}
</script>

<template>
  <div class="coin-grid-wrapper" v-if="props.currentTab === 'Special'">
    <CoinCardGridSpecialItem
        v-for="item in props.cardList"
        :key="item.id"
        :card-item="item"
        @click="() => onSelectCardForImpro(item)"
    />
    <div v-if="props.cardList.length % 2 !== 0" style="width: 48%"></div>
  </div>
  <div class="coin-grid-wrapper" v-else>
    <CoinCardGridSimpleItem
        v-for="item in props.cardList"
        :key="item.id"
        :card-item="item"
        @click="() => onSelectCardForImpro(item)"
    />
    <div v-if="props.cardList.length % 2 !== 0" style="width: 48%"></div>
  </div>
</template>

<style scoped>
.coin-grid-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}
</style>