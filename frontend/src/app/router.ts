import {createRouter, createWebHistory} from "vue-router";
import MainView from "../views/main-view/MainView.vue";

const router = createRouter(
  {
    history: createWebHistory(),
    routes: [
      {
        path: "/",
        name: 'Main',
        component: MainView
      },
      {
        path: '/improvements',
        name: 'Improvements',
        component: () => import('../views/improvements-view/ImprovementsView.vue')
      },
      {
        path: '/friends',
        name: 'Friends',
        component: () => import('../views/friends-view/friends-view.vue')
      },
      {
        path: '/income',
        name: 'Income',
        component: () => import('../views/income-view/IncomeView.vue')
      },
      {
        path: '/gameplay',
        name: 'Gameplay',
        component: () => import('../views/game-view/GameView.vue')
      }
    ]
  }
);

export default router;