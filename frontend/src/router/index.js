import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/owner',
    name: 'OwnerHome',
    component: () => import('../views/owner/Home.vue'),
    meta: { requireAuth: true, role: 'owner' }
  },
  {
    path: '/owner/repair',
    name: 'OwnerRepair',
    component: () => import('../views/owner/Repair.vue'),
    meta: { requireAuth: true, role: 'owner' }
  },
  {
    path: '/owner/feedback',
    name: 'OwnerFeedback',
    component: () => import('../views/owner/Feedback.vue'),
    meta: { requireAuth: true, role: 'owner' }
  },
  {
    path: '/owner/evaluation',
    name: 'OwnerEvaluation',
    component: () => import('../views/owner/Evaluation.vue'),
    meta: { requireAuth: true, role: 'owner' }
  },
  {
    path: '/owner/profile',
    name: 'OwnerProfile',
    component: () => import('../views/owner/Profile.vue'),
    meta: { requireAuth: true, role: 'owner' }
  },
  {
    path: '/staff',
    name: 'StaffHome',
    component: () => import('../views/staff/Home.vue'),
    meta: { requireAuth: true, role: 'staff' }
  },
  {
    path: '/staff/repair-list',
    name: 'StaffRepairList',
    component: () => import('../views/staff/RepairList.vue'),
    meta: { requireAuth: true, role: 'staff' }
  },
  {
    path: '/staff/feedback-list',
    name: 'StaffFeedbackList',
    component: () => import('../views/staff/FeedbackList.vue'),
    meta: { requireAuth: true, role: 'staff' }
  },
  {
    path: '/staff/lost-items',
    name: 'StaffLostItems',
    component: () => import('../views/staff/LostItems.vue'),
    meta: { requireAuth: true, role: 'staff' }
  },
  {
    path: '/staff/notifications',
    name: 'StaffNotifications',
    component: () => import('../views/staff/Notifications.vue'),
    meta: { requireAuth: true, role: 'staff' }
  },
  {
    path: '/staff/profile',
    name: 'StaffProfile',
    component: () => import('../views/staff/Profile.vue'),
    meta: { requireAuth: true, role: 'staff' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    const storedUser = store.getUser()
    if (!storedUser) {
      next('/login')
      return
    }
    if (to.meta.role && storedUser.user.role !== to.meta.role) {
      next('/login')
      return
    }
  }
  next()
})

export default router