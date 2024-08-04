<script setup lang="ts">

import FriendsHeader from "@/views/friends-view/components/friends-header.vue";
import InviteInfoCards from "@/views/friends-view/components/InviteInfoCards.vue";
import FloatButton from "@/components/FloatButton.vue";
import CoinCountItem from "@/views/friends-view/components/coin-count-item.vue";
import FriendItem from "@/views/friends-view/components/friend-item.vue";
import {axiosInstance, errorHandler} from "@/shared/api/axios/axios-instance.ts";
import FriendsApiService from "@/shared/api/services/friends-api-service.ts";
import {onMounted} from "vue";
import {copyTextToClipboard} from "@/helpers/clipbaord.ts";
import {useFriendsStore} from "@/shared/pinia/friends-store.ts";

const friendApiService = new FriendsApiService(axiosInstance, errorHandler);
const friendsStore = useFriendsStore();

const copy = () => {
  copyTextToClipboard(friendsStore.referralLink || '');
}

onMounted(async () => {

  if (!friendsStore.referralLink) {
    friendApiService.getRefLink().then((res) => {
      if (res && res.right) {
        friendsStore.setReferralLink(res.right.referral_link);
      }
    });
  }

  if (!friendsStore.friendsList) {
    friendApiService.getFriends().then((res) => {
      if (res && res.right) {
        friendsStore.setFriendsList(res.right);
        let sumIncome = 0;

        res.right.forEach((friend: any) => {
          sumIncome += friend.external_income_field;
        });
        friendsStore.setSumAllProfits(sumIncome);
      }
    });
  }
});
</script>

<template>
  <div class="friend-wrapper">
    <FriendsHeader/>
    <InviteInfoCards/>

    <div class="invite-buttons" v-if="friendsStore.referralLink !== ''">
      <FloatButton style="flex: 1; height: 65px;">
        <div class="button-content">
          <span>Пригласить друга</span>
          <img src="@/assets/svg/friends/main-invite-button-icon.png" alt="">
        </div>
      </FloatButton>
      <FloatButton style="height: 65px; width: 65px;" @click="copy">
        <img src="@/assets/svg/copy-icon.svg" alt="" style="width: 21.45px; height: 23.71px;">
      </FloatButton>
    </div>

    <div class="friends-list-wrap">
      <div class="all-friend-statistic-wrap" v-if="friendsStore.friendsList">
        <span class="sf-pro-font">Ваши друзья ({{ friendsStore.friendsList.length }})</span>
        <CoinCountItem :count="friendsStore.sumAllProfits"/>
      </div>
      <div class="friends-list" v-if="friendsStore.friendsList">
        <FriendItem v-for="item in friendsStore.friendsList" :friend-data="item"/>
      </div>
    </div>
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
  background-image: url('@/assets/img/app-bg.png');
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