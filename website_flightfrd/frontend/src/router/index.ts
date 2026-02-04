import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AircraftView from '../views/AircraftView.vue'
import ATCView from '../views/ATCView.vue'
import CalendarView from '../views/CalendarView.vue'
import AboutView from '../views/AboutView.vue'
import NotFoundView from '../views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/aircraft',
      name: 'aircraft-list',
      component: AircraftView
    },
    {
      path: '/aircraft/:id',
      name: 'aircraft-detail',
      component: AircraftView,
      props: true
    },
    {
      path: '/atc',
      name: 'atc',
      component: ATCView
    },
    {
      path: '/calendar',
      name: 'calendar',
      component: CalendarView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView
    }
  ]
})

export default router