<template>
  <header class="status-bar" aria-label="手机状态栏">
    <span class="status-bar__time">11:24</span>
    <div class="status-bar__right">
      <span class="status-bar__network">4G</span>
      <div class="status-bar__signal" aria-hidden="true">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
      <div class="status-bar__battery" aria-label="电量 72%">
        <span class="status-bar__battery-level">72</span>
        <span class="status-bar__battery-cap"></span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.status-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 3;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 8px 22px 0;
  height: 44px;
  color: #101828;
  font-weight: 600;
}

.status-bar__time {
  font-size: 0.98rem;
  letter-spacing: 0.02em;
  line-height: 1;
}

.status-bar__right {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  line-height: 1;
  color: #4a5568;
}

.status-bar__signal {
  display: flex;
  align-items: end;
  gap: 2px;
  height: 14px;
}

.status-bar__signal span {
  display: block;
  width: 2px;
  background: currentColor;
  border-radius: 999px;
}

.status-bar__signal span:nth-child(1) {
  height: 5px;
}

.status-bar__signal span:nth-child(2) {
  height: 8px;
}

.status-bar__signal span:nth-child(3) {
  height: 11px;
}

.status-bar__signal span:nth-child(4) {
  height: 14px;
}

.status-bar__battery {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 31px;
  height: 16px;
  padding: 0 5px;
  border: 1.8px solid currentColor;
  border-radius: 5px;
  font-size: 0.66rem;
  line-height: 1;
}

.status-bar__battery-cap {
  position: absolute;
  right: -4px;
  width: 3px;
  height: 6px;
  border-radius: 0 2px 2px 0;
  background: currentColor;
}
</style>
