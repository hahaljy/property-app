<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <span class="text-white text-3xl">🏠</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-800">掌上物业</h1>
        <p class="text-gray-500 mt-2">注册新账号</p>
      </div>

      <div class="bg-white rounded-2xl shadow-lg p-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
            <input 
              v-model="form.username"
              type="text" 
              placeholder="请输入用户名"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
            <input 
              v-model="form.password"
              type="password" 
              placeholder="请输入密码"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">确认密码</label>
            <input 
              v-model="confirmPassword"
              type="password" 
              placeholder="请再次输入密码"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">手机号</label>
            <input 
              v-model="form.phone"
              type="tel" 
              placeholder="请输入手机号"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">身份选择</label>
            <div class="flex space-x-4">
              <label class="flex items-center">
                <input 
                  type="radio" 
                  v-model="form.role" 
                  value="owner"
                  class="w-4 h-4 text-blue-500 border-gray-300 focus:ring-blue-500"
                />
                <span class="ml-2">业主</span>
              </label>
              <label class="flex items-center">
                <input 
                  type="radio" 
                  v-model="form.role" 
                  value="staff"
                  class="w-4 h-4 text-blue-500 border-gray-300 focus:ring-blue-500"
                />
                <span class="ml-2">物业人员</span>
              </label>
            </div>
          </div>
          <div v-if="form.role === 'owner'">
            <label class="block text-sm font-medium text-gray-700 mb-2">住址</label>
            <input 
              v-model="form.address"
              type="text" 
              placeholder="请输入住址（如：XX小区X栋X单元XXX室）"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div v-if="form.role === 'staff'">
            <label class="block text-sm font-medium text-gray-700 mb-2">保密密码</label>
            <input 
              v-model="secretPassword"
              type="password" 
              placeholder="请输入物业人员保密密码"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            />
          </div>
          <div v-if="form.role === 'staff'">
            <label class="block text-sm font-medium text-gray-700 mb-2">负责业务</label>
            <select 
              v-model="form.department"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            >
              <option value="">请选择负责业务</option>
              <option value="维修">维修</option>
              <option value="园林">园林</option>
              <option value="保洁">保洁</option>
              <option value="安保">安保</option>
              <option value="客服">客服</option>
            </select>
          </div>
        </div>

        <button 
          @click="handleRegister"
          class="w-full mt-6 bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition flex items-center justify-center"
        >
          <span v-if="loading" class="animate-spin mr-2">⏳</span>
          {{ loading ? '注册中...' : '注 册' }}
        </button>

        <p class="text-center mt-6 text-gray-500">
          已有账号? 
          <router-link to="/login" class="text-blue-500 hover:text-blue-600">立即登录</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api'

const router = useRouter()
const loading = ref(false)
const confirmPassword = ref('')
const secretPassword = ref('')
const form = reactive({
  username: '',
  password: '',
  phone: '',
  role: 'owner',
  address: '',
  department: ''
})

const STAFF_SECRET_PASSWORD = '2023082024'

const handleRegister = async () => {
  if (!form.username) {
    alert('请填写用户名')
    return
  }

  if (!form.password) {
    alert('请填写密码')
    return
  }

  if (form.password.length < 6) {
    alert('密码长度不能少于6位')
    return
  }

  if (form.password !== confirmPassword.value) {
    alert('两次密码不一致')
    return
  }

  if (!form.phone) {
    alert('请填写手机号')
    return
  }

  if (!/^1[3-9]\d{9}$/.test(form.phone)) {
    alert('请输入有效的11位手机号')
    return
  }

  if (!form.role) {
    alert('请选择身份')
    return
  }

  if (form.role === 'owner' && !form.address) {
    alert('请填写住址')
    return
  }

  if (form.role === 'staff') {
    if (!secretPassword.value) {
      alert('请输入物业人员保密密码')
      return
    }
    if (secretPassword.value !== STAFF_SECRET_PASSWORD) {
      alert('保密密码错误，无法注册为物业人员')
      return
    }
    if (!form.department) {
      alert('请选择负责业务')
      return
    }
  }

  loading.value = true
  try {
    await authAPI.register(form)
    alert('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    alert(error.response?.data?.error || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>