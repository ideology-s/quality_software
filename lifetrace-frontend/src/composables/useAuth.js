import { computed, ref } from 'vue'
import { login as apiLogin, register as apiRegister } from '../api'

const TOKEN_KEY = 'lifetrace-token'
const USER_KEY = 'lifetrace-user'

const savedUser = JSON.parse(window.localStorage.getItem(USER_KEY) || 'null')
const savedToken = window.localStorage.getItem(TOKEN_KEY)
const isLoggedIn = ref(!!savedToken)
const currentUser = ref(savedUser || {
  nickname: '',
  account: '',
  avatarUrl: '',
})

function saveToken(token) {
  if (token) {
    window.localStorage.setItem(TOKEN_KEY, token)
  } else {
    window.localStorage.removeItem(TOKEN_KEY)
  }
}

function saveUser(user) {
  currentUser.value = { ...currentUser.value, ...user }
  window.localStorage.setItem(USER_KEY, JSON.stringify(currentUser.value))
}

export function useAuth() {
  const isAuthenticated = computed(() => isLoggedIn.value)

  async function login({ account, password }) {
    const cleanAccount = account.trim()
    if (!cleanAccount || !password) {
      return { ok: false, message: '请输入账号和密码' }
    }

    try {
      const res = await apiLogin({ username: cleanAccount, password })
      const data = res.data.data
      saveToken(data.token)
      saveUser({ nickname: data.username, account: cleanAccount, avatarUrl: '' })
      isLoggedIn.value = true
      return { ok: true }
    } catch (e) {
      const msg = e.response?.data?.message || '登录失败，请检查后端服务'
      return { ok: false, message: msg }
    }
  }

  async function register({ nickname, account, password, confirm }) {
    const cleanNickname = nickname.trim()
    const cleanAccount = account.trim()

    if (!cleanNickname || !cleanAccount || !password || !confirm) {
      return { ok: false, message: '请完整填写注册信息' }
    }
    if (password.length < 6) {
      return { ok: false, message: '密码至少需要 6 位' }
    }
    if (password !== confirm) {
      return { ok: false, message: '两次输入的密码不一致' }
    }

    try {
      const res = await apiRegister({ username: cleanAccount, password })
      const data = res.data.data
      saveToken(data.token)
      saveUser({ nickname: cleanNickname, account: cleanAccount, avatarUrl: '' })
      isLoggedIn.value = true
      return { ok: true }
    } catch (e) {
      const msg = e.response?.data?.message || '注册失败，请检查后端服务'
      return { ok: false, message: msg }
    }
  }

  function updateProfile(profile) {
    const cleanNickname = profile.nickname.trim()
    const cleanAccount = profile.account.trim()
    if (!cleanNickname || !cleanAccount) {
      return { ok: false, message: '昵称和账号不能为空' }
    }
    saveUser({ nickname: cleanNickname, account: cleanAccount, avatarUrl: profile.avatarUrl || '' })
    return { ok: true }
  }

  function logout() {
    isLoggedIn.value = false
    saveToken(null)
    window.localStorage.removeItem(USER_KEY)
    window.location.href = '/login'
  }

  return { currentUser, isAuthenticated, login, logout, register, updateProfile }
}
