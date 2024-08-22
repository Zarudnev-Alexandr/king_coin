<script setup lang="ts">

</script>

<template>
  <div class="rating-skeleton-wrap">
    <div class="rating-card-list-tab">
      <div class="rating-card-list-tab-item active">
        <span>Монеты</span>
      </div>
      <div class="rating-card-list-tab-item">
        <span>Колонны</span>
      </div>
      <div class="rating-card-list-tab-item">
        <span>Soon</span>
      </div>
    </div>

    <div class="skeleton-top-1 skeleton-loading"/>

    <div class="rating-skeleton-actual">
      <div style="height: 40px"/>
      <div class="img-wrap">
        <span class="top-10-text">{{ $t('top') }} - 10</span>
        <img src="@/assets/svg/rating-top-100.svg" alt="">
      </div>
      <div class="user-item skeleton-loading"></div>
      <div class="user-item skeleton-loading"></div>
      <div class="user-item skeleton-loading"></div>
      <div class="user-item skeleton-loading"></div>
      <div class="user-item skeleton-loading"></div>
    </div>
  </div>
</template>

<style scoped>
.rating-skeleton-wrap {
  display: flex;
  flex-direction: column;
  padding: 0 15px;
  gap: 10px;

  .rating-skeleton-actual {
    border-radius: 10px;
    background-color: rgba(57, 34, 0, 1);
    padding: 20px 10px;
    display: flex;
    flex-direction: column;
    position: relative;
    gap: 10px;

    .img-wrap {
      position: absolute;
      top: -20px;
      left: 0;
      width: 100%;
      display: flex;
      justify-content: center;

      .top-10-text {
        font-family: 'SuperSquadRus', sans-serif;
        font-size: 18px;
        font-weight: 400;
        line-height: 27.79px;
        text-align: center;
        color: white;
        position: absolute;
        top: 40%;
        bottom: 50%;
        text-shadow: -3px 3px 0 rgba(57, 34, 0, 1),
        1px 1px 0 rgba(57, 34, 0, 1),
        1px -1px 0 rgba(57, 34, 0, 1),
        -1px -1px 0 rgba(57, 34, 0, 1);
      }

      img {
        width: 232px;
      }
    }

    .user-item {
      height: 59px;
      background-color: rgba(93, 56, 0, 1);
      border-radius: 10px;
    }
  }

  .rating-card-list-tab {
    display: flex;
    border-radius: 10px;
    background-color: rgba(57, 34, 0, 1);
    padding: 5px;

    .rating-card-list-tab-item {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 12px 24px;
      border-radius: 8px;
      flex: 1;

      span {
        font-family: 'SFProText', sans-serif;
        font-size: 10px;
        font-weight: 400;
        line-height: 11.93px;
        text-align: center;
        color: white;
      }
    }

    .active {
      background-color: rgba(93, 56, 0, 1);
    }
  }

  .skeleton-top-1 {
    background-color: rgba(93, 56, 0, 1);
    width: 100%;
    height: 58px;
    border-radius: 10px;
  }
}

@keyframes skeleton-loading {
  0% {
    background-position: -150% 0;
  }
  100% {
    background-position: 150% 0;
  }
}

.skeleton-loading {
  background: linear-gradient(90deg, rgba(93, 56, 0, 1) 25%, rgba(113, 68, 0, 1) 50%, rgba(93, 56, 0, 1) 75%);
  background-size: 200% 100%; /* Увеличиваем размер фона для плавного эффекта */
  animation: skeleton-loading 1.5s infinite;
}
</style>