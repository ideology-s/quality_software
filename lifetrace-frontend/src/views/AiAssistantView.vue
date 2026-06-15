<script setup>
import { nextTick, ref } from 'vue'
import {
  CirclePlus,
  Microphone,
  Search,
  Star,
  Sunny,
} from '@element-plus/icons-vue'
import { chatWithAI, getTodaySummary } from '../api'

const initialMessages = [
  {
    id: 1,
    role: 'user',
    content: '你好',
  },
  {
    id: 2,
    role: 'assistant',
    content: '你好！很高兴见到你，有什么我可以帮忙的吗？我是你的校园小摊 AI 助手。',
    thinking: '',
  },
]

const messages = ref([...initialMessages])
const inputValue = ref('')
const sending = ref(false)
const chatBodyRef = ref(null)
const chatEndRef = ref(null)

function resetChat() {
  messages.value = [...initialMessages]
  inputValue.value = ''
}

function scrollToBottom() {
  requestAnimationFrame(() => {
    chatEndRef.value?.scrollIntoView({ block: 'end', behavior: 'smooth' })
  })
}

async function sendMessage() {
  const question = inputValue.value.trim()

  if (!question || sending.value) return

  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: question,
  })

  inputValue.value = ''
  sending.value = true

  messages.value.push({
    id: Date.now() + 1,
    role: 'assistant',
    content: '',
    thinking: '思考中...',
    loading: true,
  })

  await nextTick()
  scrollToBottom()

  try {
    const res = await chatWithAI(question)
    const data = res.data.data
    messages.value = messages.value.filter(m => !m.loading)
    messages.value.push({
      id: Date.now() + 2,
      role: 'assistant',
      content: data.content || 'AI 暂时无法回答这个问题。',
      thinking: data.thinking || '',
    })
  } catch (e) {
    messages.value = messages.value.filter(m => !m.loading)
    messages.value.push({
      id: Date.now() + 2,
      role: 'assistant',
      content: '抱歉，AI 服务暂时不可用。请检查后端服务是否正常运行，以及 OpenAI API Key 是否已配置。',
      thinking: '',
    })
  } finally {
    sending.value = false
    await nextTick()
    scrollToBottom()
  }
}

async function fetchSummary() {
  sending.value = true
  try {
    const res = await getTodaySummary()
    const data = res.data.data
    const adviceText = data.advice && data.advice.length > 0
      ? data.advice.join('；')
      : '当前各项指标正常。'

    messages.value.push({
      id: Date.now(),
      role: 'user',
      content: '帮我总结一下今天的经营情况',
    })
    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: `📊 **今日综合分析（${data.date}）**

**出摊**：共 ${data.stall?.count || 0} 次，收入 ¥${data.stall?.total_income || 0}，利润 ¥${data.stall?.total_profit || 0}
**天气**：${data.weather?.has_data ? `${data.weather.temperature}°C，${data.weather.weather_type}，${data.weather.is_rainy ? '有雨' : '无雨'}，风力 ${data.weather.wind_level} 级` : '暂无天气数据'}
**日程**：未完成 ${data.schedule?.unfinished_count || 0} 项 / 共 ${data.schedule?.total_count || 0} 项
**商品**：${data.product?.total_count || 0} 种商品，${data.product?.low_stock_count || 0} 种库存不足，${data.product?.sold_out_count || 0} 种已售空
**排队**：${data.queue?.waiting_count || 0} 人等待，${data.queue?.serving_count || 0} 人服务中

💡 **建议**：${adviceText}`,
      thinking: '已分析今日数据',
    })
  } catch (e) {
    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: '抱歉，暂时无法获取经营数据。请检查后端服务是否正常。',
      thinking: '',
    })
  } finally {
    sending.value = false
    await nextTick()
    scrollToBottom()
  }
}
</script>

<template>
  <section class="page-view ai-view">
    <header class="ai-top">
      <h1>AI助手</h1>
      <div class="ai-top-actions">
        <button class="ai-reset" type="button" @click="fetchSummary" :disabled="sending">今日总结</button>
        <button class="ai-reset" type="button" @click="resetChat">新对话</button>
      </div>
    </header>

    <main ref="chatBodyRef" class="ai-chat" aria-live="polite">
      <article
        v-for="message in messages"
        :key="message.id"
        :class="['ai-message', `ai-message--${message.role}`]"
      >
        <template v-if="message.role === 'assistant'">
          <div v-if="message.thinking" class="assistant-thinking">
            <span class="assistant-icon">
              <el-icon><Sunny /></el-icon>
            </span>
            <span>{{ message.thinking }}</span>
            <b>⌄</b>
          </div>
          <div v-if="message.loading" class="assistant-bubble assistant-bubble--loading">
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>
          </div>
          <div v-else class="assistant-bubble" v-html="message.content.replace(/\n/g, '<br>')">
          </div>
        </template>

        <div v-else class="user-bubble">
          {{ message.content }}
        </div>
      </article>
      <div ref="chatEndRef" class="chat-end" aria-hidden="true"></div>
    </main>

    <form class="ai-composer" @submit.prevent="sendMessage">
      <label class="sr-only" for="ai-message-input">给 AI 助手发送消息</label>
        <input
        id="ai-message-input"
        v-model="inputValue"
        autocomplete="off"
        placeholder="发消息或按住说话"
        :disabled="sending"
      >
      <div class="composer-tools">
        <button class="composer-pill" type="button">
          <el-icon><Star /></el-icon>
          深度思考
        </button>
        <button class="composer-pill" type="button">
          <el-icon><Search /></el-icon>
          智能搜索
        </button>
        <span class="composer-spacer"></span>
        <button class="composer-round" type="button" aria-label="添加">
          <el-icon><CirclePlus /></el-icon>
        </button>
        <button class="composer-round" type="submit" aria-label="发送消息" :disabled="!inputValue.trim() || sending">
          <el-icon><Microphone /></el-icon>
        </button>
      </div>
    </form>
  </section>
</template>

<style scoped>
.ai-view {
  position: relative;
  height: 100%;
  min-height: 0;
  overflow: hidden;
  padding: 40px var(--page-padding) 0;
  background:
    radial-gradient(circle at 50% 0%, rgba(225, 244, 255, 0.85) 0%, rgba(255, 255, 255, 0) 34%),
    linear-gradient(180deg, #f8fcff 0%, #ffffff 56%, #ffffff 100%);
}

.ai-top {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.ai-top h1 {
  margin: 0;
  color: var(--text-main);
  font-size: 1.55rem;
  font-weight: 900;
  line-height: 1.1;
}

.ai-top-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 8px;
}

.ai-reset {
  padding: 7px 14px;
  border: 1px solid rgba(45, 115, 219, 0.2);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  color: var(--primary);
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
}

.ai-reset:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ai-chat {
  position: absolute;
  top: 122px;
  left: var(--page-padding);
  right: var(--page-padding);
  bottom: 226px;
  display: grid;
  align-content: start;
  gap: 34px;
  margin-top: 0;
  overflow-y: auto;
  padding: 0 0 24px;
  scrollbar-width: none;
}

.chat-end {
  height: 1px;
}

.ai-chat::-webkit-scrollbar {
  display: none;
}

.ai-message {
  display: grid;
}

.ai-message--user {
  justify-items: end;
}

.user-bubble {
  max-width: 46%;
  padding: 15px 18px;
  border-radius: 20px 20px 6px 20px;
  background: linear-gradient(180deg, #eef6ff 0%, #e6f1ff 100%);
  color: var(--text-main);
  font-size: 0.94rem;
  font-weight: 800;
  box-shadow: inset 0 -8px 16px rgba(45, 115, 219, 0.04);
}

.assistant-thinking {
  display: inline-grid;
  grid-template-columns: 36px auto 12px;
  align-items: center;
  gap: 10px;
  justify-self: start;
  margin-bottom: 14px;
  color: #7d8798;
  font-size: 0.78rem;
  font-weight: 800;
}

.assistant-icon {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  border-radius: 50%;
  background: linear-gradient(135deg, #e8f4ff 0%, #d7ecff 100%);
  color: var(--primary);
}

.assistant-bubble {
  justify-self: start;
  max-width: 66%;
  padding: 15px 18px;
  border: 1px solid rgba(105, 145, 198, 0.14);
  border-radius: 18px 18px 18px 6px;
  background: rgba(255, 255, 255, 0.96);
  color: var(--text-main);
  box-shadow: 0 10px 24px rgba(66, 105, 153, 0.07);
  font-size: 0.9rem;
  line-height: 1.7;
  font-weight: 700;
  white-space: pre-wrap;
}

.assistant-bubble--loading {
  display: flex;
  gap: 6px;
  align-items: center;
  padding: 18px 22px;
}

.loading-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary);
  animation: dotPulse 1.2s infinite ease-in-out;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dotPulse {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.ai-composer {
  position: absolute;
  left: 10px;
  right: 10px;
  bottom: 96px;
  z-index: 5;
  padding: 18px 18px 14px;
  border: 1px solid rgba(105, 145, 198, 0.12);
  border-radius: 26px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 -4px 26px rgba(66, 105, 153, 0.12);
  backdrop-filter: blur(12px);
}

.ai-composer input {
  width: 100%;
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--text-main);
  font-size: 0.92rem;
  font-weight: 700;
}

.ai-composer input::placeholder {
  color: #64748b;
}

.composer-tools {
  display: grid;
  grid-template-columns: auto auto 1fr 36px 36px;
  align-items: center;
  gap: 9px;
  margin-top: 18px;
}

.composer-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  min-height: 34px;
  padding: 7px 10px;
  border: 1px solid rgba(45, 115, 219, 0.24);
  border-radius: 999px;
  background: #eef5ff;
  color: var(--primary);
  font-size: 0.7rem;
  font-weight: 900;
  white-space: nowrap;
}

.composer-round {
  display: grid;
  width: 44px;
  height: 44px;
  place-items: center;
  border: 1.6px solid #111827;
  border-radius: 50%;
  background: #ffffff;
  color: #111827;
  font-size: 1.1rem;
}

@media (max-width: 420px) {
  .ai-view {
    padding-top: 38px;
  }

  .ai-chat {
    top: 116px;
    bottom: 222px;
    gap: 30px;
  }

  .assistant-bubble {
    max-width: 72%;
  }

  .composer-tools {
    grid-template-columns: auto auto 1fr 44px 44px;
    gap: 7px;
  }

  .composer-pill {
    padding: 6px 8px;
    font-size: 0.66rem;
  }
}

@media (max-width: 380px) {
  .ai-reset {
    padding: 6px 8px;
    font-size: 0.68rem;
  }

  .ai-chat {
    left: 18px;
    right: 18px;
  }

  .ai-composer {
    left: 8px;
    right: 8px;
    padding: 16px 14px 12px;
    border-radius: 22px;
  }

  .composer-tools {
    grid-template-columns: 1fr 1fr 44px 44px;
  }

  .composer-spacer {
    display: none;
  }

  .composer-pill {
    justify-content: center;
    min-width: 0;
  }

  .user-bubble {
    max-width: 70%;
  }

  .assistant-bubble {
    max-width: 82%;
  }
}
</style>
