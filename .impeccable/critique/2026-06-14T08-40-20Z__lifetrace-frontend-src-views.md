---
target: lifetrace-frontend/src/views
total_score: 25
p0_count: 0
p1_count: 3
timestamp: 2026-06-14T08-40-20Z
slug: lifetrace-frontend-src-views
---
# LifeTrace 移动端页面 UX 审查报告

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | 多数增删改动作没有成功反馈；AI 回复有即时回显，但其他页面保存后只关闭弹窗。 |
| 2 | Match System / Real World | 3 | 术语整体贴近学生摊主；“商品单子”等个别文案略口语但不够清楚。 |
| 3 | User Control and Freedom | 3 | 主要弹窗可取消；缺少撤销、确认后的恢复路径。 |
| 4 | Consistency and Standards | 2 | 日志/商品卡片用 article 模拟按钮，日程用 button；弹窗和表单实现方式不完全一致。 |
| 5 | Error Prevention | 2 | 日程和商品有基础校验；日志保存位置为空时静默失败，排队操作对无当前服务状态缺少提示。 |
| 6 | Recognition Rather Than Recall | 3 | 底部导航有文字，主路径可见；部分 icon-only / close 按钮缺少明确名称。 |
| 7 | Flexibility and Efficiency | 2 | 适合新手轻量使用；缺少批量、快捷或快速复用路径。 |
| 8 | Aesthetic and Minimalist Design | 3 | 视觉整体轻量温暖；重复蓝白卡片较多，个别阴影和圆角偏重。 |
| 9 | Error Recovery | 2 | 表单错误文案存在但读屏语义不足；保存成功、删除后恢复、空状态指导不足。 |
| 10 | Help and Documentation | 1 | 没有上下文帮助；对第一次使用的学生摊主只依赖页面标题和占位符。 |
| **Total** | | **25/40** | **Acceptable：可用基础不错，但发布前需要移动端可用性收口。** |

## Anti-Patterns Verdict

**LLM assessment**: 这不像完全随机生成的 AI 页面，因为领域信息明确，导航结构和五个任务页都围绕学生摊主经营闭环。但它有几个典型“演示稿”痕迹：许多数据是静态状态，保存后缺少反馈，卡片按钮语义不稳定，弹窗/表单样式重复实现，部分控件为了视觉像按钮但没有完整交互状态。

**Deterministic scan**: `detect.mjs --json lifetrace-frontend/src/views` 返回 `[]`，未命中内置反模式。复扫 `src/views src/components src/styles` 也返回 `[]`。这说明没有明显的 detector 规则问题，但不能证明交互和可访问性已经达标。

**Visual overlays**: 当前 Codex 环境没有浏览器自动化面板可用于可见 overlay 注入；未生成 Human tab overlay。替代证据来自源码审查、detector 和 Vite 构建。

## Overall Impression

LifeTrace 的基础方向是对的：移动端优先、底部导航清楚、蓝白视觉温和，和“校园摊主的小助手”匹配。最大机会是把它从“看起来像能用的 demo”推到“忙碌场景真的能放心点”的状态：补足按钮语义、触控尺寸、焦点、错误反馈、成功反馈和小屏稳定性。

## What's Working

- 五个核心模块覆盖完整：出摊日志、日程、AI、商品、排队，符合 PRODUCT.md 的经营闭环。
- 底部导航有文字标签，适合首次使用，不需要记图标含义。
- 颜色整体克制，主蓝色、成功绿、提醒橙、危险红已经建立了基础语义。

## Priority Issues

**[P1] 交互语义和可访问性不稳定**

**Why it matters**: 忙碌移动端用户需要可点区域明确，键盘/读屏用户需要正确语义。用 `article role="button"` 模拟按钮容易漏掉焦点、键盘、aria 状态。

**Fix**: 日志卡片、商品卡片改成真正的 `<button>`；补 `aria-label`、可见焦点、44px 触控目标。

**Suggested command**: `$impeccable polish lifetrace-frontend/src/views`

**[P1] 表单错误和操作反馈不足**

**Why it matters**: 保存失败、输入错误或成功后没有明确反馈时，用户会怀疑数据是否保存，尤其是在出摊现场。

**Fix**: 错误文案加 `role="alert"`；提交按钮根据输入禁用；后续应补成功 toast 或保存状态提示。

**Suggested command**: `$impeccable harden lifetrace-frontend/src/views`

**[P1] 弹窗层级和关闭控件过于随意**

**Why it matters**: `z-index: 9999`、32px 关闭按钮、无 aria 名称会让弹窗像临时实现，也影响触控和可访问性。

**Fix**: 使用稳定层级值；关闭按钮至少 44px；补明确 `aria-label`。

**Suggested command**: `$impeccable polish lifetrace-frontend/src/views`

**[P2] AI 助手页输入区缺少完整状态**

**Why it matters**: 空输入时提交没有提示，发送按钮图标语义偏“语音”，读屏没有输入 label。

**Fix**: 给输入框添加隐藏 label；空输入禁用发送；增加“新对话”作为控制出口。

**Suggested command**: `$impeccable harden lifetrace-frontend/src/views/AiAssistantView.vue`

**[P2] 小屏文本和触控区域还需要持续压测**

**Why it matters**: 页面运行在 390px 手机框中，长商品名、长地点、长备注和底部 composer 都可能挤压。

**Fix**: 降低窄屏标题字号；保持按钮/关闭控件 44px；后续用真机或浏览器截图检查 360/390/420px。

**Suggested command**: `$impeccable adapt lifetrace-frontend/src/views`

## Persona Red Flags

**Sam（无障碍依赖用户）**: polish 前日志/商品卡片是模拟按钮，关闭按钮只有 `×`，错误信息不是 alert。读屏和键盘路径会不稳定。

**Casey（忙碌移动端用户）**: 添加按钮、关闭按钮和 composer 圆形按钮部分低于 44px；出摊现场单手操作时容易误触或点不到。

**Jordan（第一次使用的学生摊主）**: 主流程清楚，但保存成功没有反馈；排队页“商品单子”不如“商品内容”明确。

## Minor Observations

- `resetChat` 已存在但 polish 前没有入口。
- detector 没有发现 slop，但代码里硬编码视觉值较多，未来可进一步抽 tokens。
- 构建产物 chunk 超过 500k，主要是依赖体积，不是本轮 UX 阻塞项。

## Questions to Consider

- 保存日志、商品和日程后，用户最需要看到 toast、列表高亮，还是轻量震动/状态条？
- 排队管理是否需要“当前服务为空”时禁用完成/取消按钮，而不是静默无动作？
- 商品页是否需要一个真正的空库存/低库存优先视图，而不是只在卡片内提示？

## Polish Applied In This Run

- 日志和商品列表卡片已改成真正 `<button>`，并补充可访问名称。
- 底部导航增加 `aria-current`，icon/当前页语义更清楚。
- 全局补充可见 `focus-visible`、禁用状态、占位符对比度和 reduced motion。
- 关键按钮、关闭按钮和 action 控件提高到更接近 44px 触控目标。
- AI 输入框补隐藏 label，空消息禁用发送，并添加“新对话”出口。
- 弹窗错误信息补 `role="alert"`，弹窗层级从任意 `9999` 收口到稳定层级。
- 排队页“商品单子”统一为“商品内容”。
