<template>
  <div class="min-h-screen bg-gray-100 pb-24">
    <div class="bg-blue-500 text-white p-6">
      <div class="flex items-center">
        <button @click="goBack" class="mr-4">
          <span class="text-xl">←</span>
        </button>
        <h1 class="text-xl font-bold">个人中心</h1>
      </div>
    </div>

    <div class="p-4">
      <div class="bg-white rounded-xl p-4 shadow-sm mb-4">
        <div class="flex items-center">
          <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center">
            <span class="text-3xl">👤</span>
          </div>
          <div class="ml-4">
            <h3 class="font-medium text-gray-800">{{ user?.username }}</h3>
            <p class="text-sm text-gray-500">业主</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm mb-4">
        <h3 class="font-medium text-gray-800 mb-4">基本信息</h3>
        <div class="space-y-3">
          <div class="flex justify-between items-center py-2 border-b border-gray-100">
            <span class="text-gray-500">用户名</span>
            <span class="text-gray-800">{{ user?.username }}</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-gray-100">
            <span class="text-gray-500">手机号</span>
            <span class="text-gray-800">{{ user?.phone || '未设置' }}</span>
          </div>
          <div class="flex justify-between items-center py-2">
            <span class="text-gray-500">住址</span>
            <span class="text-gray-800">{{ user?.address || '未设置' }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm mb-4 overflow-hidden">
        <button 
          @click="showChangePassword = true"
          class="w-full p-4 flex justify-between items-center hover:bg-gray-50 transition"
        >
          <span class="flex items-center">
            <span class="mr-3 text-lg">🔑</span>
            <span class="text-gray-800">修改密码</span>
          </span>
          <span class="text-gray-400">→</span>
        </button>
        <button 
          @click="showEditProfile = true"
          class="w-full p-4 flex justify-between items-center hover:bg-gray-50 transition border-t border-gray-100"
        >
          <span class="flex items-center">
            <span class="mr-3 text-lg">✏️</span>
            <span class="text-gray-800">编辑资料</span>
          </span>
          <span class="text-gray-400">→</span>
        </button>
      </div>

      <button 
        @click="handleLogout"
        class="w-full bg-red-500 text-white py-3 rounded-lg font-medium hover:bg-red-600 transition"
      >
        退出登录
      </button>
    </div>

    <div v-if="showChangePassword" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-sm">
        <h3 class="font-medium text-gray-800 mb-4">修改密码</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">原密码</label>
            <input 
              v-model="passwordForm.oldPassword"
              type="password" 
              placeholder="请输入原密码"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">新密码</label>
            <input 
              v-model="passwordForm.newPassword"
              type="password" 
              placeholder="请输入新密码"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">确认新密码</label>
            <input 
              v-model="passwordForm.confirmPassword"
              type="password" 
              placeholder="请再次输入新密码"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div class="flex space-x-3">
            <button 
              @click="showChangePassword = false"
              class="flex-1 border border-gray-300 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-50 transition"
            >
              取消
            </button>
            <button 
              @click="changePassword"
              class="flex-1 bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition"
            >
              {{ passwordLoading ? '修改中...' : '确认修改' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showEditProfile" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-sm">
        <h3 class="font-medium text-gray-800 mb-4">编辑资料</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">手机号</label>
            <input 
              v-model="profileForm.phone"
              type="tel" 
              placeholder="请输入手机号"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">住址</label>
            <input 
              v-model="profileForm.address"
              type="text" 
              placeholder="请输入住址"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div class="flex space-x-3">
            <button 
              @click="showEditProfile = false"
              class="flex-1 border border-gray-300 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-50 transition"
            >
              取消
            </button>
            <button 
              @click="editProfile"
              class="flex-1 bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition"
            >
              {{ profileLoading ? '修改中...' : '确认修改' }}
            </button>
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
      <button @click="navigateTo('/owner/profile')" class="flex flex-col items-center text-blue-500">
        <span class="text-2xl">👤</span>
        <span class="text-xs mt-1">我的</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../../api'
import store from '../../store'

const router = useRouter()
const user = ref(null)
const showChangePassword = ref(false)
const showEditProfile = ref(false)
const passwordLoading = ref(false)
const profileLoading = ref(false)

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const profileForm = reactive({
  phone: '',
  address: ''
})

onMounted(() => {
  user.value = store.getUser()?.user
  profileForm.phone = user.value?.phone || ''
  profileForm.address = user.value?.address || ''
})

const changePassword = async () => {
  if (!passwordForm.oldPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
    alert('请填写所有字段')
    return
  }

  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    alert('两次密码不一致')
    return
  }

  passwordLoading.value = true
  try {
    await authAPI.updatePassword(passwordForm.oldPassword, passwordForm.newPassword)
    alert('密码修改成功')
    showChangePassword.value = false
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (error) {
    alert(error.response?.data?.error || '修改失败')
  } finally {
    passwordLoading.value = false
  }
}

const editProfile = async () => {
  profileLoading.value = true
  try {
    await authAPI.updateProfile(profileForm)
    alert('资料修改成功')
    showEditProfile.value = false
    const currentUser = store.getUser()
    currentUser.user.phone = profileForm.phone
    currentUser.user.address = profileForm.address
    store.setUser(currentUser)
    user.value = currentUser.user
  } catch (error) {
    alert(error.response?.data?.error || '修改失败')
  } finally {
    profileLoading.value = false
  }
}

const handleLogout = () => {
  if (confirm('确定要退出登录吗?')) {
    store.removeUser()
    router.push('/login')
  }
}

const goBack = () => {
  router.back()
}

const navigateTo = (path) => {
  router.push(path)
}
</script>