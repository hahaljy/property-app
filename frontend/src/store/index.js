const STORAGE_KEY = 'property_user'

const store = {
  getUser() {
    try {
      const data = localStorage.getItem(STORAGE_KEY)
      return data ? JSON.parse(data) : null
    } catch {
      return null
    }
  },

  setUser(user) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(user))
  },

  removeUser() {
    localStorage.removeItem(STORAGE_KEY)
  },

  getToken() {
    const user = this.getUser()
    return user ? user.token : null
  }
}

export default store