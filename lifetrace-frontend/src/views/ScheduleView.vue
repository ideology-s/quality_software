<script setup>
import { computed, reactive, ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

const taskOptions = [
  '上课',
  '进货采购',
  '晚间出摊',
  '整理库存',
  '回复客户消息',
  '准备明日货品',
]

const schedules = ref([
  { id: 1, date: '2026-05-24', start: '08:30', end: '10:00', task: '上课', status: '待办' },
  { id: 2, date: '2026-05-24', start: '14:00', end: '15:00', task: '进货采购', status: '进行中' },
  { id: 3, date: '2026-05-24', start: '17:30', end: '20:30', task: '晚间出摊', status: '待办' },
  { id: 4, date: '2026-05-24', start: '21:00', end: '21:30', task: '整理库存', status: '已完成' },
  { id: 5, date: '2026-05-25', start: '09:00', end: '10:00', task: '回复客户消息', status: '已完成' },
  { id: 6, date: '2026-05-25', start: '15:00', end: '16:00', task: '准备明日货品', status: '未开始' },
])

const isDialogOpen = ref(false)
const editingId = ref(null)
const formError = ref('')

const scheduleForm = reactive({
  date: '',
  start: '',
  end: '',
  task: '',
  status: '待办',
})

const sortedSchedules = computed(() =>
  [...schedules.value].sort((a, b) => `${a.date} ${a.start}`.localeCompare(`${b.date} ${b.start}`)),
)

const pendingCount = computed(() =>
  schedules.value.filter((item) => item.status !== '已完成').length,
)

const completedCount = computed(() =>
  schedules.value.filter((item) => item.status === '已完成').length,
)

const dialogTitle = computed(() => (editingId.value ? '编辑日程' : '添加日程'))

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
  scheduleForm.date = '2026-05-24'
  scheduleForm.start = '09:00'
  scheduleForm.end = '10:00'
  scheduleForm.task = taskOptions[0]
  scheduleForm.status = '待办'
  formError.value = ''
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
  isDialogOpen.value = true
}

function closeDialog() {
  isDialogOpen.value = false
  formError.value = ''
}

function submitSchedule() {
  if (!scheduleForm.date || !scheduleForm.start || !scheduleForm.end || !scheduleForm.task) {
    formError.value = '请完整选择日期、时间和任务'
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
    task: scheduleForm.task,
    status: scheduleForm.status,
  }

  if (editingId.value) {
    const index = schedules.value.findIndex((item) => item.id === editingId.value)

    if (index !== -1) {
      schedules.value[index] = {
        ...schedules.value[index],
        ...payload,
      }
    }
  } else {
    schedules.value.push({
      id: Date.now(),
      ...payload,
    })
  }

  closeDialog()
}

function deleteSchedule() {
  if (!editingId.value) {
    return
  }

  schedules.value = schedules.value.filter((item) => item.id !== editingId.value)
  closeDialog()
}
</script>

<template>
  <section class="page-view schedule-view">
    <header class="page-header schedule-header">
      <div>
        <h1 class="page-title">日程清单</h1>
        <p class="page-subtitle">记录每日安排</p>
      </div>
      <button class="schedule-add" type="button" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
      </button>
    </header>

    <div class="page-card schedule-summary">
      <div class="schedule-summary__item">
        <span class="schedule-summary__icon">▣</span>
        <div>
          <p>待完成</p>
          <strong>{{ pendingCount }}<small>项</small></strong>
        </div>
      </div>
      <div class="schedule-summary__item">
        <span class="schedule-summary__icon schedule-summary__icon--done">✓</span>
        <div>
          <p>已完成</p>
          <strong>{{ completedCount }}<small>项</small></strong>
        </div>
      </div>
      <span class="schedule-summary__pill">安排适中</span>
    </div>

    <div class="page-card schedule-panel">
      <div class="schedule-panel__title">
        <span class="schedule-panel__icon">▣</span>
        <h2>日程列表</h2>
      </div>

      <div class="schedule-table" role="table" aria-label="日程列表">
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
    </div>

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
            <button type="button" @click="closeDialog">×</button>
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
            <span>选择任务</span>
            <select v-model="scheduleForm.task">
              <option
                v-for="task in taskOptions"
                :key="task"
                :value="task"
              >
                {{ task }}
              </option>
            </select>
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

          <p v-if="formError" class="schedule-modal__error">{{ formError }}</p>

          <div :class="['schedule-modal__actions', { 'schedule-modal__actions--edit': editingId }]">
            <button
              v-if="editingId"
              class="schedule-modal__delete"
              type="button"
              @click="deleteSchedule"
            >
              删除
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

.schedule-add {
  display: grid;
  width: 48px;
  height: 48px;
  place-items: center;
  border: 1px solid rgba(87, 145, 230, 0.16);
  border-radius: 17px;
  background: rgba(255, 255, 255, 0.94);
  color: var(--primary);
  box-shadow: 0 10px 24px rgba(71, 119, 183, 0.12);
  font-size: 1.35rem;
}

.schedule-summary {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  align-items: center;
  gap: 14px;
  padding: 18px;
  background: rgba(255, 255, 255, 0.96);
}

.schedule-summary__item {
  display: grid;
  grid-template-columns: 40px minmax(0, 1fr);
  align-items: center;
  gap: 10px;
}

.schedule-summary__item + .schedule-summary__item {
  padding-left: 14px;
  border-left: 1px solid rgba(105, 145, 198, 0.14);
}

.schedule-summary__icon {
  display: grid;
  width: 38px;
  height: 38px;
  place-items: center;
  border-radius: 14px;
  background: #edf6ff;
  color: var(--primary);
  font-size: 1rem;
  font-weight: 900;
}

.schedule-summary__icon--done {
  background: #e1f7ee;
  color: #16a46b;
}

.schedule-summary p {
  margin: 0 0 4px;
  color: var(--text-muted);
  font-size: 0.72rem;
  font-weight: 700;
}

.schedule-summary strong {
  color: #4b8cff;
  font-size: 1.25rem;
  line-height: 1;
}

.schedule-summary small {
  margin-left: 3px;
  color: var(--text-muted);
  font-size: 0.7rem;
}

.schedule-summary__pill {
  padding: 7px 10px;
  border-radius: 999px;
  background: #eef5ff;
  color: var(--primary);
  font-size: 0.72rem;
  font-weight: 800;
  white-space: nowrap;
}

.schedule-panel {
  margin-top: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.96);
}

.schedule-panel__title {
  display: flex;
  align-items: center;
  gap: 9px;
  margin-bottom: 16px;
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

:global(.schedule-modal) {
  position: absolute;
  inset: 0;
  z-index: 9999;
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
  width: 32px;
  height: 32px;
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
  .schedule-summary {
    gap: 10px;
    padding: 16px;
  }

  .schedule-summary__item {
    grid-template-columns: 36px minmax(0, 1fr);
    gap: 8px;
  }

  .schedule-summary__pill {
    padding: 6px 8px;
    font-size: 0.68rem;
  }

  .schedule-table__head,
  .schedule-row {
    grid-template-columns: 0.7fr 1.35fr 1.25fr 0.88fr;
    gap: 6px;
  }
}
</style>
