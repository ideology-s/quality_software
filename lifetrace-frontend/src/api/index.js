import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

// ===== 出摊日志 =====

export function getStallLogs() {
  return api.get('/stall-logs')
}

export function createStallLog(data) {
  return api.post('/stall-logs', data)
}

export function updateStallLog(logId, data) {
  return api.put(`/stall-logs/${logId}`, data)
}

export function deleteStallLog(logId) {
  return api.delete(`/stall-logs/${logId}`)
}

export function getWeeklySummary() {
  return api.get('/stall-logs/weekly-summary')
}

// ===== 天气 =====

export function setWeather(data) {
  return api.post('/weather', data)
}

export function getTodayWeather() {
  return api.get('/weather/today')
}

// ===== 出摊建议 =====

export function getStallAdvice(data) {
  return api.post('/stall-advice', data)
}

// ===== 日程 =====

export function getSchedules() {
  return api.get('/schedules')
}

export function getSchedulesByDate(date) {
  return api.get(`/schedules/date/${date}`)
}

export function getScheduleSummary() {
  return api.get('/schedules/summary')
}

export function createSchedule(data) {
  return api.post('/schedules', data)
}

export function updateSchedule(scheduleId, data) {
  return api.put(`/schedules/${scheduleId}`, data)
}

export function deleteSchedule(scheduleId) {
  return api.delete(`/schedules/${scheduleId}`)
}

// ===== 商品 =====

export function getProducts() {
  return api.get('/products')
}

export function getProduct(productId) {
  return api.get(`/products/${productId}`)
}

export function getProductSummary() {
  return api.get('/products/summary')
}

export function createProduct(data) {
  return api.post('/products', data)
}

export function updateProduct(productId, data) {
  return api.put(`/products/${productId}`, data)
}

export function deleteProduct(productId) {
  return api.delete(`/products/${productId}`)
}

export function sellProduct(productId, quantity) {
  return api.post(`/products/${productId}/sell`, { quantity })
}

// ===== 排队 =====

export function getQueueList() {
  return api.get('/queue')
}

export function getQueueSummary() {
  return api.get('/queue/summary')
}

export function takeNumber(data) {
  return api.post('/queue', data)
}

export function serveNext(number) {
  return api.put(`/queue/${number}/serve`)
}

export function completeOrder(number) {
  return api.put(`/queue/${number}/complete`)
}

export function cancelOrder(number) {
  return api.put(`/queue/${number}/cancel`)
}

export function deleteQueueOrder(number) {
  return api.delete(`/queue/${number}`)
}

// ===== AI 助手 =====

export function chatWithAI(message) {
  return api.post('/ai/chat', { message })
}

export function getTodaySummary() {
  return api.get('/summary/today')
}

export default api
