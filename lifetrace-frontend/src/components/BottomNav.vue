<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import {
  Calendar,
  ChatDotRound,
  Memo,
  ShoppingBag,
  User,
} from '@element-plus/icons-vue'

const route = useRoute()

const navItems = [
  { label: '出摊日志', to: '/health', icon: Memo },
  { label: '排队', to: '/queue', icon: User },
  { label: 'AI助手', to: '/ai', icon: ChatDotRound, center: true },
  { label: '商品', to: '/products', icon: ShoppingBag },
  { label: '日程', to: '/schedule', icon: Calendar },
]

const currentPath = computed(() => route.path)
</script>

<template>
  <nav class="bottom-nav" aria-label="主导航">
    <RouterLink
      v-for="item in navItems"
      :key="item.to"
      :to="item.to"
      :aria-label="item.label"
      :aria-current="currentPath === item.to ? 'page' : undefined"
      :class="[
        'bottom-nav__item',
        { 'bottom-nav__item--active': currentPath === item.to },
        { 'bottom-nav__item--center': item.center },
      ]"
    >
      <span v-if="item.center" class="bottom-nav__center-button">
        <span class="bottom-nav__center-spark" aria-hidden="true">✦</span>
        <span class="bottom-nav__center-core">AI</span>
        <span class="bottom-nav__center-badge">助手</span>
      </span>
      <span v-else class="bottom-nav__icon">
        <span class="bottom-nav__icon-blob" aria-hidden="true"></span>
        <el-icon>
          <component :is="item.icon" />
        </el-icon>
      </span>
      <span v-if="!item.center" class="bottom-nav__label">{{ item.label }}</span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.bottom-nav {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 6;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  align-items: center;
  padding: 8px 14px 7px;
  min-height: 74px;
  background: rgba(255, 255, 255, 0.96);
  border-top: 1px solid rgba(115, 154, 216, 0.12);
  box-shadow: 0 -6px 18px rgba(77, 116, 169, 0.05);
  backdrop-filter: blur(14px);
}

.bottom-nav__item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-height: 54px;
  color: #7d8798;
  text-decoration: none;
  border-radius: 16px;
  transition: color 0.2s ease, transform 0.2s ease;
}

.bottom-nav__item--active {
  color: #2d73db;
}

.bottom-nav__icon {
  position: relative;
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  font-size: 1.42rem;
}

.bottom-nav__icon :deep(.el-icon) {
  position: relative;
  z-index: 1;
}

.bottom-nav__icon-blob {
  position: absolute;
  right: 1px;
  bottom: 2px;
  width: 18px;
  height: 18px;
  border-radius: 7px;
  background: rgba(124, 194, 255, 0);
  transition: background-color 0.2s ease;
}

.bottom-nav__label {
  font-size: 0.7rem;
  font-weight: 600;
  line-height: 1;
}

.bottom-nav__item--center {
  transform: translateY(-12px);
}

.bottom-nav__item--center:hover {
  transform: translateY(-14px);
}

.bottom-nav__item--active:not(.bottom-nav__item--center) .bottom-nav__icon-blob {
  background: rgba(124, 194, 255, 0.45);
}

.bottom-nav__center-button {
  position: relative;
  display: grid;
  place-items: center;
  width: 56px;
  height: 56px;
  border-radius: 999px;
  border-bottom-left-radius: 14px;
  background: linear-gradient(135deg, #7dd8ff 0%, #41a3f4 100%);
  color: #ffffff;
  box-shadow: 0 8px 20px rgba(65, 163, 244, 0.28);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.bottom-nav__center-core {
  font-size: 1rem;
  font-weight: 800;
  letter-spacing: 0.02em;
}

.bottom-nav__center-spark {
  position: absolute;
  top: 8px;
  left: 10px;
  font-size: 0.62rem;
  opacity: 0.92;
}

.bottom-nav__center-badge {
  position: absolute;
  top: -3px;
  right: -11px;
  padding: 2px 6px;
  border-radius: 999px 999px 999px 4px;
  border: 1.5px solid #ffffff;
  background: linear-gradient(135deg, #a789ff 0%, #7d55ea 100%);
  box-shadow: 0 4px 10px rgba(125, 85, 234, 0.24);
  font-size: 0.58rem;
  font-weight: 700;
  line-height: 1;
}

.bottom-nav__item--active.bottom-nav__item--center .bottom-nav__center-button {
  background: linear-gradient(135deg, #82e0ff 0%, #2f8ef0 100%);
  box-shadow: 0 10px 22px rgba(47, 142, 240, 0.32);
}

@media (max-width: 420px) {
  .bottom-nav {
    padding-left: 10px;
    padding-right: 10px;
  }

  .bottom-nav__center-button {
    width: 54px;
    height: 54px;
  }
}

@media (max-width: 380px) {
  .bottom-nav {
    padding-left: 8px;
    padding-right: 8px;
  }

  .bottom-nav__label {
    font-size: 0.66rem;
  }

  .bottom-nav__center-button {
    width: 50px;
    height: 50px;
  }

  .bottom-nav__center-badge {
    right: -6px;
    font-size: 0.54rem;
  }
}
</style>
