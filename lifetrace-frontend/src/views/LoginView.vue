<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Lock, User } from '@element-plus/icons-vue'
import { useAuth } from '../composables/useAuth'

const route = useRoute()
const router = useRouter()
const { login } = useAuth()

const form = reactive({
  account: '',
  password: '',
})

const errorMessage = ref('')
const statusMessage = ref(route.query.loggedOut ? '已退出登录，下次出摊再回来。' : '')

function submitLogin() {
  errorMessage.value = ''
  statusMessage.value = ''

  const result = login(form)

  if (!result.ok) {
    errorMessage.value = result.message
    return
  }

  const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/health'
  router.replace(redirect)
}
</script>

<template>
  <section class="login-view" aria-labelledby="login-title">
    <div class="login-brand">
      <span class="login-brand__mark">LT</span>
      <div>
        <p>LifeTrace</p>
        <h1 id="login-title">欢迎回来</h1>
      </div>
    </div>

    <form class="login-card" @submit.prevent="submitLogin">
      <label class="login-field">
        <span>账号</span>
        <span class="login-field__control">
          <el-icon><User /></el-icon>
          <input
            v-model="form.account"
            autocomplete="username"
            placeholder="请输入账号或昵称"
          >
        </span>
      </label>

      <label class="login-field">
        <span>密码</span>
        <span class="login-field__control">
          <el-icon><Lock /></el-icon>
          <input
            v-model="form.password"
            autocomplete="current-password"
            placeholder="请输入密码"
            type="password"
          >
        </span>
      </label>

      <p v-if="errorMessage" class="login-message login-message--error" role="alert">
        {{ errorMessage }}
      </p>
      <p v-else-if="statusMessage" class="login-message" role="status">
        {{ statusMessage }}
      </p>

      <button class="login-submit" type="submit">登录</button>

      <p class="login-switch">
        还没有账号？
        <RouterLink to="/register">去注册</RouterLink>
      </p>
    </form>
  </section>
</template>

<style scoped>
.login-view {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 18px;
  padding: 28px var(--page-padding) 38px;
  background:
    radial-gradient(circle at 18% 14%, rgba(125, 216, 255, 0.18) 0%, rgba(125, 216, 255, 0) 35%),
    linear-gradient(180deg, #f4fbff 0%, #ffffff 58%, #ffffff 100%);
}

.login-brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.login-brand__mark {
  display: grid;
  width: 56px;
  height: 56px;
  place-items: center;
  border-radius: 18px;
  background: linear-gradient(135deg, #79cdfd 0%, #2d73db 100%);
  color: #ffffff;
  box-shadow: 0 12px 24px rgba(45, 115, 219, 0.2);
  font-size: 1.02rem;
  font-weight: 900;
}

.login-brand p {
  margin: 0 0 5px;
  color: var(--primary);
  font-size: 0.8rem;
  font-weight: 900;
}

.login-brand h1 {
  margin: 0;
  color: var(--text-main);
  font-size: 2rem;
  line-height: 1.15;
  font-weight: 900;
}

.login-card {
  display: grid;
  gap: 14px;
  padding: 18px;
  border: 1px solid rgba(126, 165, 220, 0.18);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 16px 36px rgba(71, 119, 183, 0.12);
}

.login-field {
  display: grid;
  gap: 8px;
}

.login-field > span:first-child {
  color: var(--text-main);
  font-size: 0.76rem;
  font-weight: 900;
}

.login-field__control {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  padding: 0 13px;
  border: 1px solid rgba(126, 165, 220, 0.2);
  border-radius: 15px;
  background: #f8fbff;
  color: var(--primary);
}

.login-field__control input {
  width: 100%;
  min-width: 0;
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--text-main);
  font-size: 0.86rem;
  font-weight: 700;
}

.login-field__control:focus-within {
  border-color: rgba(45, 115, 219, 0.45);
  box-shadow: 0 0 0 3px rgba(45, 115, 219, 0.08);
}

.login-message {
  margin: 0;
  color: #107348;
  font-size: 0.76rem;
  font-weight: 800;
  line-height: 1.45;
}

.login-message--error {
  color: #d93636;
}

.login-submit {
  min-height: 48px;
  border: 0;
  border-radius: 15px;
  background: linear-gradient(135deg, #6fbaff 0%, #2d73db 100%);
  color: #ffffff;
  box-shadow: 0 12px 24px rgba(45, 115, 219, 0.22);
  font-size: 0.9rem;
  font-weight: 900;
}

.login-switch {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.78rem;
  font-weight: 800;
  text-align: center;
}

.login-switch a {
  color: var(--primary);
  text-decoration: none;
}

@media (max-width: 380px) {
  .login-view {
    gap: 16px;
    padding-top: 22px;
  }

  .login-brand h1 {
    font-size: 1.78rem;
  }

  .login-card {
    padding: 16px;
  }
}
</style>
