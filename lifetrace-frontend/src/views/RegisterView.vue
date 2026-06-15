<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Lock, User } from '@element-plus/icons-vue'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const { register } = useAuth()

const form = reactive({
  nickname: '',
  account: '',
  password: '',
  confirm: '',
})

const errorMessage = ref('')

async function submitRegister() {
  errorMessage.value = ''

  const result = await register(form)

  if (!result.ok) {
    errorMessage.value = result.message
    return
  }

  router.replace('/health')
}
</script>

<template>
  <section class="register-view" aria-labelledby="register-title">
    <div class="register-brand">
      <span class="register-brand__mark">LT</span>
      <div>
        <p>LifeTrace</p>
        <h1 id="register-title">创建账号</h1>
      </div>
    </div>

    <form class="register-card" @submit.prevent="submitRegister">
      <label class="register-field">
        <span>昵称</span>
        <span class="register-field__control">
          <el-icon><User /></el-icon>
          <input
            v-model="form.nickname"
            autocomplete="nickname"
            maxlength="12"
            placeholder="例如：林小摊"
          >
        </span>
      </label>

      <label class="register-field">
        <span>账号</span>
        <span class="register-field__control">
          <el-icon><User /></el-icon>
          <input
            v-model="form.account"
            autocomplete="username"
            placeholder="请输入登录账号"
          >
        </span>
      </label>

      <label class="register-field">
        <span>密码</span>
        <span class="register-field__control">
          <el-icon><Lock /></el-icon>
          <input
            v-model="form.password"
            autocomplete="new-password"
            placeholder="至少 6 位"
            type="password"
          >
        </span>
      </label>

      <label class="register-field">
        <span>确认密码</span>
        <span class="register-field__control">
          <el-icon><Lock /></el-icon>
          <input
            v-model="form.confirm"
            autocomplete="new-password"
            placeholder="再输入一次密码"
            type="password"
          >
        </span>
      </label>

      <p v-if="errorMessage" class="register-message register-message--error" role="alert">
        {{ errorMessage }}
      </p>

      <button class="register-submit" type="submit">注册并进入</button>

      <p class="register-switch">
        已有账号？
        <RouterLink to="/login">去登录</RouterLink>
      </p>
    </form>
  </section>
</template>

<style scoped>
.register-view {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 18px;
  padding: 24px var(--page-padding) 34px;
  background:
    radial-gradient(circle at 18% 14%, rgba(125, 216, 255, 0.18) 0%, rgba(125, 216, 255, 0) 35%),
    linear-gradient(180deg, #f4fbff 0%, #ffffff 58%, #ffffff 100%);
}

.register-brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.register-brand__mark {
  display: grid;
  width: 54px;
  height: 54px;
  place-items: center;
  border-radius: 18px;
  background: linear-gradient(135deg, #79cdfd 0%, #2d73db 100%);
  color: #ffffff;
  box-shadow: 0 12px 24px rgba(45, 115, 219, 0.2);
  font-size: 1rem;
  font-weight: 900;
}

.register-brand p {
  margin: 0 0 5px;
  color: var(--primary);
  font-size: 0.8rem;
  font-weight: 900;
}

.register-brand h1 {
  margin: 0;
  color: var(--text-main);
  font-size: 1.9rem;
  line-height: 1.15;
  font-weight: 900;
}

.register-card {
  display: grid;
  gap: 12px;
  padding: 18px;
  border: 1px solid rgba(126, 165, 220, 0.18);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 16px 36px rgba(71, 119, 183, 0.12);
}

.register-field {
  display: grid;
  gap: 7px;
}

.register-field > span:first-child {
  color: var(--text-main);
  font-size: 0.76rem;
  font-weight: 900;
}

.register-field__control {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 46px;
  padding: 0 13px;
  border: 1px solid rgba(126, 165, 220, 0.2);
  border-radius: 15px;
  background: #f8fbff;
  color: var(--primary);
}

.register-field__control input {
  width: 100%;
  min-width: 0;
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--text-main);
  font-size: 0.86rem;
  font-weight: 700;
}

.register-field__control:focus-within {
  border-color: rgba(45, 115, 219, 0.45);
  box-shadow: 0 0 0 3px rgba(45, 115, 219, 0.08);
}

.register-message {
  margin: 0;
  color: #107348;
  font-size: 0.76rem;
  font-weight: 800;
  line-height: 1.45;
}

.register-message--error {
  color: #d93636;
}

.register-submit {
  min-height: 48px;
  border: 0;
  border-radius: 15px;
  background: linear-gradient(135deg, #6fbaff 0%, #2d73db 100%);
  color: #ffffff;
  box-shadow: 0 12px 24px rgba(45, 115, 219, 0.22);
  font-size: 0.9rem;
  font-weight: 900;
}

.register-switch {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.78rem;
  font-weight: 800;
  text-align: center;
}

.register-switch a {
  color: var(--primary);
  text-decoration: none;
}

@media (max-width: 380px) {
  .register-view {
    gap: 14px;
    padding-top: 18px;
  }

  .register-card {
    padding: 16px;
  }
}
</style>
