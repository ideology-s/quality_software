import { computed, ref } from 'vue'

const AUTH_KEY = 'lifetrace-authenticated'
const USER_KEY = 'lifetrace-user'

const savedUser = JSON.parse(window.localStorage.getItem(USER_KEY) || 'null')
const isLoggedIn = ref(window.localStorage.getItem(AUTH_KEY) === 'true')
const currentUser = ref(savedUser || {
  nickname: '林小摊',
  account: 'student',
  avatarUrl: '',
})

function saveUser(user) {
  currentUser.value = {
    ...currentUser.value,
    ...user,
  }
  window.localStorage.setItem(USER_KEY, JSON.stringify(currentUser.value))
}

export function useAuth() {
  const isAuthenticated = computed(() => isLoggedIn.value)

  function login({ account, password }) {
    const cleanAccount = account.trim()

    if (!cleanAccount || !password) {
      return { ok: false, message: '请输入账号和密码' }
    }

    if (currentUser.value.account !== cleanAccount) {
      saveUser({
        nickname: cleanAccount.length > 8 ? cleanAccount.slice(0, 8) : cleanAccount,
        account: cleanAccount,
        avatarUrl: '',
      })
    }

    isLoggedIn.value = true
    window.localStorage.setItem(AUTH_KEY, 'true')

    return { ok: true }
  }

  function register({ nickname, account, password, confirm }) {
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

    saveUser({
      nickname: cleanNickname,
      account: cleanAccount,
      avatarUrl: '',
    })
    isLoggedIn.value = true
    window.localStorage.setItem(AUTH_KEY, 'true')

    return { ok: true }
  }

  function updateProfile(profile) {
    const cleanNickname = profile.nickname.trim()
    const cleanAccount = profile.account.trim()

    if (!cleanNickname || !cleanAccount) {
      return { ok: false, message: '昵称和账号不能为空' }
    }

    saveUser({
      nickname: cleanNickname,
      account: cleanAccount,
      avatarUrl: profile.avatarUrl || '',
    })

    return { ok: true }
  }

  function logout() {
    isLoggedIn.value = false
    window.localStorage.removeItem(AUTH_KEY)
  }

  return {
    currentUser,
    isAuthenticated,
    login,
    logout,
    register,
    updateProfile,
  }
}
