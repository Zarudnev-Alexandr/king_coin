<script setup lang="ts">

</script>

<template>
  <div class="invite-info-cards-wrap">
    <div class="banner-item">
      <div class="banner-item-up-block">
        <span class="sf-pro-font">Пригласить друга</span>
        <img src="@/assets/svg/friends/invite-friend-banner.png" alt="">
      </div>
      <div class="banner-item-down-block">
        <div class="banner-item-reward">
          <img src="@/assets/svg/coin.svg" alt="">
          <span class="sf-pro-font">+ 5 000</span>
        </div>
        <span class="sf-pro-font">для вас и вашего друга</span>
      </div>
    </div>
    <div class="banner-item">
      <img src="@/assets/svg/friends/invite-card-up-coin.png" alt="" class="premium-up-coin">
      <img src="@/assets/svg/friends/invite-friends-card-down-coin.png" alt="" class="premium-down-coin">
      <div class="banner-item-up-block">
        <span class="sf-pro-font">Пригласить друга с Premium</span>
        <img src="@/assets/svg/friends/invite-friend-premium-banner.png" alt="">
      </div>
      <div class="banner-item-down-block">
        <div class="banner-item-reward">
          <img src="@/assets/svg/coin.svg" alt="">
          <span class="sf-pro-font">+ 25 000</span>
        </div>
        <span class="sf-pro-font">для вас и вашего друга</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.invite-info-cards-wrap {
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 0 16px;

  .banner-item {
    display: flex;
    flex: 1;
    flex-direction: column;
    border-radius: 10px;
    background-color: rgba(57, 34, 0, 1);
    padding: 10px;
    position: relative;

    .banner-item-down-block {
      display: flex;
      flex-direction: column;
      gap: 5px;

      .banner-item-reward {
        display: flex;
        align-items: center;
        gap: 5px;

        img {
          width: 18px;
          height: 18px;
        }

        span {
          font-size: 12px;
          font-weight: 700;
          line-height: 14.32px;
          text-align: center;
          color: white;
        }
      }

      span {
        font-size: 10px;
        font-weight: 400;
        line-height: 11.93px;
        text-align: left;
        color: rgba(238, 214, 147, 1);
      }
    }

    .banner-item-up-block {
      display: flex;
      justify-content: space-between;

      span {
        font-size: 12px;
        font-weight: 600;
        line-height: 14.32px;
        text-align: left;
        color: white;
      }

      img {
        width: 52px;
        height: 53px;
      }
    }

    .premium-up-coin {
      position: absolute;
      width: 20px;
      height: 20px;
      top: -10px;
      right: 40%;
    }

    .premium-down-coin {
      position: absolute;
      width: 26px;
      height: 29px;
      right: -7px;
      bottom: 22%;
    }
  }
}
</style>