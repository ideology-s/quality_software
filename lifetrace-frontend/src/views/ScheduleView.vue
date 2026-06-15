<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Lock, Plus, SwitchButton } from '@element-plus/icons-vue'
import { useAuth } from '../composables/useAuth'
import { usePageNotice } from '../composables/usePageNotice'
import { getSchedules, getScheduleSummary, createSchedule, updateSchedule, deleteSchedule as apiDeleteSchedule } from '../api'

const router = useRouter()
const { currentUser, logout, updateProfile } = useAuth()

const schedules = ref([])
const summary = ref({ pending_count: 0, completed_count: 0, total_count: 0 })
const loading = ref(false)

async function fetchSchedules() {
  loading.value = true
  try {
    const [schedRes, sumRes] = await Promise.all([
      getSchedules(),
      getScheduleSummary(),
    ])
    schedules.value = schedRes.data.data || []
    summary.value = sumRes.data.data || { pending_count: 0, completed_count: 0, total_count: 0 }
  } catch (e) {
    showNotice('加载日程失败', 'warning')
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchSchedules())

const isDialogOpen = ref(false)
const isProfileDialogOpen = ref(false)
const isPasswordDialogOpen = ref(false)
const editingId = ref(null)
const formError = ref('')
const profileError = ref('')
const passwordError = ref('')
const confirmDelete = ref(false)
const { notice, showNotice } = usePageNotice()

const scheduleForm = reactive({
  date: '',
  start: '',
  end: '',
  task: '',
  status: '待办',
})

const passwordForm = reactive({
  current: '',
  next: '',
  confirm: '',
})

const profileForm = reactive({
  nickname: '',
  account: '',
  avatarUrl: '',
})

const sortedSchedules = computed(() =>
  [...schedules.value].sort((a, b) => `${a.date} ${a.start}`.localeCompare(`${b.date} ${b.start}`)),
)

const dialogTitle = computed(() => (editingId.value ? '编辑日程' : '添加日程'))
const avatarText = computed(() => currentUser.value.nickname.slice(0, 1).toUpperCase())
const profileAvatarText = computed(() => profileForm.nickname.slice(0, 1).toUpperCase() || 'U')

function getStatusTone(status) {
  const statusMap = {
    待办: 'todo',
    进行中: 'active',
    已完成: 'done',
    未开始: 'idle',
  }

  return statusMap[status] ?? 'todo'
}

function formatDate(date) {
  return date.slice(5)
}

function resetForm() {
  const today = new Date().toISOString().slice(0, 10)
  scheduleForm.date = today
  scheduleForm.start = '09:00'
  scheduleForm.end = '10:00'
  scheduleForm.task = ''
  scheduleForm.status = '待办'
  formError.value = ''
  confirmDelete.value = false
}

function openAddDialog() {
  editingId.value = null
  resetForm()
  isDialogOpen.value = true
}

function openEditDialog(schedule) {
  editingId.value = schedule.id
  scheduleForm.date = schedule.date
  scheduleForm.start = schedule.start
  scheduleForm.end = schedule.end
  scheduleForm.task = schedule.task
  scheduleForm.status = schedule.status
  formError.value = ''
  confirmDelete.value = false
  isDialogOpen.value = true
}

function closeDialog() {
  isDialogOpen.value = false
  formError.value = ''
  confirmDelete.value = false
}

function resetProfileForm() {
  profileForm.nickname = currentUser.value.nickname
  profileForm.account = currentUser.value.account
  profileForm.avatarUrl = currentUser.value.avatarUrl || ''
  profileError.value = ''
}

function openProfileDialog() {
  resetProfileForm()
  isProfileDialogOpen.value = true
}

function closeProfileDialog() {
  isProfileDialogOpen.value = false
  resetProfileForm()
}

function handleAvatarFile(event) {
  const [file] = event.target.files

  if (!file) {
    return
  }

  if (!file.type.startsWith('image/')) {
    profileError.value = '请选择图片作为头像'
    return
  }

  const reader = new FileReader()
  reader.addEventListener('load', () => {
    profileForm.avatarUrl = String(reader.result)
    profileError.value = ''
  })
  reader.readAsDataURL(file)
}

function clearAvatar() {
  profileForm.avatarUrl = ''
}

function submitProfile() {
  const result = updateProfile(profileForm)

  if (!result.ok) {
    profileError.value = result.message
    return
  }

  closeProfileDialog()
  showNotice('个人资料已保存')
}

function resetPasswordForm() {
  passwordForm.current = ''
  passwordForm.next = ''
  passwordForm.confirm = ''
  passwordError.value = ''
}

function openPasswordDialog() {
  resetPasswordForm()
  isPasswordDialogOpen.value = true
}

function closePasswordDialog() {
  isPasswordDialogOpen.value = false
  resetPasswordForm()
}

function submitPassword() {
  if (!passwordForm.current || !passwordForm.next || !passwordForm.confirm) {
    passwordError.value = '请完整填写当前密码和新密码'
    return
  }

  if (passwordForm.next.length < 6) {
    passwordError.value = '新密码至少需要 6 位'
    return
  }

  if (passwordForm.next !== passwordForm.confirm) {
    passwordError.value = '两次输入的新密码不一致'
    return
  }

  closePasswordDialog()
  showNotice('密码已更新')
}

function handleLogout() {
  logout()
  router.replace({
    path: '/login',
    query: {
      loggedOut: '1',
    },
  })
}

async function submitSchedule() {
  if (!scheduleForm.date || !scheduleForm.start || !scheduleForm.end || !scheduleForm.task.trim()) {
    formError.value = '请完整填写日期、时间和任务'
    return
  }

  if (scheduleForm.start >= scheduleForm.end) {
    formError.value = '结束时间需要晚于开始时间'
    return
  }

  const payload = {
    date: scheduleForm.date,
    start: scheduleForm.start,
    end: scheduleForm.end,
    task: scheduleForm.task.trim(),
    status: scheduleForm.status,
  }

  try {
    if (editingId.value) {
      await updateSchedule(editingId.value, payload)
    } else {
      await createSchedule(payload)
    }
    closeDialog()
    showNotice(editingId.value ? '日程已保存' : '新日程已添加')
    await fetchSchedules()
  } catch (e) {
    const msg = e.response?.data?.message || '操作失败'
    formError.value = msg
    showNotice(msg, 'warning')
  }
}

async function deleteSchedule() {
  if (!editingId.value) return

  if (!confirmDelete.value) {
    confirmDelete.value = true
    formError.value = '再次点击删除，确认移除这条日程'
    return
  }

  try {
    await apiDeleteSchedule(editingId.value)
    closeDialog()
    showNotice('日程已删除')
    await fetchSchedules()
  } catch (e) {
    showNotice('删除失败', 'warning')
  }
}
</script>

<template>
  <section class="page-view schedule-view">
    <p
      v-if="notice"
      :class="['page-notice', `page-notice--${notice.tone}`]"
      role="status"
      aria-live="polite"
    >
      {{ notice.message }}
    </p>

    <header class="page-header schedule-header">
      <div>
        <h1 class="page-title">日程清单</h1>
        <p class="page-subtitle">记录每日安排</p>
      </div>
    </header>

    <div class="page-card profile-card">
      <button
        class="profile-card__identity profile-card__identity--button"
        type="button"
        aria-label="查看和编辑个人资料"
        @click="openProfileDialog"
      >
        <span class="profile-card__avatar" aria-hidden="true">
          <img v-if="currentUser.avatarUrl" :src="currentUser.avatarUrl" alt="">
          <span v-else>{{ avatarText }}</span>
        </span>
        <div class="profile-card__person">
          <strong>{{ currentUser.nickname }}</strong>
          <span>校园摊主 · 今日 {{ sortedSchedules.length }} 项安排</span>
        </div>
      </button>
      <div class="profile-card__actions" aria-label="账号操作">
        <button class="profile-card__action" type="button" @click="openPasswordDialog">
          <el-icon><Lock /></el-icon>
          <span>修改密码</span>
        </button>
        <button class="profile-card__action profile-card__action--danger" type="button" @click="handleLogout">
          <el-icon><SwitchButton /></el-icon>
          <span>退出登录</span>
        </button>
      </div>
    </div>

    <Teleport to=".phone-screen">
      <div
        v-if="isProfileDialogOpen"
        class="profile-modal"
        role="dialog"
        aria-modal="true"
        aria-label="个人资料"
        @click.self="closeProfileDialog"
      >
        <form class="profile-modal__card" @submit.prevent="submitProfile">
          <div class="profile-modal__header">
            <div>
              <span>个人中心</span>
              <strong>个人资料</strong>
            </div>
            <button type="button" aria-label="关闭个人资料弹窗" @click="closeProfileDialog">×</button>
          </div>

          <label class="profile-avatar-picker">
            <span class="profile-avatar-picker__preview" aria-hidden="true">
              <img v-if="profileForm.avatarUrl" :src="profileForm.avatarUrl" alt="">
              <span v-else>{{ profileAvatarText }}</span>
            </span>
            <span class="profile-avatar-picker__text">上传头像</span>
            <input type="file" accept="image/*" @change="handleAvatarFile">
          </label>

          <button
            v-if="profileForm.avatarUrl"
            class="profile-avatar-clear"
            type="button"
            @click="clearAvatar"
          >
            移除头像
          </button>

          <label class="schedule-field">
            <span>昵称</span>
            <input
              v-model="profileForm.nickname"
              autocomplete="nickname"
              maxlength="12"
              placeholder="例如：林小摊"
            >
          </label>

          <label class="schedule-field">
            <span>账号</span>
            <input
              v-model="profileForm.account"
              autocomplete="username"
              placeholder="请输入账号"
            >
          </label>

          <p v-if="profileError" class="profile-modal__error" role="alert">{{ profileError }}</p>

          <button class="profile-modal__submit" type="submit">保存资料</button>
        </form>
      </div>
    </Teleport>

    <div class="page-card schedule-panel">
      <div class="schedule-panel__title">
        <div class="schedule-panel__heading">
          <span class="schedule-panel__icon">▣</span>
          <h2>日程列表</h2>
        </div>
        <button class="schedule-panel__add" type="button" aria-label="添加日程" @click="openAddDialog">
          <el-icon><Plus /></el-icon>
        </button>
      </div>

      <div v-if="loading" class="empty-state">加载中…</div>

      <div v-else-if="sortedSchedules.length" class="schedule-table" role="table" aria-label="日程列表">
        <div class="schedule-table__head" role="row">
          <span>日期</span>
          <span>时间</span>
          <span>任务</span>
          <span>状态</span>
        </div>
        <button
          v-for="schedule in sortedSchedules"
          :key="schedule.id"
          class="schedule-row"
          type="button"
          :aria-label="`编辑 ${formatDate(schedule.date)} ${schedule.start} 到 ${schedule.end} 的${schedule.task}日程，状态${schedule.status}`"
          @click="openEditDialog(schedule)"
        >
          <span>{{ formatDate(schedule.date) }}</span>
          <span>{{ schedule.start }}-{{ schedule.end }}</span>
          <strong>{{ schedule.task }}</strong>
          <em :class="['schedule-status', `schedule-status--${getStatusTone(schedule.status)}`]">
            {{ schedule.status }}
          </em>
        </button>
      </div>
      <div v-else class="empty-state">
        <strong>还没有日程</strong>
        <p>添加上课、采购或出摊安排，避免时间冲突。</p>
      </div>
    </div>

    <Teleport to=".phone-screen">
      <div
        v-if="isPasswordDialogOpen"
        class="profile-modal"
        role="dialog"
        aria-modal="true"
        aria-label="修改密码"
        @click.self="closePasswordDialog"
      >
        <form class="profile-modal__card" @submit.prevent="submitPassword">
          <div class="profile-modal__header">
            <div>
              <span>账号安全</span>
              <strong>修改密码</strong>
            </div>
            <button type="button" aria-label="关闭修改密码弹窗" @click="closePasswordDialog">×</button>
          </div>

          <label class="schedule-field">
            <span>当前密码</span>
            <input
              v-model="passwordForm.current"
              type="password"
              autocomplete="current-password"
              placeholder="请输入当前密码"
            >
          </label>

          <label class="schedule-field">
            <span>新密码</span>
            <input
              v-model="passwordForm.next"
              type="password"
              autocomplete="new-password"
              placeholder="至少 6 位"
            >
          </label>

          <label class="schedule-field">
            <span>确认新密码</span>
            <input
              v-model="passwordForm.confirm"
              type="password"
              autocomplete="new-password"
              placeholder="再输入一次新密码"
            >
          </label>

          <p v-if="passwordError" class="profile-modal__error" role="alert">{{ passwordError }}</p>

          <button class="profile-modal__submit" type="submit">保存新密码</button>
        </form>
      </div>
    </Teleport>

    <Teleport to=".phone-screen">
      <div
        v-if="isDialogOpen"
        class="schedule-modal"
        role="dialog"
        aria-modal="true"
        :aria-label="dialogTitle"
        @click.self="closeDialog"
      >
        <form class="schedule-modal__card" @submit.prevent="submitSchedule">
          <div class="schedule-modal__header">
            <div>
              <span>{{ editingId ? '调整安排' : '新建安排' }}</span>
              <strong>{{ dialogTitle }}</strong>
            </div>
            <button type="button" aria-label="关闭日程弹窗" @click="closeDialog">×</button>
          </div>

          <label class="schedule-field">
            <span>选择日期</span>
            <input v-model="scheduleForm.date" type="date">
          </label>

          <div class="schedule-field-grid">
            <label class="schedule-field">
              <span>开始时间</span>
              <input v-model="scheduleForm.start" type="time">
            </label>
            <label class="schedule-field">
              <span>结束时间</span>
              <input v-model="scheduleForm.end" type="time">
            </label>
          </div>

          <label class="schedule-field">
            <span>任务内容</span>
            <input
              v-model="scheduleForm.task"
              autocomplete="off"
              maxlength="30"
              placeholder="例如：晚间出摊"
            >
          </label>

          <label class="schedule-field">
            <span>状态</span>
            <select v-model="scheduleForm.status">
              <option value="未开始">未开始</option>
              <option value="待办">待办</option>
              <option value="进行中">进行中</option>
              <option value="已完成">已完成</option>
            </select>
          </label>

          <p v-if="formError" class="schedule-modal__error" role="alert">{{ formError }}</p>

          <div :class="['schedule-modal__actions', { 'schedule-modal__actions--edit': editingId }]">
            <button
              v-if="editingId"
              class="schedule-modal__delete"
              type="button"
              @click="deleteSchedule"
            >
              {{ confirmDelete ? '确认删除' : '删除' }}
            </button>
            <button class="schedule-modal__submit" type="submit">
              {{ editingId ? '保存' : '添加' }}
            </button>
          </div>
        </form>
      </div>
    </Teleport>
  </section>
</template>

<style scoped>
.schedule-view {
  min-height: 100%;
  background:
    linear-gradient(180deg, #f4fbff 0%, #f8fbff 25%, #ffffff 62%, #ffffff 100%);
}

.schedule-header {
  align-items: center;
  margin-bottom: 18px;
}

.profile-card {
  display: grid;
  gap: 16px;
  padding: 18px;
  background: rgba(255, 255, 255, 0.96);
}

.profile-card__identity {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.profile-card__identity--button {
  width: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  color: inherit;
  text-align: left;
}

.profile-card__avatar {
  flex: 0 0 auto;
  display: grid;
  width: 56px;
  height: 56px;
  place-items: center;
  border-radius: 50%;
  background: linear-gradient(135deg, #dff2ff 0%, #b9dcff 100%);
  color: #1d5fb6;
  box-shadow: inset 0 0 0 1px rgba(45, 115, 219, 0.12);
  font-size: 1.2rem;
  font-weight: 900;
  overflow: hidden;
}

.profile-card__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-card__person {
  display: grid;
  gap: 5px;
  min-width: 0;
}

.profile-card__person strong {
  overflow: hidden;
  color: var(--text-main);
  font-size: 1.05rem;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-card__person span {
  overflow: hidden;
  color: var(--text-muted);
  font-size: 0.76rem;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-card__actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.profile-card__action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: 44px;
  padding: 11px 10px;
  border: 0;
  border-radius: 14px;
  background: #eef5ff;
  color: var(--primary);
  font-size: 0.78rem;
  font-weight: 900;
}

.profile-card__action--danger {
  background: #fff1f1;
  color: #d93636;
}

.schedule-panel {
  margin-top: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.96);
}

.schedule-panel__title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.schedule-panel__heading {
  display: flex;
  align-items: center;
  gap: 9px;
  min-width: 0;
}

.schedule-panel__icon {
  display: grid;
  width: 32px;
  height: 32px;
  place-items: center;
  border-radius: 11px;
  background: #edf6ff;
  color: var(--primary);
  font-size: 0.9rem;
}

.schedule-panel h2 {
  margin: 0;
  color: var(--text-main);
  font-size: 1rem;
}

.schedule-panel__add {
  display: grid;
  flex: 0 0 auto;
  width: 44px;
  height: 44px;
  place-items: center;
  border: 0;
  border-radius: 14px;
  background: #eef5ff;
  color: var(--primary);
  font-size: 1.18rem;
  font-weight: 900;
}

.schedule-table {
  display: grid;
}

.schedule-table__head,
.schedule-row {
  display: grid;
  grid-template-columns: 0.75fr 1.35fr 1.35fr 0.9fr;
  align-items: center;
  gap: 8px;
}

.schedule-table__head {
  padding: 0 0 10px;
  border-bottom: 1px solid rgba(105, 145, 198, 0.12);
  color: var(--text-muted);
  font-size: 0.68rem;
  font-weight: 800;
}

.schedule-row {
  width: 100%;
  min-height: 44px;
  padding: 10px 0;
  border: 0;
  border-bottom: 1px solid rgba(105, 145, 198, 0.08);
  background: transparent;
  color: #5e708a;
  text-align: left;
  font-size: 0.72rem;
}

.schedule-row:last-child {
  border-bottom: 0;
}

.schedule-row strong {
  overflow: hidden;
  color: var(--text-main);
  font-size: 0.74rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.schedule-status {
  display: inline-flex;
  justify-content: center;
  padding: 5px 7px;
  border-radius: 8px;
  font-style: normal;
  font-size: 0.66rem;
  font-weight: 800;
  white-space: nowrap;
}

.schedule-status--todo,
.schedule-status--idle {
  background: #eef5ff;
  color: var(--primary);
}

.schedule-status--active {
  background: #fff1e4;
  color: #f07c22;
}

.schedule-status--done {
  background: #e7f8ef;
  color: #16a46b;
}

:global(.profile-modal) {
  position: absolute;
  inset: 0;
  z-index: 20;
  display: grid;
  place-items: center;
  padding: 22px;
  background: rgba(17, 37, 61, 0.28);
  backdrop-filter: blur(10px);
}

:global(.profile-modal__card) {
  width: min(320px, 100%);
  padding: 18px;
  border: 1px solid rgba(126, 165, 220, 0.18);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 24px 60px rgba(18, 30, 52, 0.22);
}

:global(.profile-modal__header) {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 14px;
}

:global(.profile-modal__header span) {
  display: block;
  margin-bottom: 4px;
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 700;
}

:global(.profile-modal__header strong) {
  color: var(--text-main);
  font-size: 1.35rem;
  line-height: 1;
}

:global(.profile-modal__header button) {
  display: grid;
  width: 44px;
  height: 44px;
  place-items: center;
  border: 0;
  border-radius: 999px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 1.2rem;
}

:global(.profile-modal__error) {
  margin: 10px 0 0;
  color: #ef4444;
  font-size: 0.72rem;
  font-weight: 700;
}

.profile-avatar-picker {
  display: grid;
  justify-items: center;
  gap: 8px;
  padding: 12px;
  border: 1px dashed rgba(126, 165, 220, 0.32);
  border-radius: 18px;
  background: #f8fbff;
  color: var(--primary);
  font-size: 0.78rem;
  font-weight: 900;
}

.profile-avatar-picker input {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.profile-avatar-picker__preview {
  display: grid;
  width: 72px;
  height: 72px;
  place-items: center;
  overflow: hidden;
  border-radius: 50%;
  background: linear-gradient(135deg, #dff2ff 0%, #b9dcff 100%);
  color: #1d5fb6;
  box-shadow: inset 0 0 0 1px rgba(45, 115, 219, 0.12);
  font-size: 1.35rem;
  font-weight: 900;
}

.profile-avatar-picker__preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-avatar-picker__text {
  color: var(--primary);
}

.profile-avatar-clear {
  justify-self: center;
  min-height: 34px;
  padding: 7px 12px;
  border: 0;
  border-radius: 999px;
  background: #fff1f1;
  color: #d93636;
  font-size: 0.72rem;
  font-weight: 900;
}

:global(.profile-modal__submit) {
  width: 100%;
  min-height: 44px;
  margin-top: 14px;
  padding: 12px 8px;
  border: 0;
  border-radius: 15px;
  background: linear-gradient(135deg, #6fbaff 0%, #2d73db 100%);
  color: #ffffff;
  box-shadow: 0 12px 24px rgba(45, 115, 219, 0.22);
  font-size: 0.82rem;
  font-weight: 900;
}

:global(.schedule-modal) {
  position: absolute;
  inset: 0;
  z-index: 20;
  display: grid;
  place-items: center;
  padding: 22px;
  background: rgba(17, 37, 61, 0.28);
  backdrop-filter: blur(10px);
}

:global(.schedule-modal__card) {
  width: min(320px, 100%);
  padding: 18px;
  border: 1px solid rgba(126, 165, 220, 0.18);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 24px 60px rgba(18, 30, 52, 0.22);
}

:global(.schedule-modal__header) {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 14px;
}

:global(.schedule-modal__header span) {
  display: block;
  margin-bottom: 4px;
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 700;
}

:global(.schedule-modal__header strong) {
  color: var(--text-main);
  font-size: 1.35rem;
  line-height: 1;
}

:global(.schedule-modal__header button) {
  display: grid;
  width: 44px;
  height: 44px;
  place-items: center;
  border: 0;
  border-radius: 999px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 1.2rem;
}

.schedule-field {
  display: grid;
  gap: 7px;
  margin-top: 11px;
}

.schedule-field-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.schedule-field span {
  color: var(--text-main);
  font-size: 0.76rem;
  font-weight: 800;
}

.schedule-field input,
.schedule-field select {
  width: 100%;
  padding: 11px 12px;
  border: 1px solid rgba(126, 165, 220, 0.2);
  border-radius: 14px;
  outline: 0;
  background: #f8fbff;
  color: var(--text-main);
  font-size: 0.82rem;
}

.schedule-field input:focus,
.schedule-field select:focus {
  border-color: rgba(45, 115, 219, 0.45);
  box-shadow: 0 0 0 3px rgba(45, 115, 219, 0.08);
}

:global(.schedule-modal__error) {
  margin: 10px 0 0;
  color: #ef4444;
  font-size: 0.72rem;
  font-weight: 700;
}

:global(.schedule-modal__actions) {
  display: grid;
  margin-top: 14px;
}

:global(.schedule-modal__actions--edit) {
  grid-template-columns: 0.9fr 1.1fr;
  gap: 10px;
}

:global(.schedule-modal__delete),
:global(.schedule-modal__submit) {
  width: 100%;
  min-height: 44px;
  padding: 12px 8px;
  border: 0;
  border-radius: 15px;
  font-size: 0.82rem;
  font-weight: 900;
}

:global(.schedule-modal__delete) {
  background: #fff1f1;
  color: #ef4444;
}

:global(.schedule-modal__submit) {
  background: linear-gradient(135deg, #6fbaff 0%, #2d73db 100%);
  color: #ffffff;
  box-shadow: 0 12px 24px rgba(45, 115, 219, 0.22);
}

@media (max-width: 420px) {
  .profile-card {
    padding: 16px;
  }

  .profile-card__avatar {
    width: 52px;
    height: 52px;
  }

  .profile-card__action {
    font-size: 0.74rem;
  }

  .schedule-table__head,
  .schedule-row {
    grid-template-columns: 0.7fr 1.35fr 1.25fr 0.88fr;
    gap: 6px;
  }
}

@media (max-width: 380px) {
  .profile-card__actions {
    gap: 8px;
  }

  .profile-card__action {
    padding-right: 8px;
    padding-left: 8px;
    font-size: 0.7rem;
  }

  .schedule-panel__add {
    width: 40px;
    height: 40px;
  }

  .schedule-table__head {
    display: none;
  }

  .schedule-row {
    grid-template-columns: 0.8fr 1.2fr;
    gap: 8px 10px;
    padding: 12px 0;
  }

  .schedule-row strong {
    font-size: 0.82rem;
  }

  .schedule-status {
    justify-self: start;
  }
}
</style>
