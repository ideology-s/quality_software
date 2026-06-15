<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { usePageNotice } from '../composables/usePageNotice'
import { getQueueList, getQueueSummary, takeNumber, serveNext, completeOrder, cancelOrder } from '../api'

const queueItems = ref([])
const queueSummary = ref({ current_number: null, queue_count: 0, is_crowded: false })
const loading = ref(false)

const { notice, showNotice } = usePageNotice()

async function fetchQueue() {
  loading.value = true
  try {
    const [listRes, sumRes] = await Promise.all([
      getQueueList(),
      getQueueSummary(),
    ])
    queueItems.value = (listRes.data.data || []).map(item => ({
      number: item.number,
      customer: item.customer,
      order: item.order || item.order_content,
      quantity: item.quantity,
      note: item.note,
      status: item.status,
      tone: getTone(item.status),
    }))
    queueSummary.value = sumRes.data.data || { current_number: null, queue_count: 0, is_crowded: false }
  } catch (e) {
    showNotice('加载排队信息失败', 'warning')
  } finally {
    loading.value = false
  }
}

function getTone(status) {
  const map = { '服务中': 'serving', '等待中': 'waiting', '已完成': 'completed', '已取消': 'cancelled' }
  return map[status] || 'waiting'
}

onMounted(() => fetchQueue())

const actionItems = [
  { id: 'add', label: '新增取号', icon: '+', tone: 'neutral' },
  { id: 'next', label: '叫下一号', icon: '!', tone: 'call' },
  { id: 'complete', label: '完成订单', icon: '✓', tone: 'done' },
  { id: 'cancel', label: '取消订单', icon: '×', tone: 'danger' },
]

const isDialogOpen = ref(false)
const formError = ref('')
const queueForm = reactive({
  customer: '',
  orderText: '',
  note: '',
})

const currentService = computed(() =>
  queueItems.value.find((item) => item.tone === 'serving'),
)

const summaryItems = computed(() => [
  { label: '当前号码', value: currentService.value?.number ?? '--', tone: 'primary' },
  { label: '排队人数', value: `${queueSummary.value.queue_count} 人`, tone: 'default' },
  { label: '服务状态', value: currentService.value?.status ?? '待叫号', tone: currentService.value ? 'success' : 'default' },
])

function resetForm() {
  queueForm.customer = ''
  queueForm.orderText = ''
  queueForm.note = ''
  formError.value = ''
}

function openAddDialog() {
  resetForm()
  isDialogOpen.value = true
}

function closeAddDialog() {
  isDialogOpen.value = false
  formError.value = ''
}

function parseOrderText(orderText) {
  const match = orderText.trim().match(/^(.*?)(?:\s*[x×]\s*(\d+))$/i)

  if (!match) {
    return {
      order: orderText.trim(),
      quantity: '×1',
    }
  }

  return {
    order: match[1].trim(),
    quantity: `×${match[2]}`,
  }
}

async function submitNewTicket() {
  if (!queueForm.customer.trim() || !queueForm.orderText.trim()) {
    formError.value = '请填写顾客姓名和商品内容'
    return
  }

  const parsedOrder = parseOrderText(queueForm.orderText)

  try {
    const res = await takeNumber({
      customer: queueForm.customer.trim(),
      order: parsedOrder.order,
      quantity: parsedOrder.quantity,
      note: queueForm.note.trim() || '无备注',
    })
    if (res.data.code === 409) {
      formError.value = res.data.message
      return
    }
    closeAddDialog()
    showNotice('取号成功')
    await fetchQueue()
  } catch (e) {
    const msg = e.response?.data?.message || '取号失败'
    formError.value = msg
    showNotice(msg, 'warning')
  }
}

async function handleAction(actionId) {
  if (actionId === 'add') {
    openAddDialog()
    return
  }

  try {
    if (actionId === 'next') {
      const res = await serveNext('_')
      if (res.data.code === 400) {
        showNotice(res.data.message, 'warning')
      } else {
        showNotice('已叫号')
      }
    } else if (actionId === 'complete') {
      if (!currentService.value) {
        showNotice('暂无正在服务的订单', 'warning')
        return
      }
      await completeOrder(currentService.value.number)
      showNotice('订单已完成')
    } else if (actionId === 'cancel') {
      if (!currentService.value) {
        showNotice('暂无正在服务的订单', 'warning')
        return
      }
      await cancelOrder(currentService.value.number)
      showNotice('订单已取消')
    }
    await fetchQueue()
  } catch (e) {
    const msg = e.response?.data?.message || '操作失败'
    showNotice(msg, 'warning')
  }
}

function isActionUnavailable(actionId) {
  if (['complete', 'cancel'].includes(actionId)) {
    return !currentService.value
  }
  if (actionId === 'next') {
    return !queueItems.value.some((item) => item.tone === 'waiting')
  }
  return false
}
</script>

<template>
  <section class="page-view queue-view">
    <p
      v-if="notice"
      :class="['page-notice', `page-notice--${notice.tone}`]"
      role="status"
      aria-live="polite"
    >
      {{ notice.message }}
    </p>

    <header class="page-header">
      <div>
        <h1 class="page-title">排队管理</h1>
        <p class="page-subtitle">当前服务</p>
      </div>
    </header>

    <div class="page-card page-card--hero queue-overview">
      <div class="queue-summary-grid">
        <div
          v-for="item in summaryItems"
          :key="item.label"
          class="queue-summary"
        >
          <span class="queue-summary__label">{{ item.label }}</span>
          <strong :class="['queue-summary__value', `queue-summary__value--${item.tone}`]">
            {{ item.value }}
          </strong>
        </div>
      </div>
    </div>

    <div class="page-card queue-panel">
      <div class="queue-actions" aria-label="排队操作">
        <button
          v-for="action in actionItems"
          :key="action.id"
          :class="[
            'queue-action',
            `queue-action--${action.tone}`,
            { 'queue-action--unavailable': isActionUnavailable(action.id) },
          ]"
          type="button"
          :aria-label="action.label"
          :aria-disabled="isActionUnavailable(action.id) ? 'true' : undefined"
          @click="handleAction(action.id)"
        >
          <span class="queue-action__icon">{{ action.icon }}</span>
          <span class="queue-action__label">{{ action.label }}</span>
        </button>
      </div>

      <div v-if="loading" class="empty-state">加载中…</div>

      <div v-else-if="queueItems.length" class="queue-list">
        <article
          v-for="item in queueItems"
          :key="item.number"
          :class="['queue-row', `queue-row--${item.tone}`]"
        >
          <div class="queue-row__number">{{ item.number }}</div>
          <div class="queue-row__body">
            <strong class="queue-row__customer">{{ item.customer }}</strong>
            <p class="queue-row__line">
              <span>订单：</span>
              <b>{{ item.order }}</b>
              <em>{{ item.quantity }}</em>
            </p>
            <p class="queue-row__line queue-row__line--note">
              <span>备注：</span>
              <mark>{{ item.note }}</mark>
            </p>
          </div>
          <span :class="['queue-row__status', `queue-row__status--${item.tone}`]">
            {{ item.status }}
          </span>
        </article>
      </div>
      <div v-else class="empty-state">
        <strong>当前没有排队记录</strong>
        <p>新增取号后，当前服务和等待队列会显示在这里。</p>
      </div>
    </div>

    <div
      v-if="isDialogOpen"
      class="queue-dialog"
      role="dialog"
      aria-modal="true"
      aria-label="新增取号"
      @click.self="closeAddDialog"
    >
      <form class="queue-dialog__card" @submit.prevent="submitNewTicket">
        <div class="queue-dialog__header">
          <div>
            <span>自动取号</span>
            <strong>{{ nextNumber }}</strong>
          </div>
          <button type="button" aria-label="关闭取号弹窗" @click="closeAddDialog">×</button>
        </div>

        <label class="queue-field">
          <span>顾客姓名</span>
          <input
            v-model="queueForm.customer"
            autocomplete="off"
            placeholder="例如：小陈"
          >
        </label>

        <label class="queue-field">
          <span>商品内容</span>
          <input
            v-model="queueForm.orderText"
            autocomplete="off"
            placeholder="例如：手工钥匙扣 ×2"
          >
        </label>

        <label class="queue-field">
          <span>备注项</span>
          <input
            v-model="queueForm.note"
            autocomplete="off"
            placeholder="例如：蓝色款"
          >
        </label>

        <p v-if="formError" class="queue-dialog__error" role="alert">{{ formError }}</p>

        <button class="queue-dialog__submit" type="submit">确认取号</button>
      </form>
    </div>
  </section>
</template>

<style scoped>
.queue-view {
  position: relative;
  display: block;
  min-height: 100%;
  background:
    linear-gradient(180deg, #f4fbff 0%, #f7fbff 22%, #ffffff 58%, #ffffff 100%);
}

.queue-view :deep(.page-header) {
  margin-bottom: 14px;
}

.queue-overview {
  padding: 14px;
  background: rgba(255, 255, 255, 0.95);
}

.queue-summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.queue-summary {
  min-width: 0;
  padding: 12px 8px;
  border: 1px solid rgba(80, 139, 220, 0.08);
  border-radius: 16px;
  background: linear-gradient(180deg, #f8fbff 0%, #eef6ff 100%);
  text-align: center;
}

.queue-summary__label {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 0.72rem;
  font-weight: 700;
  white-space: nowrap;
}

.queue-summary__value {
  display: block;
  color: var(--text-main);
  font-size: 0.95rem;
  font-weight: 800;
  line-height: 1.1;
  white-space: nowrap;
}

.queue-summary__value--primary {
  color: var(--primary);
  font-size: 1.18rem;
}

.queue-summary__value--success {
  color: #16a34a;
}

.queue-panel {
  margin-top: 14px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.96);
}

.queue-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 9px;
  width: 100%;
  margin: 0 auto;
}

.queue-action {
  display: grid;
  justify-items: center;
  gap: 7px;
  min-height: 64px;
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--text-main);
}

.queue-action__icon {
  display: grid;
  width: 44px;
  height: 44px;
  place-items: center;
  border: 1px solid rgba(126, 165, 220, 0.18);
  border-radius: 14px;
  background: linear-gradient(180deg, #f8fbff 0%, #eef6ff 100%);
  color: #4d89de;
  font-size: 1.25rem;
  font-weight: 500;
  line-height: 1;
}

.queue-action__label {
  color: var(--text-main);
  font-size: 0.68rem;
  font-weight: 800;
  white-space: nowrap;
}

.queue-action--call .queue-action__icon {
  background: linear-gradient(180deg, #effbf6 0%, #def6ea 100%);
  color: #16a34a;
}

.queue-action--done .queue-action__icon {
  background: linear-gradient(180deg, #f5f0ff 0%, #ece3ff 100%);
  color: #7c3aed;
}

.queue-action--danger .queue-action__icon {
  background: linear-gradient(180deg, #fff3f3 0%, #ffe8e8 100%);
  color: #ef4444;
}

.queue-action--unavailable {
  opacity: 0.56;
}

.queue-list {
  display: grid;
  gap: 9px;
  margin-top: 14px;
}

.queue-row {
  display: grid;
  grid-template-columns: 62px minmax(0, 1fr) auto;
  align-items: center;
  gap: 11px;
  width: 100%;
  margin: 0 auto;
  padding: 10px 12px;
  border: 1px solid rgba(105, 145, 198, 0.1);
  border-radius: 17px;
  background: #ffffff;
  box-shadow: 0 8px 20px rgba(66, 105, 153, 0.07);
}

.queue-row--completed,
.queue-row--cancelled {
  background: #f8fafc;
  box-shadow: none;
  opacity: 0.78;
}

.queue-row__number {
  display: grid;
  place-items: center;
  min-height: 58px;
  border-radius: 15px;
  background: linear-gradient(180deg, #edf6ff 0%, #f6faff 100%);
  color: var(--primary);
  font-size: 0.82rem;
  font-weight: 800;
  letter-spacing: 0.02em;
}

.queue-row__number::before {
  content: "☰";
  display: grid;
  width: 28px;
  height: 28px;
  place-items: center;
  margin-bottom: 4px;
  border-radius: 10px;
  background: #d8e8ff;
  color: #5a9bf3;
  font-size: 0.82rem;
  line-height: 1;
}

.queue-row--completed .queue-row__number,
.queue-row--cancelled .queue-row__number {
  background: #eef2f7;
  color: #7c8797;
}

.queue-row--completed .queue-row__number::before,
.queue-row--cancelled .queue-row__number::before {
  background: #e2e8f0;
  color: #94a3b8;
}

.queue-row__body {
  min-width: 0;
}

.queue-row__customer {
  display: block;
  margin-bottom: 3px;
  color: var(--text-main);
  font-size: 0.88rem;
  line-height: 1.15;
}

.queue-row__line {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 0;
  margin: 0;
  color: var(--text-muted);
  font-size: 0.72rem;
  line-height: 1.28;
  white-space: nowrap;
}

.queue-row__line b {
  overflow: hidden;
  color: #29405d;
  font-weight: 700;
  text-overflow: ellipsis;
}

.queue-row__line em {
  color: #29405d;
  font-style: normal;
  font-weight: 800;
}

.queue-row__line--note {
  margin-top: 2px;
}

.queue-row__line mark {
  display: inline-flex;
  padding: 2px 7px;
  border: 0;
  border-radius: 999px;
  background: #eaf3ff;
  color: var(--primary);
  font-size: 0.68rem;
  font-weight: 700;
}

.queue-row--completed .queue-row__line mark,
.queue-row--cancelled .queue-row__line mark {
  background: #eef2f7;
  color: #64748b;
}

.queue-row__status {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 54px;
  padding: 5px 8px;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 800;
  white-space: nowrap;
}

.queue-row__status--serving {
  background: #e2f7ed;
  color: #16a46b;
}

.queue-row__status--waiting {
  background: #fff1e4;
  color: #f07c22;
}

.queue-row__status--completed,
.queue-row__status--cancelled {
  background: #e5e7eb;
  color: #6b7280;
}

.queue-dialog {
  position: absolute;
  inset: 0;
  z-index: 20;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(17, 37, 61, 0.28);
  backdrop-filter: blur(10px);
}

.queue-dialog__card {
  width: min(320px, 100%);
  padding: 18px;
  border: 1px solid rgba(126, 165, 220, 0.18);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 24px 60px rgba(18, 30, 52, 0.22);
}

.queue-dialog__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}

.queue-dialog__header span {
  display: block;
  margin-bottom: 4px;
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 700;
}

.queue-dialog__header strong {
  color: var(--primary);
  font-size: 1.55rem;
  line-height: 1;
}

.queue-dialog__header button {
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

.queue-field {
  display: grid;
  gap: 7px;
  margin-top: 12px;
}

.queue-field span {
  color: var(--text-main);
  font-size: 0.76rem;
  font-weight: 800;
}

.queue-field input {
  width: 100%;
  padding: 12px 13px;
  border: 1px solid rgba(126, 165, 220, 0.2);
  border-radius: 14px;
  outline: 0;
  background: #f8fbff;
  color: var(--text-main);
  font-size: 0.82rem;
}

.queue-field input:focus {
  border-color: rgba(45, 115, 219, 0.45);
  box-shadow: 0 0 0 3px rgba(45, 115, 219, 0.08);
}

.queue-dialog__error {
  margin: 10px 0 0;
  color: #ef4444;
  font-size: 0.72rem;
  font-weight: 700;
}

.queue-dialog__submit {
  width: 100%;
  min-height: 44px;
  margin-top: 16px;
  padding: 12px;
  border: 0;
  border-radius: 15px;
  background: linear-gradient(135deg, #6fbaff 0%, #2d73db 100%);
  color: #ffffff;
  box-shadow: 0 12px 24px rgba(45, 115, 219, 0.22);
  font-size: 0.86rem;
  font-weight: 900;
}

@media (max-width: 420px) {
  .queue-summary-grid {
    gap: 8px;
  }

  .queue-summary {
    padding: 12px 8px;
  }

  .queue-row {
    grid-template-columns: 58px minmax(0, 1fr) auto;
    gap: 9px;
    padding: 10px 11px;
  }

  .queue-row__status {
    min-width: 50px;
    padding: 5px 7px;
  }

  .queue-action__icon {
    width: 40px;
    height: 40px;
    border-radius: 13px;
  }

  .queue-action__label {
    font-size: 0.68rem;
  }
}

@media (max-width: 380px) {
  .queue-summary-grid {
    grid-template-columns: 1fr;
  }

  .queue-summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    text-align: left;
  }

  .queue-summary__label {
    margin-bottom: 0;
  }

  .queue-row {
    grid-template-columns: 54px minmax(0, 1fr);
    align-items: start;
  }

  .queue-row__number {
    min-height: 54px;
  }

  .queue-row__status {
    grid-column: 2;
    justify-self: start;
    min-width: 0;
    margin-top: 4px;
  }

  .queue-row__line {
    white-space: normal;
  }
}
</style>
