<script setup lang="ts">
import CoinCountItem from "@/views/friends-view/components/coin-count-item.vue";
import {Friend} from "@/shared/api/types/friend.ts";
import {getLevelByIndex} from "@/helpers/levels.ts";

interface Props {
  friendData: Friend
}

const props: Props = defineProps<Props>();
</script>

<template>
  <div class="friend-item-wrap">
    <img src="@/assets/svg/friends/friend-item-avatar-example.png" alt="">
    <div class="friend-item-name-wrap">
      <span class="sf-pro-font">{{ props.friendData.fio }}</span>
      <div class="friend-item-league">
        <img src="@/assets/svg/friends/friend-grandmaster-league-icon.png" alt="">
        <span class="sf-pro-font">{{ getLevelByIndex(props.friendData.lvl).name }}</span>
      </div>
    </div>
    <div class="friend-item-profit-wrap">
      <CoinCountItem :count="props.friendData.external_income_field"/>
      <div class="friend-invite-count-wrap">
        <img src="@/assets/svg/friends/friend-group-icon.png" alt="">
        <span class="sf-pro-font">+ {{ props.friendData.invited_count }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.friend-item-wrap {
  width: 100%;
  border-radius: 10px;
  padding: 9px 12px;
  background-color: rgba(93, 56, 0, 1);
  display: flex;
  box-sizing: border-box;
  gap: 10px;

  .friend-item-profit-wrap {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-end;
    gap: 5px;

    .friend-invite-count-wrap {
      display: flex;
      align-items: center;
      gap: 3px;

      img {
        width: 10px;
        height: 10px;
      }

      span {
        font-size: 10px;
        font-weight: 400;
        line-height: 11.93px;
        text-align: right;
        color: rgba(238, 214, 147, 1);
      }
    }
  }

  .friend-item-name-wrap {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 5px;
    flex: 1;

    span {
      font-size: 12px;
      font-weight: 600;
      line-height: 14.32px;
      text-align: left;
      color: white;
    }

    .friend-item-league {
      display: flex;
      align-items: center;
      gap: 2px;

      img {
        width: 6.28px;
        height: 8px;
      }

      span {
        font-size: 10px;
        font-weight: 400;
        line-height: 11.93px;
        text-align: left;
        color: rgba(238, 214, 147, 1);
      }
    }


  }

  img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
}
</style>