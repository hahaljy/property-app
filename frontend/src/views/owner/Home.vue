<template>
  <div class="min-h-screen bg-gray-100">
    <div class="bg-blue-500 text-white p-6">
      <h1 class="text-xl font-bold">掌上物业</h1>
      <p class="text-blue-100 mt-1">欢迎回家，{{ user?.username }}</p>
    </div>

    <div class="p-4">
      <div class="grid grid-cols-2 gap-4 mb-6">
        <div 
          @click="navigateTo('/owner/repair')"
          class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition"
        >
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-3">
            <span class="text-2xl">🔧</span>
          </div>
          <h3 class="font-medium text-gray-800">报失报修</h3>
          <p class="text-sm text-gray-500 mt-1">提交维修申请</p>
        </div>
        <div 
          @click="navigateTo('/owner/feedback')"
          class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition"
        >
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3">
            <span class="text-2xl">💬</span>
          </div>
          <h3 class="font-medium text-gray-800">问题反馈</h3>
          <p class="text-sm text-gray-500 mt-1">提交您的建议</p>
        </div>
        <div 
          @click="navigateTo('/owner/evaluation')"
          class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition"
        >
          <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mb-3">
            <span class="text-2xl">⭐</span>
          </div>
          <h3 class="font-medium text-gray-800">服务评价</h3>
          <p class="text-sm text-gray-500 mt-1">评价服务质量</p>
        </div>
        <div 
          @click="navigateTo('/owner/profile')"
          class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition"
        >
          <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-3">
            <span class="text-2xl">👤</span>
          </div>
          <h3 class="font-medium text-gray-800">个人中心</h3>
          <p class="text-sm text-gray-500 mt-1">管理个人信息</p>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm mb-6">
        <h3 class="font-medium text-gray-800 mb-4">我的报修记录</h3>
        <div v-if="repairs.length === 0" class="text-center text-gray-400 py-8">
          <span class="text-4xl block mb-2">📋</span>
          <p>暂无报修记录</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="repair in repairs.slice(0, 3)" 
            :key="repair.id"
            class="border border-gray-200 rounded-lg p-3"
          >
            <div class="flex justify-between items-start">
              <div>
                <h4 class="font-medium">{{ repair.title }}</h4>
                <p class="text-sm text-gray-500 mt-1">{{ repair.create_time }}</p>
              </div>
              <span :class="getStatusClass(repair.status)" class="px-2 py-1 rounded text-xs">
                {{ getStatusText(repair.status) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm">
        <h3 class="font-medium text-gray-800 mb-4">小区通知</h3>
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

      <div class="bg-white rounded-xl p-4 shadow-sm mt-4">
        <h3 class="font-medium text-gray-800 mb-4">失物招领</h3>
        <div v-if="lostItems.length === 0" class="text-center text-gray-400 py-8">
          <span class="text-4xl block mb-2">🔍</span>
          <p>暂无失物招领信息</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="item in lostItems.slice(0, 3)" 
            :key="item.id"
            class="border border-gray-200 rounded-lg p-3"
          >
            <div class="flex justify-between items-start">
              <div>
                <h4 class="font-medium">{{ item.title }}</h4>
                <p class="text-sm text-gray-500 mt-1">{{ item.description }}</p>
                <div class="flex items-center space-x-4 mt-2 text-xs text-gray-400">
                  <span>📍 {{ item.location }}</span>
                  <span>📞 {{ item.contact_phone }}</span>
                </div>
                <p class="text-xs text-gray-400 mt-2">{{ item.create_time }}</p>
              </div>
              <span :class="getLostItemStatusClass(item.status)" class="px-2 py-1 rounded text-xs">
                {{ getLostItemStatusText(item.status) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 flex justify-around">
      <button @click="navigateTo('/owner')" class="flex flex-col items-center text-blue-500">
        <span class="text-2xl">🏠</span>
        <span class="text-xs mt-1">首页</span>
      </button>
      <button @click="navigateTo('/owner/repair')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">🔧</span>
        <span class="text-xs mt-1">报修</span>
      </button>
      <button @click="navigateTo('/owner/feedback')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">💬</span>
        <span class="text-xs mt-1">反馈</span>
      </button>
      <button @click="navigateTo('/owner/profile')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">👤</span>
        <span class="text-xs mt-1">我的</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { repairAPI, notificationAPI, lostItemsAPI } from '../../api'
import store from '../../store'

const router = useRouter()
const user = ref(null)
const repairs = ref([])
const notifications = ref([])
const lostItems = ref([])

onMounted(() => {
  user.value = store.getUser()?.user
  loadData()
})

const loadData = async () => {
  try {
    const [repairRes, notificationRes, lostItemsRes] = await Promise.all([
      repairAPI.list(),
      notificationAPI.list(),
      lostItemsAPI.list()
    ])
    repairs.value = repairRes.data
    notifications.value = notificationRes.data
    lostItems.value = lostItemsRes.data
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const navigateTo = (path) => {
  router.push(path)
}

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-700',
    processing: 'bg-blue-100 text-blue-700',
    completed: 'bg-green-100 text-green-700'
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成'
  }
  return texts[status] || status
}

const getLostItemStatusClass = (status) => {
  return status === 'lost' 
    ? 'bg-yellow-100 text-yellow-700' 
    : 'bg-green-100 text-green-700'
}

const getLostItemStatusText = (status) => {
  return status === 'lost' ? '待认领' : '已找回'
}
</script>