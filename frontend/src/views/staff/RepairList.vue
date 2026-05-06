<template>
  <div class="min-h-screen bg-gray-100 pb-24">
    <div class="bg-green-500 text-white p-6">
      <div class="flex items-center">
        <button @click="goBack" class="mr-4">
          <span class="text-xl">←</span>
        </button>
        <h1 class="text-xl font-bold">维修记录</h1>
      </div>
    </div>

    <div class="p-4">
      <div class="flex space-x-2 mb-4">
        <button 
          v-for="tab in tabs" 
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition',
            activeTab === tab.value 
              ? 'bg-green-500 text-white' 
              : 'bg-white text-gray-600 hover:bg-gray-50'
          ]"
        >
          {{ tab.label }}
        </button>
      </div>

      <div v-if="filteredRepairs.length === 0" class="text-center text-gray-400 py-8">
        <span class="text-4xl block mb-2">📋</span>
        <p>暂无{{ tabs.find(t => t.value === activeTab)?.label }}记录</p>
      </div>

      <div v-else class="space-y-3">
        <div 
          v-for="repair in filteredRepairs" 
          :key="repair.id"
          class="bg-white rounded-xl p-4 shadow-sm"
        >
          <div class="flex justify-between items-start mb-2">
            <h4 class="font-medium text-gray-800">{{ repair.title }}</h4>
            <span :class="getStatusClass(repair.status)" class="px-2 py-1 rounded text-xs">
              {{ getStatusText(repair.status) }}
            </span>
          </div>
          <p class="text-sm text-gray-500 mb-2">{{ repair.description }}</p>
          <p class="text-xs text-gray-400 mb-3">{{ repair.create_time }}</p>
          
          <div v-if="repair.status !== 'completed'" class="flex space-x-2">
            <button 
              v-if="repair.status === 'pending'"
              @click="updateStatus(repair.id, 'processing')"
              class="flex-1 bg-blue-500 text-white py-2 rounded-lg text-sm hover:bg-blue-600 transition"
            >
              开始处理
            </button>
            <button 
              v-if="repair.status === 'processing'"
              @click="updateStatus(repair.id, 'completed')"
              class="flex-1 bg-green-500 text-white py-2 rounded-lg text-sm hover:bg-green-600 transition"
            >
              完成维修
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 flex justify-around">
      <button @click="navigateTo('/staff')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">🏠</span>
        <span class="text-xs mt-1">首页</span>
      </button>
      <button @click="navigateTo('/staff/repair-list')" class="flex flex-col items-center text-green-500">
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { repairAPI } from '../../api'

const router = useRouter()
const repairs = ref([])
const activeTab = ref('all')

const tabs = [
  { label: '全部', value: 'all' },
  { label: '待处理', value: 'pending' },
  { label: '处理中', value: 'processing' },
  { label: '已完成', value: 'completed' }
]

const filteredRepairs = computed(() => {
  if (activeTab.value === 'all') {
    return repairs.value
  }
  return repairs.value.filter(r => r.status === activeTab.value)
})

onMounted(() => {
  loadRepairs()
})

const loadRepairs = async () => {
  try {
    const response = await repairAPI.list()
    repairs.value = response.data
  } catch (error) {
    console.error('加载维修记录失败:', error)
  }
}

const updateStatus = async (id, status) => {
  try {
    await repairAPI.updateStatus(id, status)
    await loadRepairs()
    alert('状态更新成功')
  } catch (error) {
    alert(error.response?.data?.error || '更新失败')
  }
}

const goBack = () => {
  router.back()
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
</script>