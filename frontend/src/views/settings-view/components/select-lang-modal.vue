<script setup lang="ts">

import ActionModal from "@/components/ActionModal.vue";
import Languages from "@/shared/constants/languages.ts";
import {useSettingsStore} from "@/shared/pinia/settings-store.ts";

const settingsStore = useSettingsStore();

const emits = defineEmits(['close']);
const selectLang = (lang: { name: string, short: string, icon: string }) => {
  if (lang.name === settingsStore.currenLanguage?.name) return;
  settingsStore.setLanguage(lang);
  emits('close');
}

const onClose = () => {
  emits('close');
}
</script>

<template>
  <action-modal :action-button-is-hide="true" @close="onClose">
    <div class="select-lang-wrap">
      <h2 class="sf-pro-font">{{ $t('language_selection') }}</h2>

      <div v-for="item in Languages" :key="item.name" class="lang-item"
           @click="() => selectLang(item)"
           :class="{active: item.name === settingsStore.currenLanguage?.name}">
        <img :src="item.icon" alt="">
        <span class="sf-pro-font">{{ item.name }}</span>
      </div>
    </div>
  </action-modal>
</template>

<style scoped>
.select-lang-wrap {
  display: flex;
  flex-direction: column;
  padding: 30px 10px;
  gap: 15px;

  h2 {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    line-height: 40.54px;
    text-align: center;
    color: white;
  }

  .lang-item {
    display: flex;
    padding: 9px 12px;
    align-items: center;
    gap: 15px;
    background-color: rgba(93, 56, 0, 1);
    border-radius: 10px;

    img {
      width: 40px;
      height: 40px;
      border-radius: 50%;
    }

    span {
      font-size: 12px;
      font-weight: 600;
      line-height: 17.38px;
      text-align: left;
      color: white;
    }
  }

  .active {
    background: linear-gradient(90deg, #FF8200 0%, #FFC800 100%);
  }
}
</style>