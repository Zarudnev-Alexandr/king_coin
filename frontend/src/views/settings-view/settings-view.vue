<script setup lang="ts">

import SettingsHeader from "@/views/settings-view/components/settings-header.vue";
import {useSettingsStore} from "@/shared/pinia/settings-store.ts";
import SelectLangModal from "@/views/settings-view/components/select-lang-modal.vue";
import {ref} from "vue";
import AppIconButton from "@/components/AppIconButton.vue";
import SoundOnSvg from "@/assets/svg/settings/sound-on.svg"
import SoundOffSvg from "@/assets/svg/settings/sound-off.svg"
import VibrationOnSvg from "@/assets/svg/settings/vibration-on.svg"
import VibrationOffSvg from "@/assets/svg/settings/vibration-off.svg"
import FloatButton from "@/components/FloatButton.vue";
import RemoveAccountModal from "@/views/settings-view/components/remove-account-modal.vue";
import UserApiService from "@/shared/api/services/user-api-service.ts";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";

const settingsStore = useSettingsStore();
const userApiService = new UserApiService(axiosInstance, errorHandler);
const selectLangIsOpen = ref(false);
const removeModalIsVisible = ref(false);
const lang = Telegram.WebApp.initDataUnsafe.user?.language_code;

const closeSelectLangModal = () => {
  selectLangIsOpen.value = false;
}

const openSelectLangModal = () => {
  selectLangIsOpen.value = true;
}

const toggleSound = () => {
  settingsStore.setSoundOn(!settingsStore.soundOn);
}

const toggleVibration = () => {
  settingsStore.setVibrationOn(!settingsStore.vibrationOn);
}

const closeRemoveModal = () => {
  removeModalIsVisible.value = false;
}

const openRemoveModal = () => {
  removeModalIsVisible.value = true;
}

const acceptRemoveAccount = async () => {
  const res = await userApiService.removeProfile();

  if (res && res.right) {
    Telegram.WebApp.close();
  }
}
</script>

<template>
  <div class="settings-wrapper">
    <settings-header/>

    <div class="current-lang-wrapper" @click="openSelectLangModal">
      <img :src="settingsStore.currenLanguage?.icon" alt="" class="lang-icon">
      <div class="lang-content">
        <h3 class="sf-pro-font">{{ $t('change_language') }}</h3>
        <span class="sf-pro-font">{{ settingsStore.currenLanguage?.name }}</span>
      </div>
      <div style="flex: 1"/>
      <img src="@/assets/svg/settings/arrow-right.svg" alt="" class="arrow">
    </div>
    <div style="height: 20px"/>
    <div class="toggle-button-wrapper">
      <app-icon-button style="width: 48px; height: 48px;"
                       @on-click="toggleSound"
                       :class="{'off-bg': !settingsStore.soundOn}">
        <img :src="settingsStore.soundOn ? SoundOnSvg : SoundOffSvg" alt="">
      </app-icon-button>
      <app-icon-button style="width: 48px; height: 48px;"
                       @on-click="toggleVibration"
                       :class="{'off-bg': !settingsStore.vibrationOn}">
        <img :src="settingsStore.vibrationOn ? VibrationOnSvg : VibrationOffSvg" alt="">
      </app-icon-button>

      <div style="display: flex; justify-content: center">
        <span style="font-size: 20px;">Lang: {{ lang }}</span>
      </div>
    </div>
    <div style="flex: 1"></div>
    <div style="display: flex; justify-content: center;">
      <FloatButton style="width: 124px; height: 55px;" @click="openRemoveModal">
        <span class="remove-btn">{{ $t('delete_account') }}</span>
      </FloatButton>
    </div>
    <h1></h1>
    <select-lang-modal @close="closeSelectLangModal" v-if="selectLangIsOpen"/>
    <remove-account-modal v-if="removeModalIsVisible" @close="closeRemoveModal" @accept="acceptRemoveAccount"/>
  </div>
</template>

<style scoped>
.settings-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  margin: 0 auto;
  background-image: url('@/assets/img/app-bg.webp');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  overflow-y: auto;
  gap: 10px;
  padding: 0 25px;
  box-sizing: border-box;

  .toggle-button-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }

  .current-lang-wrapper {
    background-color: rgba(93, 56, 0, 1);
    border-radius: 10px;
    padding: 9px 12px;
    display: flex;
    align-items: center;
    gap: 15px;

    .lang-icon {
      width: 40px;
      height: 40px;
      border-radius: 50%;
    }

    .arrow {
      width: 24px;
      height: 24px;
    }

    .lang-content {
      display: flex;
      flex-direction: column;
      justify-content: center;

      h3 {
        font-size: 12px;
        font-weight: 600;
        line-height: 17.38px;
        text-align: left;
        color: white;
        margin: 0;
      }

      span {
        font-size: 9px;
        font-weight: 400;
        line-height: 13.03px;
        text-align: left;
        color: rgba(238, 214, 147, 1);
      }
    }
  }
}

.remove-btn {
  font-family: 'SuperSquadRus', sans-serif;
  font-size: 8px;
  font-weight: 400;
  line-height: 12.35px;
  text-align: center;
  color: rgba(93, 56, 0, 1);
}

.off-bg {
  background: rgba(57, 34, 0, 1) !important;
}
</style>