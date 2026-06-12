<script setup>
import { computed, reactive, ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

const products = ref([
  {
    id: 1,
    name: '手工钥匙扣',
    price: 15,
    cost: 12,
    stock: 86,
    sold: 12,
    image: '',
    icon: '☁',
    theme: 'sky',
  },
  {
    id: 2,
    name: '零食包',
    price: 8,
    cost: 6.8,
    stock: 7,
    sold: 18,
    image: '',
    icon: '好吃',
    theme: 'snack',
  },
  {
    id: 3,
    name: '二手教材',
    price: 20,
    cost: 20,
    stock: 0,
    sold: 10,
    image: '',
    icon: '高等数学',
    theme: 'book',
  },
])

const isDialogOpen = ref(false)
const editingId = ref(null)
const formError = ref('')

const productForm = reactive({
  name: '',
  price: '',
  stock: '',
  cost: '',
  image: '',
})

const productStats = computed(() => {
  const income = products.value.reduce((sum, product) => sum + product.price * product.sold, 0)
  const profit = products.value.reduce(
    (sum, product) => sum + Math.max(product.price - product.cost, 0) * product.sold,
    0,
  )

  return [
    { label: '今日收入', value: `¥${Math.round(income)}`, icon: '¥' },
    { label: '今日利润', value: `¥${Math.round(profit)}`, icon: '▥' },
  ]
})

const dialogTitle = computed(() => (editingId.value ? '修改商品' : '新增商品'))

function getProductStatus(product) {
  if (product.stock < 10) {
    return {
      label: '库存不足',
      tone: 'warning',
    }
  }

  return {
    label: '库存正常',
    tone: 'normal',
  }
}

function getProductProfit(product) {
  return Math.round(Math.max(product.price - product.cost, 0) * product.sold)
}

function resetForm() {
  productForm.name = ''
  productForm.price = ''
  productForm.stock = ''
  productForm.cost = ''
  productForm.image = ''
  formError.value = ''
}

function openAddDialog() {
  editingId.value = null
  resetForm()
  isDialogOpen.value = true
}

function openEditDialog(product) {
  editingId.value = product.id
  productForm.name = product.name
  productForm.price = String(product.price)
  productForm.stock = String(product.stock)
  productForm.cost = String(product.cost)
  productForm.image = product.image
  formError.value = ''
  isDialogOpen.value = true
}

function closeDialog() {
  isDialogOpen.value = false
  formError.value = ''
}

function handleImageUpload(event) {
  const file = event.target.files?.[0]

  if (!file) {
    return
  }

  const reader = new FileReader()
  reader.onload = () => {
    productForm.image = String(reader.result)
  }
  reader.readAsDataURL(file)
}

function submitProduct() {
  const price = Number(productForm.price)
  const stock = Number.parseInt(productForm.stock, 10)
  const cost = Number(productForm.cost)

  if (!productForm.name.trim() || Number.isNaN(price) || Number.isNaN(stock) || Number.isNaN(cost)) {
    formError.value = '请完整填写商品名、售价、库存和成本价'
    return
  }

  if (price < 0 || stock < 0 || cost < 0) {
    formError.value = '售价、库存和成本价不能小于 0'
    return
  }

  const payload = {
    name: productForm.name.trim(),
    price,
    stock,
    cost,
    image: productForm.image,
  }

  if (editingId.value) {
    const index = products.value.findIndex((product) => product.id === editingId.value)

    if (index !== -1) {
      products.value[index] = {
        ...products.value[index],
        ...payload,
      }
    }
  } else {
    products.value.unshift({
      id: Date.now(),
      sold: 0,
      icon: productForm.name.trim().slice(0, 2),
      theme: 'custom',
      ...payload,
    })
  }

  closeDialog()
}

function deleteProduct() {
  if (!editingId.value) {
    return
  }

  products.value = products.value.filter((product) => product.id !== editingId.value)
  closeDialog()
}
</script>

<template>
  <section class="page-view products-view">
    <header class="page-header products-header">
      <div>
        <h1 class="page-title">商品管理</h1>
        <p class="page-subtitle">今日经营概览</p>
      </div>
      <button class="add-product" type="button" @click="openAddDialog">
        <el-icon><Plus /></el-icon>
        <span>添加商品</span>
      </button>
    </header>

    <div class="page-card product-stats">
      <div
        v-for="stat in productStats"
        :key="stat.label"
        class="product-stat"
      >
        <span class="product-stat__icon">{{ stat.icon }}</span>
        <div>
          <span class="product-stat__label">{{ stat.label }}</span>
          <strong>{{ stat.value }}</strong>
        </div>
      </div>
    </div>

    <div class="product-section-title">
      <h2>商品列表</h2>
      <span>共 {{ products.length }} 件商品</span>
    </div>

    <div class="product-list">
      <article
        v-for="product in products"
        :key="product.id"
        class="product-card"
        role="button"
        tabindex="0"
        @click="openEditDialog(product)"
        @keydown.enter="openEditDialog(product)"
      >
        <div :class="['product-card__cover', `product-card__cover--${product.theme}`]">
          <img
            v-if="product.image"
            :src="product.image"
            :alt="product.name"
          >
          <span v-else>{{ product.icon }}</span>
        </div>
        <div class="product-card__content">
          <div class="product-card__top">
            <h3>{{ product.name }}</h3>
            <span :class="['product-card__status', `product-card__status--${getProductStatus(product).tone}`]">
              {{ getProductStatus(product).label }}
            </span>
          </div>
          <div class="product-metrics">
            <div>
              <span>售价</span>
              <strong>¥{{ product.price }}</strong>
            </div>
            <div>
              <span>库存</span>
              <strong :class="{ 'is-warning': product.stock < 10 }">
                {{ product.stock }}
              </strong>
            </div>
            <div>
              <span>今日已售</span>
              <strong>{{ product.sold }}</strong>
            </div>
            <div>
              <span>今日利润</span>
              <strong>¥{{ getProductProfit(product) }}</strong>
            </div>
          </div>
        </div>
      </article>
    </div>

    <Teleport to=".phone-screen">
      <div
        v-if="isDialogOpen"
        class="product-modal"
        role="dialog"
        aria-modal="true"
        :aria-label="dialogTitle"
        @click.self="closeDialog"
      >
        <form class="product-modal__card" @submit.prevent="submitProduct">
          <div class="product-modal__header">
            <div>
              <span>{{ editingId ? '编辑库存信息' : '录入新商品' }}</span>
              <strong>{{ dialogTitle }}</strong>
            </div>
            <button type="button" @click="closeDialog">×</button>
          </div>

          <label class="product-field">
            <span>商品名</span>
            <input
              v-model="productForm.name"
              autocomplete="off"
              placeholder="例如：手工钥匙扣"
            >
          </label>

          <div class="product-field-grid">
            <label class="product-field">
              <span>售价</span>
              <input
                v-model="productForm.price"
                inputmode="decimal"
                placeholder="15"
              >
            </label>
            <label class="product-field">
              <span>库存</span>
              <input
                v-model="productForm.stock"
                inputmode="numeric"
                placeholder="86"
              >
            </label>
          </div>

          <label class="product-field">
            <span>成本价</span>
            <input
              v-model="productForm.cost"
              inputmode="decimal"
              placeholder="12"
            >
          </label>

          <label class="product-upload">
            <span class="product-upload__preview">
              <img
                v-if="productForm.image"
                :src="productForm.image"
                alt="商品图片预览"
              >
              <b v-else>上传图片</b>
            </span>
            <input
              accept="image/*"
              type="file"
              @change="handleImageUpload"
            >
          </label>

          <p v-if="formError" class="product-modal__error">{{ formError }}</p>

          <div :class="['product-modal__actions', { 'product-modal__actions--edit': editingId }]">
            <button
              v-if="editingId"
              class="product-modal__delete"
              type="button"
              @click="deleteProduct"
            >
              删除商品
            </button>
            <button class="product-modal__submit" type="submit">
              {{ editingId ? '保存修改' : '确认添加' }}
            </button>
          </div>
        </form>
      </div>
    </Teleport>
  </section>
</template>

<style scoped>
.products-view {
  position: relative;
  min-height: 100%;
  background:
    linear-gradient(180deg, #f4fbff 0%, #f7fbff 24%, #ffffff 62%, #ffffff 100%);
}

.products-header {
  align-items: center;
  margin-bottom: 18px;
}

.add-product {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 12px;
  border: 1px solid rgba(87, 145, 230, 0.18);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.92);
  color: var(--primary);
  box-shadow: 0 10px 22px rgba(71, 119, 183, 0.12);
  font-size: 0.78rem;
  font-weight: 800;
}

.add-product :deep(.el-icon) {
  padding: 3px;
  border-radius: 999px;
  background: var(--primary);
  color: #ffffff;
  font-size: 0.92rem;
}

.product-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0;
  padding: 18px;
  background: rgba(255, 255, 255, 0.96);
}

.product-stat {
  display: grid;
  grid-template-columns: 52px minmax(0, 1fr);
  align-items: center;
  gap: 12px;
}

.product-stat + .product-stat {
  padding-left: 18px;
  border-left: 1px solid rgba(105, 145, 198, 0.16);
}

.product-stat__icon {
  display: grid;
  width: 48px;
  height: 48px;
  place-items: center;
  border-radius: 50%;
  background: linear-gradient(180deg, #edf6ff 0%, #f6faff 100%);
  color: #4d89de;
  font-size: 1.35rem;
  font-weight: 900;
}

.product-stat__label {
  display: block;
  margin-bottom: 5px;
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 700;
}

.product-stat strong {
  color: #4b8cff;
  font-size: 1.6rem;
  line-height: 1;
}

.product-section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 24px 2px 12px;
}

.product-section-title h2 {
  margin: 0;
  color: var(--text-main);
  font-size: 1.18rem;
  line-height: 1;
}

.product-section-title span {
  color: var(--text-muted);
  font-size: 0.78rem;
  font-weight: 700;
}

.product-list {
  display: grid;
  gap: 12px;
}

.product-card {
  display: grid;
  grid-template-columns: 86px minmax(0, 1fr);
  gap: 14px;
  padding: 12px;
  border: 1px solid rgba(105, 145, 198, 0.1);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 10px 24px rgba(66, 105, 153, 0.08);
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.product-card:active {
  transform: scale(0.985);
}

.product-card__cover {
  display: grid;
  height: 86px;
  place-items: center;
  border-radius: 12px;
  overflow: hidden;
}

.product-card__cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-card__cover span {
  display: grid;
  place-items: center;
  width: 68px;
  height: 68px;
  text-align: center;
  line-height: 1.1;
}

.product-card__cover--sky {
  background: linear-gradient(160deg, #f8fafc 0%, #eef6ff 100%);
}

.product-card__cover--sky span {
  border-radius: 50%;
  background: linear-gradient(180deg, #dff3ff 0%, #9bd8ff 100%);
  color: #437ad8;
  font-size: 1.65rem;
  box-shadow: inset 0 -8px 14px rgba(45, 115, 219, 0.1);
}

.product-card__cover--snack {
  background: #fff7e8;
}

.product-card__cover--snack span {
  border-radius: 12px;
  background: linear-gradient(180deg, #ffca4f 0%, #f19a22 100%);
  color: #9a4f00;
  font-size: 0.82rem;
  font-weight: 900;
  transform: rotate(4deg);
}

.product-card__cover--book {
  background: #ecfbf8;
}

.product-card__cover--book span {
  border-radius: 4px;
  background: linear-gradient(160deg, #79d2c8 0%, #4db6aa 100%);
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.68rem;
  font-weight: 800;
  box-shadow: 6px 8px 14px rgba(55, 125, 118, 0.16);
}

.product-card__cover--custom {
  background: linear-gradient(160deg, #eef6ff 0%, #f8fbff 100%);
}

.product-card__cover--custom span {
  border-radius: 18px;
  background: linear-gradient(135deg, #82e0ff 0%, #2f8ef0 100%);
  color: #ffffff;
  font-size: 0.9rem;
  font-weight: 900;
}

.product-card__content {
  min-width: 0;
}

.product-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 16px;
}

.product-card__top h3 {
  margin: 0;
  color: var(--text-main);
  font-size: 1rem;
  line-height: 1.25;
}

.product-card__status {
  flex: 0 0 auto;
  padding: 5px 8px;
  border-radius: 9px;
  font-size: 0.68rem;
  font-weight: 800;
  white-space: nowrap;
}

.product-card__status--normal {
  background: #e7f8ef;
  color: #16a46b;
}

.product-card__status--warning {
  background: #fff1e4;
  color: #f07c22;
}

.product-metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}

.product-metrics span {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 0.66rem;
  font-weight: 700;
  white-space: nowrap;
}

.product-metrics strong {
  color: #4b8cff;
  font-size: 1rem;
  line-height: 1;
}

.product-metrics .is-warning {
  color: #f07c22;
}

:global(.product-modal) {
  position: absolute;
  inset: 0;
  z-index: 9999;
  display: grid;
  place-items: center;
  padding: 22px;
  background: rgba(17, 37, 61, 0.28);
  backdrop-filter: blur(10px);
}

:global(.product-modal__card) {
  width: min(320px, 100%);
  padding: 18px;
  border: 1px solid rgba(126, 165, 220, 0.18);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 24px 60px rgba(18, 30, 52, 0.22);
}

:global(.product-modal__header) {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 14px;
}

:global(.product-modal__header span) {
  display: block;
  margin-bottom: 4px;
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 700;
}

:global(.product-modal__header strong) {
  color: var(--text-main);
  font-size: 1.35rem;
  line-height: 1;
}

:global(.product-modal__header button) {
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

.product-field {
  display: grid;
  gap: 7px;
  margin-top: 11px;
}

.product-field-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.product-field span {
  color: var(--text-main);
  font-size: 0.76rem;
  font-weight: 800;
}

.product-field input {
  width: 100%;
  padding: 11px 12px;
  border: 1px solid rgba(126, 165, 220, 0.2);
  border-radius: 14px;
  outline: 0;
  background: #f8fbff;
  color: var(--text-main);
  font-size: 0.82rem;
}

.product-field input:focus {
  border-color: rgba(45, 115, 219, 0.45);
  box-shadow: 0 0 0 3px rgba(45, 115, 219, 0.08);
}

.product-upload {
  display: grid;
  margin-top: 12px;
}

.product-upload input {
  display: none;
}

.product-upload__preview {
  display: grid;
  height: 82px;
  place-items: center;
  border: 1px dashed rgba(45, 115, 219, 0.36);
  border-radius: 16px;
  overflow: hidden;
  background: #f8fbff;
  color: var(--primary);
  font-size: 0.82rem;
  font-weight: 800;
}

.product-upload__preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

:global(.product-modal__error) {
  margin: 10px 0 0;
  color: #ef4444;
  font-size: 0.72rem;
  font-weight: 700;
}

:global(.product-modal__actions) {
  display: grid;
  margin-top: 14px;
}

:global(.product-modal__actions--edit) {
  grid-template-columns: 0.9fr 1.1fr;
  gap: 10px;
}

:global(.product-modal__delete) {
  width: 100%;
  padding: 12px;
  border: 0;
  border-radius: 15px;
  background: #fff1f1;
  color: #ef4444;
  font-size: 0.86rem;
  font-weight: 900;
}

:global(.product-modal__submit) {
  width: 100%;
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
  .add-product {
    padding: 9px 10px;
    font-size: 0.74rem;
  }

  .product-card {
    grid-template-columns: 78px minmax(0, 1fr);
    gap: 12px;
  }

  .product-card__cover {
    height: 78px;
  }

  .product-card__cover span {
    width: 62px;
    height: 62px;
  }

  .product-metrics {
    gap: 6px;
  }
}
</style>
