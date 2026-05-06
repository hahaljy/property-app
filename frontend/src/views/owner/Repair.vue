<template>
  <div class="min-h-screen bg-gray-100 pb-24">
    <div class="bg-blue-500 text-white p-6">
      <div class="flex items-center">
        <button @click="goBack" class="mr-4">
          <span class="text-xl">←</span>
        </button>
        <h1 class="text-xl font-bold">报失报修</h1>
      </div>
    </div>

    <div class="p-4">
      <div class="bg-white rounded-xl p-4 shadow-sm mb-4">
        <h3 class="font-medium text-gray-800 mb-4">提交报修</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">报修标题</label>
            <input 
              v-model="form.title"
              type="text" 
              placeholder="请输入报修标题"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">详细描述</label>
            <textarea 
              v-model="form.description"
              rows="4"
              placeholder="请详细描述问题..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition resize-none"
            ></textarea>
          </div>
          <button 
            @click="submitRepair"
            class="w-full bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition"
          >
            {{ submitting ? '提交中...' : '提交报修' }}
          </button>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm">
        <h3 class="font-medium text-gray-800 mb-4">我的报修记录</h3>
        <div v-if="repairs.length === 0" class="text-center text-gray-400 py-8">
          <span class="text-4xl block mb-2">📋</span>
          <p>暂无报修记录</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="repair in repairs" 
            :key="repair.id"
            class="border border-gray-200 rounded-lg p-3"
          >
            <div class="flex justify-between items-start">
              <div>
                <h4 class="font-medium">{{ repair.title }}</h4>
                <p class="text-sm text-gray-500 mt-1">{{ repair.description }}</p>
                <p class="text-xs text-gray-400 mt-2">{{ repair.create_time }}</p>
              </div>
              <span :class="getStatusClass(repair.status)" class="px-2 py-1 rounded text-xs">
                {{ getStatusText(repair.status) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 flex justify-around">
      <button @click="navigateTo('/owner')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">🏠</span>
        <span class="text-xs mt-1">首页</span>
      </button>
      <button @click="navigateTo('/owner/repair')" class="flex flex-col items-center text-blue-500">
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { repairAPI } from '../../api'

const router = useRouter()
const submitting = ref(false)
const repairs = ref([])
const form = reactive({
  title: '',
  description: ''
})

onMounted(() => {
  loadRepairs()
})

const loadRepairs = async () => {
  try {
    const response = await repairAPI.list()
    repairs.value = response.data
  } catch (error) {
    console.error('加载报修记录失败:', error)
  }
}

const submitRepair = async () => {
  if (!form.title) {
    alert('请输入报修标题')
    return
  }

  submitting.value = true
  try {
    await repairAPI.create(form.title, form.description)
    alert('报修提交成功')
    form.title = ''
    form.description = ''
    await loadRepairs()
  } catch (error) {
    alert(error.response?.data?.error || '提交失败')
  } finally {
    submitting.value = false
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