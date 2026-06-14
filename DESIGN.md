---
name: LifeTrace
description: 面向学生摊主的移动端轻量经营助手。
colors:
  primary: "#2d73db"
  primary-soft: "#e9f3ff"
  screen-blue: "#f4fbff"
  surface: "#ffffff"
  surface-tint: "#f8fbff"
  text-main: "#16324f"
  text-strong: "#11253d"
  text-muted: "#6c86a4"
  success: "#16a46b"
  warning: "#f07c22"
  danger: "#ef4444"
  ai-violet: "#7d55ea"
  device-black: "#1f1f1f"
typography:
  display:
    fontFamily: "SF Pro Display, Segoe UI, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif"
    fontSize: "2.2rem"
    fontWeight: 800
    lineHeight: 1.18
    letterSpacing: "0"
  headline:
    fontFamily: "SF Pro Display, Segoe UI, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif"
    fontSize: "1.55rem"
    fontWeight: 900
    lineHeight: 1.1
    letterSpacing: "0"
  title:
    fontFamily: "SF Pro Display, Segoe UI, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 800
    lineHeight: 1.25
  body:
    fontFamily: "SF Pro Display, Segoe UI, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 600
    lineHeight: 1.7
  label:
    fontFamily: "SF Pro Display, Segoe UI, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 700
    lineHeight: 1.2
rounded:
  xs: "5px"
  sm: "8px"
  md: "14px"
  lg: "18px"
  xl: "24px"
  card: "28px"
  pill: "999px"
spacing:
  xs: "8px"
  sm: "10px"
  md: "14px"
  lg: "16px"
  xl: "18px"
  page: "22px"
  panel: "24px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "12px 18px"
  button-soft:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
    rounded: "{rounded.pill}"
    padding: "7px 10px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-main}"
    rounded: "{rounded.card}"
    padding: "20px"
  input:
    backgroundColor: "{colors.surface-tint}"
    textColor: "{colors.text-main}"
    rounded: "{rounded.md}"
    padding: "12px 14px"
  nav-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.pill}"
    size: "56px"
---

# Design System: LifeTrace

## 1. Overview：概览

**Creative North Star: "校园摊主的口袋控制台"**

LifeTrace 应该像学生手里的一个小型经营控制台：在不理想的环境里也能快速看清，在校园生活里足够亲切，同时又能把出摊、库存、日程、排队这些容易乱掉的事情组织起来。当前视觉系统是一个浅色移动端外壳，使用柔和蓝色背景、白色卡片、紧凑摘要和清晰中文标签。

产品性格是轻量、温暖、清晰。因此视觉应该克制用色、使用熟悉的移动端控件、保证足够大的点击区域，并用直接的中文标签降低理解成本。它明确拒绝企业后台密度、冷冰冰的财务软件、ERP 风格和表格化管理界面。

**Key Characteristics：关键特征**
- 移动端优先：手机框架、底部导航、短任务流程。
- 柔和蓝色主操作，搭配白色和极浅蓝工作面。
- 卡片和输入框有圆角，但必须保留足够结构感，不能糊成一团。
- 状态颜色必须搭配 `库存不足`、`已完成`、`服务中` 这样的文字。
- 使用适合中文移动端 UI 的系统无衬线字体，不做装饰性品牌字体。

## 2. Colors：颜色

LifeTrace 的配色是一套克制的蓝色经营工具调色板，辅以绿色、橙色、红色语义色，以及一个用于 AI 的紫色小强调。

### Primary
- **清爽出摊蓝**：主要操作和选中状态颜色。用于主按钮、当前导航、聚焦状态、链接和最重要的数据强调。
- **浅蓝提示底**：柔和辅助色。用于选中背景、浅色标签、摘要卡片和友好的局部强调。
- **屏幕雾蓝**：应用外壳氛围色。用于手机屏幕顶部和页面背景，让白色界面更柔和，但不能变成装饰。

### Secondary
- **AI 助手紫**：只用于 AI 助手徽标和少量陪伴型强调。它不能替代主操作色。

### Tertiary
- **完成绿**：用于已完成、库存健康、服务正常等正向经营状态。
- **提醒橙**：用于库存不足、待注意、利润提醒或高温/客流提示。
- **危险红**：只用于删除、输入错误、取消订单和破坏性操作。

### Neutral
- **工作白**：主要卡片、弹窗和底部导航表面。
- **浅面板蓝白**：用于表单输入、列表行背景和嵌套辅助区域。
- **墨蓝正文**：主要文字颜色。正文和标签应优先使用它，而不是在蓝色背景上使用发灰文字。
- **强墨蓝**：页面标题和高强调数字。
- **静音蓝灰**：辅助说明和元信息。必须注意对比度，不能用于关键说明。
- **设备黑**：只用于手机外壳和刘海。

### Named Rules

**蓝色只做事规则。** 主蓝色只用于操作、选中和聚焦状态；不要把它到处撒成装饰。

**状态必须有文字规则。** 绿色、橙色、红色和紫色必须搭配文字标签或图标。禁止只靠颜色表达状态含义。

## 3. Typography：字体

**Display Font:** SF Pro Display，后备为 Segoe UI、PingFang SC、Hiragino Sans GB、Microsoft YaHei、sans-serif。
**Body Font:** 同一套系统无衬线字体。
**Label/Mono Font:** 不使用单独的标签字体或等宽字体。

**Character：字体性格**：字体系统要实用、自然、像原生移动端工具。它应该像一个打磨过的小工具，而不是宣传页或桌面管理后台。

### Hierarchy
- **Display**（800，2.2rem，1.18）：页面标题，例如 `出摊日志`、`商品管理`、`排队管理`。谨慎使用，不要塞进紧凑列表行。
- **Headline**（900，1.55rem，1.1）：居中或特殊页面标题，尤其适合 AI 助手页面。
- **Title**（800，0.95rem，1.25）：卡片标题、列表项标题、商品名和弹窗标题。
- **Body**（600，0.95rem，1.7）：说明、AI 回复、备注和解释性文字。文案要短，因为这是移动端任务界面。
- **Label**（700，0.72rem，1.2）：元信息、表头、状态标签、底部导航文字和表单标签。

### Named Rules

**原生工具规则。** 整个产品使用一套系统无衬线字体。核心 UI 禁止引入展示字体、衬线品牌字体或等宽字体风格。

**关键文字不能太小规则。** 用户需要据此行动的说明、状态和错误信息，必须具备可读字号和足够对比度；小标签只用于辅助元信息。

## 4. Elevation：层级与阴影

LifeTrace 使用色块层级和轻柔阴影的混合策略。阴影用于帮助卡片、浮动控件和弹窗从手机背景中分离出来，但必须轻、克制、服务功能。沉重的桌面式阴影会让应用显得企业化、迟钝。

### Shadow Vocabulary
- **柔和卡片浮层**（`0 16px 36px rgba(71, 119, 183, 0.12)`）：重要容器的共享卡片阴影。
- **紧凑控件浮层**（`0 10px 24px rgba(71, 119, 183, 0.12)`）：添加按钮、商品卡片和小型操作控件。
- **弹窗浮层**（`0 24px 60px rgba(18, 30, 52, 0.22)`）：只用于手机框架内的弹窗。
- **底部栏浮层**（`0 -6px 18px rgba(77, 116, 169, 0.05)`）：用于区分底部导航和内容。

### Named Rules

**忙碌手指规则。** 阴影应该帮助用户判断什么可点、什么在浮动。只是好看的阴影应该删掉。

## 5. Components：组件

### Buttons

- **Shape:** 方形操作按钮使用温和圆角（14-17px），紧凑标签使用胶囊圆角，纯图标添加按钮可以使用圆形。
- **Primary:** 清爽出摊蓝配白字，现有实现中常使用蓝色渐变。用于保存、添加、确认和当前 AI 中心操作。
- **Hover / Focus:** 使用 150-250ms 的颜色、位移或聚焦环反馈。键盘聚焦必须有可见蓝色轮廓或边框变化。
- **Secondary / Ghost / Tertiary:** 次级按钮使用浅蓝标签或灰色幽灵按钮。破坏性按钮使用危险红加浅红背景。

### Chips

- **Style:** 柔和蓝色或语义色胶囊标签，文字加粗，横向内边距紧凑。
- **State:** 选中或激活标签使用主色；警告和成功标签必须同时使用文字和颜色。不要只靠色相传递状态。

### Cards / Containers

- **Corner Style:** 当前大卡片使用 18-28px 圆角；重复列表卡片应收紧到 16-18px，以保持信息密度。
- **Background:** 工作白叠在屏幕雾蓝或浅面板蓝白之上。
- **Shadow Strategy:** 主要容器使用柔和卡片浮层；嵌套列表行应减少或去掉阴影。
- **Border:** 在阴影较轻时，用浅蓝边框定义卡片边界。
- **Internal Padding:** 卡片 16-20px，列表行和紧凑卡片 12-16px。

### Inputs / Fields

- **Style:** 浅蓝白背景、14px 圆角、上方清晰标签、直接可理解的占位文字。
- **Focus:** 使用主蓝色边框和浅蓝聚焦光晕。
- **Error / Disabled:** 错误文字使用危险红，并提供可读错误信息。禁用状态可以降低透明度，但仍要保持可读。

### Navigation

底部导航是产品锚点：五个等分目的地，图标加文字，中间 AI 操作凸起。当前状态使用清爽出摊蓝，未激活项保持静音蓝灰。标签必须短，保证小屏幕不挤压。

### Signature Component

手机框架是应用展示的一部分：黑色设备外壳、刘海、状态栏、可滚动屏幕内容和固定底部导航。它应作为移动端优先设计检查的稳定预览面。

## 6. Do's and Don'ts：应该做与不要做

### Do:

- **Do** 保持移动端优先：大点击区域、短标签、稳定底部导航和可滚动任务页面。
- **Do** 使用清爽出摊蓝表达主操作、当前选中和聚焦状态。
- **Do** 每个状态颜色都搭配 `库存不足`、`已完成`、`服务中`、`已取消` 等文字。
- **Do** 保持表单短、直接、友好，适合忙碌出摊场景。
- **Do** 保证正文、占位符和状态标签达到 WCAG AA 对比度目标。

### Don't:

- **Don't** 让 LifeTrace 看起来像企业后台、ERP 系统、正式进销存平台，或冷冰冰的财务/会计软件。
- **Don't** 把页面做成密集桌面仪表盘、表格化财务界面或配置很多的管理后台。
- **Don't** 使用复杂动画、页面加载编排，或任何拖慢任务完成的动效。
- **Don't** 只依赖颜色表达状态、警告、错误或排队状态。
- **Don't** 引入装饰性渐变文字、卡片侧边色条、玻璃拟态或营销页式超大标题。
