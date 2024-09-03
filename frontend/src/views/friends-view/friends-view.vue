<script setup lang="ts">

import FriendsHeader from "@/views/friends-view/components/friends-header.vue";
import InviteInfoCards from "@/views/friends-view/components/InviteInfoCards.vue";
import FloatButton from "@/components/FloatButton.vue";
import CoinCountItem from "@/views/friends-view/components/coin-count-item.vue";
import FriendItem from "@/views/friends-view/components/friend-item.vue";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import FriendsApiService from "@/shared/api/services/friends-api-service.ts";
import {onMounted, ref} from "vue";
import {copyTextToClipboard} from "@/helpers/clipbaord.ts";
import {useFriendsStore} from "@/shared/pinia/friends-store.ts";
import VibrationService from "@/shared/api/services/vibration-service.ts";
import FriendsSkeleton from "@/views/friends-view/components/friends-skeleton.vue";
import {useAppStore} from "@/shared/pinia/app-store.ts";
import {ToastType} from "@/shared/api/types/toast.ts";
import {useI18n} from "vue-i18n";
import {Friend} from "@/shared/api/types/friend.ts";

const friendApiService = new FriendsApiService(axiosInstance, errorHandler);
const friendsStore = useFriendsStore();
const appStore = useAppStore();
const {t} = useI18n();
const vibrationService = new VibrationService();
const shareHref = ref('');
const isLoading = ref(false);

const copy = () => {
  copyTextToClipboard(friendsStore.referralLink || '');
  appStore.pushToast(ToastType.SUCCESS, t('link_copied'));
}

onMounted(async () => {
  vibrationService.light();
  if (!friendsStore.referralLink) {
    friendApiService.getRefLink().then((res) => {
      if (res && res.right) {
        friendsStore.setReferralLink(res.right.referral_link);
        shareHref.value = `https://t.me/share/url?url=${res.right.referral_link}&text=${t('invite_text')}`;
      }
    });
  }

  if (!friendsStore.friendsList) {
    isLoading.value = true;
    friendApiService.getFriends().then((res) => {
      if (res && res.right) {
        friendsStore.setFriendsList(res.right);
        let sumIncome = 0;

        res.right.forEach((friend: Friend) => {
          sumIncome += friend.earned_money;
        });
        friendsStore.setSumAllProfits(sumIncome);
        isLoading.value = false;
      }
    });
  }
});
</script>

<template>
  <div class="friend-wrapper">
    <FriendsHeader/>
    <InviteInfoCards style="margin-top: 10px;"/>
    <div class="invite-buttons" v-if="friendsStore.referralLink !== ''">
      <a :href="shareHref" style="flex: 1">
        <FloatButton style="height: 65px;">
          <div class="button-content">
            <span>{{ $t('invite_a_friend') }}</span>
            <img src="@/assets/svg/friends/main-invite-button-icon.png" alt="">
          </div>
        </FloatButton>
      </a>

      <FloatButton style="height: 65px; width: 65px;" @click="copy">
        <img src="@/assets/svg/copy-icon.svg" alt="" style="width: 21.45px; height: 23.71px;">
      </FloatButton>
    </div>

    <div class="friends-list-wrap" v-if="!isLoading">
      <div class="all-friend-statistic-wrap" v-if="friendsStore.friendsList">
        <span class="sf-pro-font">{{ $t('your_friends') }} ({{ friendsStore.friendsList.length }})</span>
        <CoinCountItem :count="friendsStore.sumAllProfits"/>
      </div>
      <div class="friends-list" v-if="friendsStore.friendsList">
        <FriendItem v-for="item in friendsStore.friendsList" :friend-data="item"/>
      </div>

    </div>
    <friends-skeleton v-else/>
    <h1/>
  </div>
</template>

<style scoped>
.friend-wrapper {
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
  padding-bottom: 80px;

  .invite-buttons {
    display: flex;
    gap: 10px;
    padding: 0 16px;

    .button-content {
      display: flex;
      gap: 5px;

      span {
        font-family: 'SuperSquadRus', sans-serif;
        font-size: 14px;
        font-weight: 400;
        line-height: 21.62px;
        text-align: center;
        color: rgba(88, 54, 0, 1);
      }

      img {
        width: 20.5px;
        height: 22.5px;
      }
    }
  }

  .friends-list-wrap {
    display: flex;
    flex-direction: column;
    padding: 15px 10px;
    margin: 0 16px;
    border-radius: 10px;
    background-color: rgba(57, 34, 0, 1);
    gap: 10px;

    .friends-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .all-friend-statistic-wrap {
      display: flex;
      justify-content: space-between;
      padding: 0 10px;

      span {
        font-size: 12px;
        font-weight: 600;
        line-height: 14.32px;
        text-align: left;
        color: white;
      }
    }
  }
}
</style>