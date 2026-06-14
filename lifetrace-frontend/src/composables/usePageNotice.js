import { onBeforeUnmount, ref } from 'vue'

export function usePageNotice() {
  const notice = ref(null)
  let timer = null

  function showNotice(message, tone = 'success') {
    notice.value = { message, tone }
    window.clearTimeout(timer)
    timer = window.setTimeout(() => {
      notice.value = null
    }, 2400)
  }

  onBeforeUnmount(() => {
    window.clearTimeout(timer)
  })

  return {
    notice,
    showNotice,
  }
}
