<script setup>
import { nextTick, ref } from 'vue'
import {
  CirclePlus,
  Microphone,
  Search,
  Star,
  Sunny,
} from '@element-plus/icons-vue'

const initialMessages = [
  {
    id: 1,
    role: 'user',
    content: '你好',
  },
  {
    id: 2,
    role: 'assistant',
    content: '你好！很高兴见到你，有什么我可以帮忙的吗？',
    thinking: '已思考（用时 2 秒）',
  },
]

const messages = ref([...initialMessages])
const inputValue = ref('')
const chatBodyRef = ref(null)
const chatEndRef = ref(null)

function resetChat() {
  messages.value = [...initialMessages]
  inputValue.value = ''
}

async function sendMessage() {
  const question = inputValue.value.trim()

  if (!question) {
    return
  }

  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: question,
  })

  inputValue.value = ''

  messages.value.push({
    id: Date.now() + 1,
    role: 'assistant',
    content: '我可以根据你的出摊日志、日程、商品库存和排队情况，帮你整理经营建议。比如：优先补充库存不足商品，避开日程冲突，并把高利润商品安排在客流高峰时段。',
    thinking: '已思考（用时 1 秒）',
  })

  await nextTick()
  requestAnimationFrame(() => {
    chatEndRef.value?.scrollIntoView({ block: 'end', behavior: 'smooth' })
  })
}
</script>

<template>
  <section class="page-view ai-view">
    <header class="ai-top">
      <h1>AI助手</h1>
    </header>

    <main ref="chatBodyRef" class="ai-chat">
      <article
        v-for="message in messages"
        :key="message.id"
        :class="['ai-message', `ai-message--${message.role}`]"
      >
        <template v-if="message.role === 'assistant'">
          <div class="assistant-thinking">
            <span class="assistant-icon">
              <el-icon><Sunny /></el-icon>
            </span>
            <span>{{ message.thinking }}</span>
            <b>⌄</b>
          </div>
          <div class="assistant-bubble">
            {{ message.content }}
          </div>
        </template>

        <div v-else class="user-bubble">
          {{ message.content }}
        </div>
      </article>
      <div ref="chatEndRef" class="chat-end" aria-hidden="true"></div>
    </main>

    <form class="ai-composer" @submit.prevent="sendMessage">
      <input
        v-model="inputValue"
        autocomplete="off"
        placeholder="发消息或按住说话"
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
        <button class="composer-round" type="submit" aria-label="发送或语音">
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
  text-align: center;
}

.ai-top h1 {
  margin: 0;
  color: var(--text-main);
  font-size: 1.55rem;
  font-weight: 900;
  line-height: 1.1;
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
  color: #b4beca;
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
  width: 34px;
  height: 34px;
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
    gap: 7px;
  }

  .composer-pill {
    padding: 6px 8px;
    font-size: 0.66rem;
  }
}
</style>
