<template>
  <div class="min-h-screen bg-gray-100 pb-24">
    <div class="bg-green-500 text-white p-6">
      <div class="flex items-center">
        <button @click="goBack" class="mr-4">
          <span class="text-xl">←</span>
        </button>
        <h1 class="text-xl font-bold">问题反馈</h1>
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

      <div v-if="filteredFeedbacks.length === 0" class="text-center text-gray-400 py-8">
        <span class="text-4xl block mb-2">💬</span>
        <p>暂无{{ tabs.find(t => t.value === activeTab)?.label }}反馈</p>
      </div>

      <div v-else class="space-y-3">
        <div 
          v-for="feedback in filteredFeedbacks" 
          :key="feedback.id"
          class="bg-white rounded-xl p-4 shadow-sm"
        >
          <div class="flex justify-between items-start mb-2">
            <h4 class="font-medium text-gray-800">反馈 #{{ feedback.id }}</h4>
            <span :class="getStatusClass(feedback.status)" class="px-2 py-1 rounded text-xs">
              {{ getStatusText(feedback.status) }}
            </span>
          </div>
          <p class="text-sm text-gray-500 mb-2">{{ feedback.content }}</p>
          <p class="text-xs text-gray-400 mb-3">{{ feedback.create_time }}</p>
          
          <div v-if="feedback.reply" class="p-3 bg-blue-50 rounded-lg mb-3">
            <p class="text-xs text-blue-600">物业回复:</p>
            <p class="text-sm text-gray-700 mt-1">{{ feedback.reply }}</p>
          </div>

          <div v-if="feedback.status !== 'resolved'" class="mt-3">
            <textarea 
              v-if="showReplyForm === feedback.id"
              v-model="replyContent"
              rows="3"
              placeholder="请输入回复内容..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition resize-none mb-3"
            ></textarea>
            <div v-if="showReplyForm === feedback.id" class="flex space-x-2">
              <button 
                @click="showReplyForm = null; replyContent = ''"
                class="flex-1 border border-gray-300 text-gray-700 py-2 rounded-lg text-sm hover:bg-gray-50 transition"
              >
                取消
              </button>
              <button 
                @click="submitReply(feedback.id)"
                class="flex-1 bg-blue-500 text-white py-2 rounded-lg text-sm hover:bg-blue-600 transition"
              >
                发送回复
              </button>
            </div>
            <button 
              v-else
              @click="showReplyForm = feedback.id"
              class="w-full border border-blue-500 text-blue-500 py-2 rounded-lg text-sm hover:bg-blue-50 transition"
            >
              回复反馈
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
      <button @click="navigateTo('/staff/repair-list')" class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">🔧</span>
        <span class="text-xs mt-1">维修</span>
      </button>
      <button @click="navigateTo('/staff/feedback-list')" class="flex flex-col items-center text-green-500">
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
import { feedbackAPI } from '../../api'

const router = useRouter()
const feedbacks = ref([])
const activeTab = ref('all')
const showReplyForm = ref(null)
const replyContent = ref('')

const tabs = [
  { label: '全部', value: 'all' },
  { label: '待处理', value: 'pending' },
  { label: '已回复', value: 'replied' },
  { label: '已解决', value: 'resolved' }
]

const filteredFeedbacks = computed(() => {
  if (activeTab.value === 'all') {
    return feedbacks.value
  }
  return feedbacks.value.filter(f => f.status === activeTab.value)
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

const submitReply = async (id) => {
  if (!replyContent.value.trim()) {
    alert('请输入回复内容')
    return
  }

  try {
    await feedbackAPI.reply(id, replyContent.value)
    showReplyForm.value = null
    replyContent.value = ''
    await loadFeedbacks()
    alert('回复成功')
  } catch (error) {
    alert(error.response?.data?.error || '回复失败')
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