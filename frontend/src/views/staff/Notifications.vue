<template>
  <div class="min-h-screen bg-gray-100 pb-24">
    <div class="bg-green-500 text-white p-6">
      <div class="flex items-center">
        <button @click="goBack" class="mr-4">
          <span class="text-xl">←</span>
        </button>
        <h1 class="text-xl font-bold">通知广播</h1>
      </div>
    </div>

    <div class="p-4">
      <div class="bg-white rounded-xl p-4 shadow-sm mb-4">
        <h3 class="font-medium text-gray-800 mb-4">发布通知</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">通知标题</label>
            <input 
              v-model="form.title"
              type="text" 
              placeholder="请输入通知标题"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">通知内容</label>
            <textarea 
              v-model="form.content"
              rows="4"
              placeholder="请输入通知内容..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition resize-none"
            ></textarea>
          </div>
          <button 
            @click="submitNotification"
            class="w-full bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition"
          >
            {{ submitting ? '发布中...' : '发布通知' }}
          </button>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm">
        <h3 class="font-medium text-gray-800 mb-4">通知列表</h3>
        <div v-if="notifications.length === 0" class="text-center text-gray-400 py-8">
          <span class="text-4xl block mb-2">📢</span>
          <p>暂无通知</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="notification in notifications" 
            :key="notification.id"
            class="border border-gray-200 rounded-lg p-3"
          >
            <h4 class="font-medium">{{ notification.title }}</h4>
            <p class="text-sm text-gray-500 mt-1">{{ notification.content }}</p>
            <p class="text-xs text-gray-400 mt-2">{{ notification.create_time }}</p>
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { notificationAPI } from '../../api'

const router = useRouter()
const submitting = ref(false)
const notifications = ref([])
const form = reactive({
  title: '',
  content: ''
})

onMounted(() => {
  loadNotifications()
})

const loadNotifications = async () => {
  try {
    const response = await notificationAPI.list()
    notifications.value = response.data
  } catch (error) {
    console.error('加载通知失败:', error)
  }
}

const submitNotification = async () => {
  if (!form.title || !form.content) {
    alert('请填写标题和内容')
    return
  }

  submitting.value = true
  try {
    await notificationAPI.create(form.title, form.content)
    alert('通知发布成功')
    form.title = ''
    form.content = ''
    await loadNotifications()
  } catch (error) {
    alert(error.response?.data?.error || '发布失败')
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