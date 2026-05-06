import axios from 'axios'
import store from '../store'

const API_BASE_URL = '/api'

const axiosInstance = axios.create({
  baseURL: API_BASE_URL
})

axiosInstance.interceptors.request.use(config => {
  const token = store.getToken()
  if (token) {
    config.headers.Authorization = token
  }
  return config
}, error => {
  return Promise.reject(error)
})

axiosInstance.interceptors.response.use(response => {
  return response
}, error => {
  if (error.response && error.response.status === 401) {
    store.removeUser()
    window.location.href = '/login'
  }
  return Promise.reject(error)
})

export const authAPI = {
  login(username, password) {
    return axiosInstance.post('/login', { username, password })
  },

  register(data) {
    return axiosInstance.post('/register', data)
  },

  getProfile() {
    return axiosInstance.get('/user/profile')
  },

  updateProfile(data) {
    return axiosInstance.put('/user/profile', data)
  },

  updatePassword(oldPassword, newPassword) {
    return axiosInstance.put('/user/password', { oldPassword, newPassword })
  }
}

export const repairAPI = {
  create(title, description) {
    return axiosInstance.post('/repairs', { title, description })
  },

  list() {
    return axiosInstance.get('/repairs')
  },

  updateStatus(id, status) {
    return axiosInstance.put(`/repairs/${id}`, { status })
  }
}

export const feedbackAPI = {
  create(content) {
    return axiosInstance.post('/feedbacks', { content })
  },

  list() {
    return axiosInstance.get('/feedbacks')
  },

  reply(id, reply, status = 'replied') {
    return axiosInstance.put(`/feedbacks/${id}`, { reply, status })
  }
}

export const evaluationAPI = {
  create(repairId, rating, comment) {
    return axiosInstance.post('/evaluations', { repair_id: repairId, rating, comment })
  }
}

export const lostItemsAPI = {
  create(data) {
    return axiosInstance.post('/lost_items', data)
  },

  list() {
    return axiosInstance.get('/lost_items')
  },

  updateStatus(id, status) {
    return axiosInstance.put(`/lost_items/${id}`, { status })
  }
}

export const notificationAPI = {
  create(title, content) {
    return axiosInstance.post('/notifications', { title, content })
  },

  list() {
    return axiosInstance.get('/notifications')
  }
}