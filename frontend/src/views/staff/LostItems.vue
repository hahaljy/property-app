<template>
  <div class="min-h-screen bg-gray-100 pb-24">
    <div class="bg-green-500 text-white p-6">
      <div class="flex items-center">
        <button @click="goBack" class="mr-4">
          <span class="text-xl">←</span>
        </button>
        <h1 class="text-xl font-bold">失物招领</h1>
      </div>
    </div>

    <div class="p-4">
      <div class="bg-white rounded-xl p-4 shadow-sm mb-4">
        <h3 class="font-medium text-gray-800 mb-4">发布失物信息</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">物品名称</label>
            <input 
              v-model="form.title"
              type="text" 
              placeholder="请输入物品名称"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">物品描述</label>
            <textarea 
              v-model="form.description"
              rows="3"
              placeholder="请描述物品特征..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition resize-none"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">发现地点</label>
            <input 
              v-model="form.location"
              type="text" 
              placeholder="请输入发现地点"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">联系电话</label>
            <input 
              v-model="form.contact_phone"
              type="tel" 
              placeholder="请输入联系电话"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <button 
            @click="submitLostItem"
            class="w-full bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition"
          >
            {{ submitting ? '发布中...' : '发布信息' }}
          </button>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm">
        <h3 class="font-medium text-gray-800 mb-4">失物招领列表</h3>
        <div v-if="lostItems.length === 0" class="text-center text-gray-400 py-8">
          <span class="text-4xl block mb-2">🔍</span>
          <p>暂无失物招领信息</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="item in lostItems" 
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
              <span :class="getStatusClass(item.status)" class="px-2 py-1 rounded text-xs">
                {{ getStatusText(item.status) }}
              </span>
            </div>
            <button 
              v-if="item.status === 'lost'"
              @click="updateStatus(item.id, 'found')"
              class="mt-3 w-full bg-green-500 text-white py-2 rounded-lg text-sm hover:bg-green-600 transition"
            >
              已找到失主
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
import { lostItemsAPI } from '../../api'

const router = useRouter()
const submitting = ref(false)
const lostItems = ref([])
const form = reactive({
  title: '',
  description: '',
  location: '',
  contact_phone: ''
})

onMounted(() => {
  loadLostItems()
})

const loadLostItems = async () => {
  try {
    const response = await lostItemsAPI.list()
    lostItems.value = response.data
  } catch (error) {
    console.error('加载失物招领信息失败:', error)
  }
}

const submitLostItem = async () => {
  if (!form.title) {
    alert('请输入物品名称')
    return
  }

  submitting.value = true
  try {
    await lostItemsAPI.create(form)
    alert('发布成功')
    form.title = ''
    form.description = ''
    form.location = ''
    form.contact_phone = ''
    await loadLostItems()
  } catch (error) {
    alert(error.response?.data?.error || '发布失败')
  } finally {
    submitting.value = false
  }
}

const updateStatus = async (id, status) => {
  try {
    await lostItemsAPI.updateStatus(id, status)
    await loadLostItems()
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
  return status === 'lost' 
    ? 'bg-yellow-100 text-yellow-700' 
    : 'bg-green-100 text-green-700'
}

const getStatusText = (status) => {
  return status === 'lost' ? '待认领' : '已找回'
}
</script>