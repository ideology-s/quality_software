<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { RouterView } from 'vue-router'
import { useRoute } from 'vue-router'
import BottomNav from './BottomNav.vue'
import StatusBar from './StatusBar.vue'

const route = useRoute()
const contentRef = ref(null)
const shouldShowNav = computed(() => !route.meta.hideNav)

watch(
  () => route.fullPath,
  async () => {
    await nextTick()
    contentRef.value?.scrollTo({ top: 0 })
  },
)
</script>

<template>
  <div class="phone-page">
    <div class="phone-device">
      <div class="phone-screen">
        <div class="phone-screen__notch" aria-hidden="true"></div>
        <StatusBar />
        <div ref="contentRef" class="phone-screen__content">
          <RouterView :key="route.fullPath" />
        </div>
        <BottomNav v-if="shouldShowNav" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.phone-page {
  min-height: 100vh;
  padding: 18px;
  background:
    radial-gradient(circle at top, rgba(224, 236, 250, 0.9) 0%, rgba(238, 244, 251, 1) 45%, rgba(233, 240, 248, 1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.phone-device {
  width: min(390px, calc(100vw - 28px));
  height: min(844px, calc(100vh - 36px));
  border: 12px solid #1f1f1f;
  border-radius: 40px;
  background: #1f1f1f;
  box-shadow:
    0 30px 70px rgba(18, 30, 52, 0.24),
    0 8px 24px rgba(18, 30, 52, 0.12);
  position: relative;
  overflow: hidden;
}

.phone-screen {
  width: 100%;
  height: 100%;
  border-radius: 28px;
  background: linear-gradient(180deg, #f4fbff 0%, #ffffff 22%, #ffffff 100%);
  position: relative;
  overflow: hidden;
}

.phone-screen__notch {
  position: absolute;
  top: 0;
  left: 50%;
  width: 150px;
  height: 26px;
  border-radius: 0 0 20px 20px;
  transform: translateX(-50%);
  background: #1f1f1f;
  z-index: 4;
}

.phone-screen__content {
  position: absolute;
  inset: 44px 0 0;
  z-index: 2;
  background: linear-gradient(180deg, #f4fbff 0%, #ffffff 22%, #ffffff 100%);
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
}

.phone-screen__content::-webkit-scrollbar {
  display: none;
}

@media (max-width: 540px) {
  .phone-page {
    padding: 10px;
  }

  .phone-device {
    width: min(100vw - 20px, 390px);
    height: min(100vh - 20px, 844px);
    border-width: 10px;
  }
}
</style>
