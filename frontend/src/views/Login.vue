<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <span class="text-white text-3xl">🏠</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-800">掌上物业</h1>
        <p class="text-gray-500 mt-2">连接业主与物业的桥梁</p>
      </div>

      <div class="bg-white rounded-2xl shadow-lg p-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
            <input 
              v-model="username"
              type="text" 
              placeholder="请输入用户名"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
            <input 
              v-model="password"
              type="password" 
              placeholder="请输入密码"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div class="flex items-center justify-between">
            <label class="flex items-center">
              <input type="checkbox" class="w-4 h-4 text-blue-500 border-gray-300 rounded focus:ring-blue-500" />
              <span class="ml-2 text-sm text-gray-600">记住我</span>
            </label>
            <a href="#" class="text-sm text-blue-500 hover:text-blue-600">忘记密码?</a>
          </div>
        </div>

        <button 
          @click="handleLogin"
          class="w-full mt-6 bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition flex items-center justify-center"
        >
          <span v-if="loading" class="animate-spin mr-2">⏳</span>
          {{ loading ? '登录中...' : '登 录' }}
        </button>

        <p class="text-center mt-6 text-gray-500">
          还没有账号? 
          <router-link to="/register" class="text-blue-500 hover:text-blue-600">立即注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api'
import store from '../store'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)

const handleLogin = async () => {
  if (!username.value || !password.value) {
    alert('请填写用户名和密码')
    return
  }

  loading.value = true
  try {
    const response = await authAPI.login(username.value, password.value)
    const { token, user } = response.data
    store.setUser({ token, user })
    
    if (user.role === 'owner') {
      router.push('/owner')
    } else {
      router.push('/staff')
    }
  } catch (error) {
    alert(error.response?.data?.error || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>