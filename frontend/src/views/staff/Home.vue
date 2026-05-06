<template>
  <div class="min-h-screen bg-gray-100">
    <div class="bg-green-500 text-white p-6">
      <h1 class="text-xl font-bold">掌上物业 - 管理端</h1>
      <p class="text-green-100 mt-1">欢迎, {{ user?.username }}</p>
    </div>

    <div class="p-4">
      <div class="grid grid-cols-2 gap-4 mb-6">
        <div 
          @click="navigateTo('/staff/repair-list')"
          class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition"
        >
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-3">
            <span class="text-2xl">🔧</span>
          </div>
          <h3 class="font-medium text-gray-800">维修记录</h3>
          <p class="text-sm text-gray-500 mt-1">{{ pendingCount }} 条待处理</p>
        </div>
        <div 
          @click="navigateTo('/staff/feedback-list')"
          class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition"
        >
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3">
            <span class="text-2xl">💬</span>
          </div>
          <h3 class="font-medium text-gray-800">问题反馈</h3>
          <p class="text-sm text-gray-500 mt-1">{{ feedbackCount }} 条待处理</p>
        </div>
        <div 
          @click="navigateTo('/staff/lost-items')"
          class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition"
        >
          <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mb-3">
            <span class="text-2xl">🔍</span>
          </div>
          <h3 class="font-medium text-gray-800">失物招领</h3>
          <p class="text-sm text-gray-500 mt-1">管理失物信息</p>
        </div>
        <div 
          @click="navigateTo('/staff/notifications')"
          class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition"
        >
          <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-3">
            <span class="text-2xl">📢</span>
          </div>
          <h3 class="font-medium text-gray-800">通知广播</h3>
          <p class="text-sm text-gray-500 mt-1">发布小区通知</p>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm mb-6">
        <h3 class="font-medium text-gray-800 mb-4">待处理报修</h3>
        <div v-if="pendingRepairs.length === 0" class="text-center text-gray-400 py-8">
          <span class="text-4xl block mb-2">✅</span>
          <p>暂无待处理报修</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="repair in pendingRepairs.slice(0, 3)" 
            :key="repair.id"
            class="border border-gray-200 rounded-lg p-3"
          >
            <div class="flex justify-between items-start">
              <div>
                <h4 class="font-medium">{{ repair.title }}</h4>
                <p class="text-sm text-gray-500 mt-1">{{ repair.create_time }}</p>
              </div>
              <span class="bg-yellow-100 text-yellow-700 px-2 py-1 rounded text-xs">待处理</span>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm">
        <h3 class="font-medium text-gray-800 mb-4">最新通知</h3>
        <div v-if="notifications.length === 0" class="text-center text-gray-400 py-8">
          <span class="text-4xl block mb-2">📢</span>
          <p>暂无通知</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="notification in notifications.slice(0, 3)" 
            :key="notification.id"
            class="border border-gray-200 rounded-lg p-3"
          >
            <h4 class="font-medium">{{ notification.title }}</h4>
            <p class="text-sm text-gray-500 mt-1">{{ notification.create_time }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 flex justify-around">
      <button @click="navigateTo('/staff')" class="flex flex-col items-center text-green-500">
        <span class="text-2xl">🏠</span>
        <span class="text-xs mt-1">首页</span>
      </button>
      <button @click="navigateTo('/staff/repair-list')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">🔧</span>
        <span class="text-xs mt-1">维修</span>
      </button>
      <button @click="navigateTo('/staff/feedback-list')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">💬</span>
        <span class="text-xs mt-1">反馈</span>
      </button>
      <button @click="navigateTo('/staff/profile')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">👤</span>
        <span class="text-xs mt-1">我的</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { repairAPI, feedbackAPI, notificationAPI } from '../../api'
import store from '../../store'

const router = useRouter()
const user = ref(null)
const pendingRepairs = ref([])
const notifications = ref([])
const pendingCount = ref(0)
const feedbackCount = ref(0)

onMounted(() => {
  user.value = store.getUser()?.user
  loadData()
})

const loadData = async () => {
  try {
    const [repairRes, feedbackRes, notificationRes] = await Promise.all([
      repairAPI.list(),
      feedbackAPI.list(),
      notificationAPI.list()
    ])
    
    pendingRepairs.value = repairRes.data.filter(r => r.status === 'pending')
    pendingCount.value = pendingRepairs.value.length
    feedbackCount.value = feedbackRes.data.filter(f => f.status === 'pending').length
    notifications.value = notificationRes.data
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const navigateTo = (path) => {
  router.push(path)
}
</script>