<script setup>
import { computed, reactive, ref } from 'vue'
import {
  Calendar,
  Clock,
  LocationFilled,
  Plus,
  Wallet,
} from '@element-plus/icons-vue'
import { usePageNotice } from '../composables/usePageNotice'

const isDialogOpen = ref(false)
const editingLogId = ref(null)
const formError = ref('')
const selectedLogDate = ref('all')
const { notice, showNotice } = usePageNotice()

const logs = ref([
  {
    id: 1,
    date: '2026-06-11',
    weekday: '周三',
    start: '17:30',
    end: '20:30',
    location: '下沙大学城夜市',
    income: 128,
    profit: 45,
    note: '客流稳定，零食包销量较好',
  },
  {
    id: 2,
    date: '2026-06-10',
    weekday: '周二',
    start: '18:00',
    end: '21:00',
    location: '宿舍楼下',
    income: 96,
    profit: 32,
    note: '钥匙扣卖得较好',
  },
  {
    id: 3,
    date: '2026-06-08',
    weekday: '周日',
    start: '14:00',
    end: '16:30',
    location: '社团集市',
    income: 156,
    profit: 58,
    note: '人流较多，库存消耗快',
  },
  {
    id: 4,
    date: '2026-06-05',
    weekday: '周四',
    start: '19:00',
    end: '22:00',
    location: '学校东门步行街',
    income: 80,
    profit: 18,
    note: '天气热，饮品更受欢迎',
  },
  {
    id: 5,
    date: '2026-06-03',
    weekday: '周二',
    start: '17:00',
    end: '20:00',
    location: '地铁口附近',
    income: 72,
    profit: 20,
    note: '客流一般，主要卖钥匙扣',
  },
])

const logForm = reactive({
  date: '2026-06-12',
  start: '18:00',
  end: '21:00',
  location: '',
  income: '',
  profit: '',
  note: '',
})

const weekSummary = computed(() => {
  const totalMinutes = logs.value.reduce((sum, log) => sum + getDurationMinutes(log.start, log.end), 0)
  const totalIncome = logs.value.reduce((sum, log) => sum + log.income, 0)

  return {
    count: logs.value.length,
    hours: (totalMinutes / 60).toFixed(1),
    income: totalIncome,
  }
})

const sortedLogs = computed(() =>
  [...logs.value].sort((a, b) => b.date.localeCompare(a.date)),
)

const filteredLogs = computed(() => {
  if (selectedLogDate.value === 'all') {
    return sortedLogs.value
  }

  return sortedLogs.value.filter((log) => log.date === selectedLogDate.value)
})

const logDateOptions = computed(() =>
  sortedLogs.value.reduce((options, log) => {
    if (!options.some((option) => option.value === log.date)) {
      options.push({
        value: log.date,
        label: `${formatDate(log.date)} ${log.weekday}`,
      })
    }

    return options
  }, []),
)

function getDurationMinutes(start, end) {
  const [startHour, startMinute] = start.split(':').map(Number)
  const [endHour, endMinute] = end.split(':').map(Number)
  return (endHour * 60 + endMinute) - (startHour * 60 + startMinute)
}

function getWeekday(date) {
  const weekdayMap = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return weekdayMap[new Date(`${date}T00:00:00`).getDay()]
}

function formatDate(date) {
  const [, month, day] = date.split('-')
  return `${Number(month)}月${Number(day)}日`
}

function resetForm() {
  logForm.date = '2026-06-12'
  logForm.start = '18:00'
  logForm.end = '21:00'
  logForm.location = ''
  logForm.income = ''
  logForm.profit = ''
  logForm.note = ''
  formError.value = ''
}

function openLogDialog() {
  editingLogId.value = null
  resetForm()
  isDialogOpen.value = true
}

function openLogDetail(log) {
  editingLogId.value = log.id
  logForm.date = log.date
  logForm.start = log.start
  logForm.end = log.end
  logForm.location = log.location
  logForm.income = String(log.income)
  logForm.profit = String(log.profit)
  logForm.note = log.note
  formError.value = ''
  isDialogOpen.value = true
}

function saveLog() {
  if (!logForm.location.trim()) {
    formError.value = '请填写出摊地点'
    return
  }

  const payload = {
    date: logForm.date,
    weekday: getWeekday(logForm.date),
    start: logForm.start,
    end: logForm.end,
    location: logForm.location.trim(),
    income: Number(logForm.income) || 0,
    profit: Number(logForm.profit) || 0,
    note: logForm.note.trim() || '暂无备注',
  }

  const isEditing = Boolean(editingLogId.value)

  if (isEditing) {
    const index = logs.value.findIndex((log) => log.id === editingLogId.value)

    if (index !== -1) {
      logs.value[index] = {
        ...logs.value[index],
        ...payload,
      }
    }
  } else {
    logs.value.unshift({
      id: Date.now(),
      ...payload,
    })
  }

  isDialogOpen.value = false
  showNotice(isEditing ? '日志已保存' : '新日志已记录')
}
</script>

<template>
  <section class="page-view stall-log-view">
    <p
      v-if="notice"
      :class="['page-notice', `page-notice--${notice.tone}`]"
      role="status"
      aria-live="polite"
    >
      {{ notice.message }}
    </p>

    <header class="page-header log-header">
      <div>
        <h1 class="page-title">出摊日志</h1>
        <p class="page-subtitle">记录每次出摊，复盘经营情况</p>
      </div>
      <button class="log-add" type="button" aria-label="新增出摊日志" @click="openLogDialog">
        <el-icon><Plus /></el-icon>
        <span>新增日志</span>
      </button>
    </header>

    <section class="page-card summary-card">
      <h2>本周概览</h2>
      <div class="summary-grid">
        <div class="summary-item">
          <span class="summary-icon">
            <el-icon><Calendar /></el-icon>
          </span>
          <div>
            <p>本周出摊</p>
            <strong>{{ weekSummary.count }}<small>次</small></strong>
          </div>
        </div>
        <div class="summary-item">
          <span class="summary-icon summary-icon--green">
            <el-icon><Clock /></el-icon>
          </span>
          <div>
            <p>累计时长</p>
            <strong>{{ weekSummary.hours }}<small>h</small></strong>
          </div>
        </div>
        <div class="summary-item">
          <span class="summary-icon summary-icon--orange">
            <el-icon><Wallet /></el-icon>
          </span>
          <div>
            <p>本周收入</p>
            <strong>¥{{ weekSummary.income }}</strong>
          </div>
        </div>
      </div>
    </section>

    <section class="log-section">
      <div class="log-section__title">
        <h2>日志列表</h2>
        <label class="log-date-filter">
          <span class="sr-only">按日期筛选日志</span>
          <select v-model="selectedLogDate" aria-label="按日期筛选日志">
            <option value="all">全部日期</option>
            <option
              v-for="option in logDateOptions"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </label>
      </div>

      <div v-if="filteredLogs.length" class="log-list">
        <button
          v-for="log in filteredLogs"
          :key="log.id"
          class="log-card"
          type="button"
          :aria-label="`查看 ${formatDate(log.date)} ${log.location} 的出摊日志`"
          @click="openLogDetail(log)"
        >
          <div class="log-date">
            <strong>{{ formatDate(log.date) }}</strong>
            <span>{{ log.weekday }}</span>
          </div>
          <div class="log-content">
            <div class="log-meta">
              <span>
                <el-icon><Clock /></el-icon>
                {{ log.start }}-{{ log.end }}
              </span>
              <span>
                <el-icon><LocationFilled /></el-icon>
                {{ log.location }}
              </span>
            </div>
            <div class="log-money">
              <span>收入 ¥{{ log.income }}</span>
              <span>利润 ¥{{ log.profit }}</span>
            </div>
            <p>备注：{{ log.note }}</p>
          </div>
          <span class="log-arrow">›</span>
        </button>
      </div>
      <div v-else class="empty-state">
        <strong>{{ sortedLogs.length ? '该日期没有日志' : '还没有出摊日志' }}</strong>
        <p>{{ sortedLogs.length ? '切换到全部日期，查看已有出摊记录。' : '记录第一次出摊后，这里会显示收入、利润和复盘备注。' }}</p>
      </div>
    </section>

    <el-dialog
      v-model="isDialogOpen"
      :title="editingLogId ? '日志详情' : '新增出摊日志'"
      width="320px"
      class="stall-log-dialog"
      :append-to-body="false"
    >
      <el-form label-position="top" class="log-form">
        <el-form-item label="出摊日期">
          <el-input v-model="logForm.date" type="date" />
        </el-form-item>
        <div class="log-form__grid">
          <el-form-item label="开始时间">
            <el-input v-model="logForm.start" type="time" />
          </el-form-item>
          <el-form-item label="结束时间">
            <el-input v-model="logForm.end" type="time" />
          </el-form-item>
        </div>
        <el-form-item label="出摊地点">
          <el-input v-model="logForm.location" placeholder="例如：下沙大学城夜市" />
        </el-form-item>
        <div class="log-form__grid">
          <el-form-item label="收入">
            <el-input v-model="logForm.income" inputmode="numeric" placeholder="128" />
          </el-form-item>
          <el-form-item label="利润">
            <el-input v-model="logForm.profit" inputmode="numeric" placeholder="45" />
          </el-form-item>
        </div>
        <el-form-item label="备注">
          <el-input
            v-model="logForm.note"
            type="textarea"
            :rows="2"
            placeholder="记录客流、热销商品等"
          />
        </el-form-item>
      </el-form>
      <p v-if="formError" class="log-form-error" role="alert">{{ formError }}</p>
      <template #footer>
        <button class="log-dialog-button log-dialog-button--ghost" type="button" @click="isDialogOpen = false">
          取消
        </button>
        <button class="log-dialog-button" type="button" @click="saveLog">
          {{ editingLogId ? '保存修改' : '保存' }}
        </button>
      </template>
    </el-dialog>
  </section>
</template>

<style>
.stall-log-view {
  min-height: 100%;
  background:
    linear-gradient(180deg, #f4fbff 0%, #f8fbff 24%, #ffffff 62%, #ffffff 100%);
}

.log-header {
  align-items: center;
  margin-bottom: 18px;
}

.log-add {
  display: grid;
  justify-items: center;
  gap: 5px;
  min-width: 54px;
  min-height: 54px;
  border: 0;
  background: transparent;
  color: var(--text-muted);
  font-size: 0.68rem;
  font-weight: 800;
}

.log-add :deep(.el-icon) {
  display: grid;
  width: 44px;
  height: 44px;
  place-items: center;
  border-radius: 50%;
  background: linear-gradient(135deg, #6fbaff 0%, #2d73db 100%);
  color: #ffffff;
  box-shadow: 0 10px 22px rgba(45, 115, 219, 0.22);
  font-size: 1.35rem;
}

.summary-card {
  padding: 16px;
  background: rgba(255, 255, 255, 0.96);
}

.summary-card h2 {
  margin: 0 0 14px;
  color: var(--text-main);
  font-size: 0.9rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.summary-item {
  display: grid;
  grid-template-columns: 38px minmax(0, 1fr);
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.summary-item + .summary-item {
  padding-left: 10px;
  border-left: 1px solid rgba(105, 145, 198, 0.14);
}

.summary-icon {
  display: grid;
  width: 36px;
  height: 36px;
  place-items: center;
  border-radius: 13px;
  background: #edf6ff;
  color: var(--primary);
  font-size: 1rem;
}

.summary-icon--green {
  background: #e7f8ef;
  color: #16a46b;
}

.summary-icon--orange {
  background: #fff1e4;
  color: #f07c22;
}

.summary-item p {
  margin: 0 0 4px;
  color: var(--text-muted);
  font-size: 0.66rem;
  font-weight: 800;
  white-space: nowrap;
}

.summary-item strong {
  color: var(--text-main);
  font-size: 1rem;
  line-height: 1;
  white-space: nowrap;
}

.summary-item:nth-child(2) strong {
  color: #16a46b;
}

.summary-item small {
  margin-left: 2px;
  color: var(--text-muted);
  font-size: 0.66rem;
}

.log-section {
  margin-top: 24px;
}

.log-section__title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.log-section__title h2 {
  margin: 0;
  color: var(--text-main);
  font-size: 1.05rem;
}

.log-date-filter {
  position: relative;
  display: inline-flex;
}

.log-date-filter::after {
  content: "⌄";
  position: absolute;
  right: 11px;
  top: 50%;
  color: #607894;
  font-size: 0.72rem;
  font-weight: 900;
  transform: translateY(-50%);
  pointer-events: none;
}

.log-date-filter select {
  min-height: 36px;
  padding: 8px 28px 8px 12px;
  border: 1px solid rgba(105, 145, 198, 0.12);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.92);
  color: var(--text-muted);
  font-size: 0.72rem;
  font-weight: 800;
  appearance: none;
}

.log-list {
  display: grid;
  gap: 12px;
}

.log-card {
  display: grid;
  grid-template-columns: 68px minmax(0, 1fr) 14px;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 14px 12px;
  border: 1px solid rgba(105, 145, 198, 0.1);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 10px 24px rgba(66, 105, 153, 0.08);
  cursor: pointer;
  color: inherit;
  text-align: left;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.log-card:hover {
  box-shadow: 0 8px 16px rgba(66, 105, 153, 0.08);
}

.log-card:active {
  transform: scale(0.985);
}

.log-date {
  display: grid;
  place-items: center;
  min-height: 68px;
  border-radius: 14px;
  background: #edf6ff;
}

.log-date strong {
  color: var(--primary);
  font-size: 0.86rem;
}

.log-date span {
  color: var(--text-muted);
  font-size: 0.68rem;
  font-weight: 700;
}

.log-content {
  min-width: 0;
}

.log-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  color: #607894;
  font-size: 0.72rem;
  font-weight: 700;
}

.log-meta span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.log-meta :deep(.el-icon) {
  color: var(--primary);
}

.log-money {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.log-money span {
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.68rem;
  font-weight: 800;
}

.log-money span:first-child {
  background: #e7f8ef;
  color: #16a46b;
}

.log-money span:last-child {
  background: #fff1e4;
  color: #f07c22;
}

.log-content p {
  overflow: hidden;
  margin: 8px 0 0;
  color: var(--text-muted);
  font-size: 0.7rem;
  line-height: 1.35;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.log-arrow {
  color: #94a3b8;
  font-size: 1.3rem;
}

.stall-log-dialog :deep(.el-dialog) {
  border-radius: 22px;
}

.stall-log-dialog :deep(.el-dialog__body) {
  padding-top: 4px;
}

.log-form :deep(.el-form-item) {
  margin-bottom: 12px;
}

.log-form__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.log-form-error {
  margin: 0 0 8px;
  color: #ef4444;
  font-size: 0.74rem;
  font-weight: 800;
}

.log-dialog-button {
  min-width: 80px;
  min-height: 44px;
  padding: 10px 14px;
  border: 0;
  border-radius: 13px;
  background: linear-gradient(135deg, #6fbaff 0%, #2d73db 100%);
  color: #ffffff;
  font-size: 0.82rem;
  font-weight: 900;
}

.log-dialog-button--ghost {
  margin-right: 8px;
  background: #f1f5f9;
  color: #64748b;
}

@media (max-width: 420px) {
  .summary-grid {
    gap: 8px;
  }

  .summary-item {
    grid-template-columns: 34px minmax(0, 1fr);
    gap: 6px;
  }

  .summary-icon {
    width: 32px;
    height: 32px;
  }

  .log-card {
    grid-template-columns: 64px minmax(0, 1fr) 12px;
    gap: 10px;
  }
}
</style>
