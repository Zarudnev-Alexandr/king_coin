<script setup lang="ts">
import TAppApiService from "@/shared/api/services/t-app-api-service.ts";
import {errorHandler} from "@/shared/api/axios/axios-instance.ts";
import {useIncomeStore} from "@/shared/pinia/income-store.ts";
import {onMounted, ref, Ref} from "vue";
import TAppTaskItem from "@/views/income-view/components/t-app-task-item.vue";
import ModalActionButton from "@/components/ModalActionButton.vue";
import ActionModal from "@/components/ActionModal.vue";
import FeedItem from "@/shared/api/types/feed-item.ts";
import {useI18n} from "vue-i18n";
import {formatNumberWithSpaces} from "@/helpers/formats.ts";
import FloatButton from "@/components/FloatButton.vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import {useUserStore} from "@/shared/pinia/user-store.ts";

const tappApiService = new TAppApiService(errorHandler);
const appStore = useAppStore();
const userStore = useUserStore();
const {t} = useI18n();
const loadingCheck = ref(false);
const {setTAppTasks, tAppTasks, setTAppTaskLoading, tAppTaskLoading, isLoading} = useIncomeStore();
const selectedFeed: Ref<FeedItem | null> = ref(null);

const setSelectedFeed = (feed: FeedItem | null) => {
  selectedFeed.value = feed;
}

const getTasks = async () => {
  if (tAppTasks.length !== 0) return;

  setTAppTaskLoading(true);
  const res = await tappApiService.getFeeds();

  if (res && res.right) {
    setTAppTasks(res.right);
    setTAppTaskLoading(false);
  }
}

const checkTask = async () => {
  loadingCheck.value = true;
  const res = await tappApiService.check(selectedFeed.value!);
  if (res) {
    userStore.moneyPlus(selectedFeed.value!.payout * 100000);
    selectedFeed.value!.is_done = true;
    setSelectedFeed(null);
    appStore.playCoinAnimation();
  }
  loadingCheck.value = false;
}

const goToSubscribe = async () => {
  window.open(selectedFeed.value?.url ?? '', '_blank');
  await tappApiService.onClick(selectedFeed.value!);
}

onMounted(() => {
  getTasks();
})
</script>

<template>
  <div class="tapp-tasks-wrap" v-if="!tAppTaskLoading && !isLoading">
    <h3 class="sf-pro-font">T app Tasks</h3>
    <div class="task-list-wrap">
      <t-app-task-item v-for="(task, index) in tAppTasks"
                       :key="index"
                       :task-item="task"
                       @on-click-open="() => setSelectedFeed(task)"/>
    </div>
  </div>
  <ActionModal v-if="selectedFeed"
               @close="() => setSelectedFeed(null)"
               @on-accept="checkTask"
               :main-button-text="selectedFeed.is_done ?  t('completed') : t('check')">
    <template #actions>
      <modal-action-button
          style="width: 133px; height: 67px"
          :button-text="selectedFeed.is_done ?  t('completed') : t('check')"
          @on-accept="checkTask"
          :is-disabled="selectedFeed.is_done"
          :is-loading="loadingCheck"
          :disabled-text="t('completed')"
      />
    </template>
    <template #default>
      <div class="fulfill-tapp-modal-wrap">
        <img :src="selectedFeed.icon" alt="">
        <span class="card-name sf-pro-font">{{ selectedFeed.name }}</span>
        <div class="description-wrap">
          <span class="fulfill-description sf-pro-font">{{ selectedFeed.description }}</span>
          <FloatButton @click="goToSubscribe" style="width: 128px; height: 56px">
            <h3 class="subscribe-btn">{{ selectedFeed.btn_label }}</h3>
          </FloatButton>
        </div>
        <div class="fulfill-price">
          <img src="@/assets/svg/coin.svg" alt="">
          <span class="sf-pro-font">{{ formatNumberWithSpaces(selectedFeed.payout * 100000) }}</span>
        </div>
      </div>
    </template>
  </ActionModal>
</template>

<style scoped>
.fulfill-tapp-modal-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 15px;
  padding-bottom: 10px;
  padding-top: 30px;

  .description-wrap {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;

    .subscribe-btn {
      font-family: 'SuperSquadRus', sans-serif;
      font-size: 14px;
      font-weight: 400;
      line-height: 21.62px;
      text-align: center;
      color: rgba(93, 56, 0, 1);
    }
  }

  img {
    border-radius: 10px;
    width: 106px;
    height: auto;
  }

  .card-name {
    font-size: 28px;
    font-weight: 800;
    line-height: 33.41px;
    text-align: center;
    color: white;
  }

  .fulfill-description {
    font-size: 10px;
    font-weight: 400;
    line-height: 11.93px;
    text-align: center;
    color: rgba(194, 163, 117, 1);
    width: 70%;
  }

  .fulfill-price {
    display: flex;
    gap: 8px;
    justify-content: center;
    align-items: center;

    img {
      width: 30px;
      height: 30px;
    }

    span {
      font-size: 28px;
      font-weight: 800;
      line-height: 33.41px;
      text-align: left;
      color: white;
    }
  }
}

.tapp-tasks-wrap {
  background-color: rgba(57, 34, 0, 1);
  border-radius: 10px;
  padding: 15px 10px;
  display: flex;
  flex-direction: column;
  position: relative;

  .task-list-wrap {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  img {
    width: 70px;
    height: 67px;
    position: absolute;
    top: -30px;
    right: 5px;
  }

  h3 {
    font-size: 12px;
    font-weight: 600;
    line-height: 14px;
    text-align: left;
    color: white;
    padding-left: 15px;
  }
}
</style>