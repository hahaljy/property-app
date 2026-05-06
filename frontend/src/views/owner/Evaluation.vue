<template>
  <div class="min-h-screen bg-gray-100 pb-24">
    <div class="bg-blue-500 text-white p-6">
      <div class="flex items-center">
        <button @click="goBack" class="mr-4">
          <span class="text-xl">←</span>
        </button>
        <h1 class="text-xl font-bold">服务评价</h1>
      </div>
    </div>

    <div class="p-4">
      <div v-if="showForm" class="bg-white rounded-xl p-4 shadow-sm mb-4">
        <h3 class="font-medium text-gray-800 mb-4">评价服务</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">选择评分</label>
            <div class="flex items-center space-x-2">
              <button 
                v-for="star in 5" 
                :key="star"
                @click="form.rating = star"
                class="text-3xl transition"
              >
                {{ star <= form.rating ? '★' : '☆' }}
              </button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">评价内容</label>
            <textarea 
              v-model="form.comment"
              rows="4"
              placeholder="请输入您的评价..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition resize-none"
            ></textarea>
          </div>
          <div class="flex space-x-3">
            <button 
              @click="cancelEvaluation"
              class="flex-1 border border-gray-300 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-50 transition"
            >
              取消
            </button>
            <button 
              @click="submitEvaluation"
              class="flex-1 bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition"
            >
              {{ submitting ? '提交中...' : '提交评价' }}
            </button>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm">
        <h3 class="font-medium text-gray-800 mb-4">可评价的报修</h3>
        <div v-if="completedRepairs.length === 0" class="text-center text-gray-400 py-8">
          <span class="text-4xl block mb-2">⭐</span>
          <p>暂无已完成的报修记录</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="repair in completedRepairs" 
            :key="repair.id"
            class="border border-gray-200 rounded-lg p-3"
          >
            <div class="flex justify-between items-center">
              <div>
                <h4 class="font-medium">{{ repair.title }}</h4>
                <p class="text-sm text-gray-500 mt-1">{{ repair.create_time }}</p>
              </div>
              <button 
                @click="startEvaluation(repair)"
                class="bg-yellow-500 text-white px-3 py-1 rounded text-sm hover:bg-yellow-600 transition"
              >
                评价
              </button>
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { repairAPI, evaluationAPI } from '../../api'

const router = useRouter()
const submitting = ref(false)
const showForm = ref(false)
const currentRepair = ref(null)
const completedRepairs = ref([])
const form = reactive({
  rating: 5,
  comment: ''
})

onMounted(() => {
  loadCompletedRepairs()
})

const loadCompletedRepairs = async () => {
  try {
    const response = await repairAPI.list()
    completedRepairs.value = response.data.filter(r => r.status === 'completed')
  } catch (error) {
    console.error('加载报修记录失败:', error)
  }
}

const startEvaluation = (repair) => {
  currentRepair.value = repair
  showForm.value = true
}

const cancelEvaluation = () => {
  showForm.value = false
  currentRepair.value = null
  form.rating = 5
  form.comment = ''
}

const submitEvaluation = async () => {
  if (!currentRepair.value) return

  submitting.value = true
  try {
    await evaluationAPI.create(currentRepair.value.id, form.rating, form.comment)
    alert('评价成功')
    cancelEvaluation()
    await loadCompletedRepairs()
  } catch (error) {
    alert(error.response?.data?.error || '评价失败')
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
</script>