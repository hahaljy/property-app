<template>
  <div class="min-h-screen bg-gray-100 pb-24">
    <div class="bg-blue-500 text-white p-6">
      <div class="flex items-center">
        <button @click="goBack" class="mr-4">
          <span class="text-xl">←</span>
        </button>
        <h1 class="text-xl font-bold">问题反馈</h1>
      </div>
    </div>

    <div class="p-4">
      <div class="bg-white rounded-xl p-4 shadow-sm mb-4">
        <h3 class="font-medium text-gray-800 mb-4">提交反馈</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">反馈内容</label>
            <textarea 
              v-model="form.content"
              rows="6"
              placeholder="请输入您的问题或建议..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition resize-none"
            ></textarea>
          </div>
          <button 
            @click="submitFeedback"
            class="w-full bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition"
          >
            {{ submitting ? '提交中...' : '提交反馈' }}
          </button>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm">
        <h3 class="font-medium text-gray-800 mb-4">我的反馈记录</h3>
        <div v-if="feedbacks.length === 0" class="text-center text-gray-400 py-8">
          <span class="text-4xl block mb-2">💬</span>
          <p>暂无反馈记录</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="feedback in feedbacks" 
            :key="feedback.id"
            class="border border-gray-200 rounded-lg p-3"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <p class="text-sm text-gray-700">{{ feedback.content }}</p>
                <p class="text-xs text-gray-400 mt-2">{{ feedback.create_time }}</p>
                <div v-if="feedback.reply" class="mt-3 p-3 bg-gray-50 rounded-lg">
                  <p class="text-xs text-gray-500">物业回复:</p>
                  <p class="text-sm text-blue-600 mt-1">{{ feedback.reply }}</p>
                </div>
              </div>
              <span :class="getStatusClass(feedback.status)" class="px-2 py-1 rounded text-xs">
                {{ getStatusText(feedback.status) }}
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
      <button @click="navigateTo('/owner/repair')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">🔧</span>
        <span class="text-xs mt-1">报修</span>
      </button>
      <button @click="navigateTo('/owner/feedback')" class="flex flex-col items-center text-blue-500">
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
import { feedbackAPI } from '../../api'

const router = useRouter()
const submitting = ref(false)
const feedbacks = ref([])
const form = reactive({
  content: ''
})

onMounted(() => {
  loadFeedbacks()
})

const loadFeedbacks = async () => {
  try {
    const response = await feedbackAPI.list()
    feedbacks.value = response.data
  } catch (error) {
    console.error('加载反馈记录失败:', error)
  }
}

const submitFeedback = async () => {
  if (!form.content.trim()) {
    alert('请输入反馈内容')
    return
  }

  submitting.value = true
  try {
    await feedbackAPI.create(form.content)
    alert('反馈提交成功')
    form.content = ''
    await loadFeedbacks()
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
    replied: 'bg-blue-100 text-blue-700',
    resolved: 'bg-green-100 text-green-700'
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待处理',
    replied: '已回复',
    resolved: '已解决'
  }
  return texts[status] || status
}
</script>