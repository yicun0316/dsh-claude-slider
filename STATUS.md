# STATUS.md — dsh-claude-slider 改造进度

> 以本文件为准，不要依赖记忆。每完成一步就更新。

## 发布状态（2026-10-17）

| 项 | 状态 |
|---|---|
| 代码 / 文档 | ✅ 完成，全部校验通过 |
| git commit | ✅ 8 个功能提交：`817eedd`（主体 1747+/1406-）→ `a501275` → `230dccf`（rAF 护栏）→ `b3806cd`（README）→ `83878df`（STATUS）→ `df35474`（删死 CSS 变量）→ `c011899`（思考图标实时预览）→ `243c975`（ICONS 别名去重），中间夹若干纯文档提交 |
| git push | ✅ 已同步 `origin/main`（`0 0` ahead/behind），HEAD = `243c975` |
| git tag | ✅ `v2.12.0`（annotated，`8a15f40`）指向 `243c975`，已 push |
| release tarball | ✅ `D:\deepseek\dsh-claude-slider-2.12.0.tgz`（115034 B，SHA256 `A3BDD745D70BC2550FC7863A385ECC8649839E402B301996B6343093E79E5121`，7 files；从 `git archive HEAD` 的干净树打包，与 `243c975` 逐字节一致） |
| npm publish | ❌ **被凭据阻断** —— 见下 |

### npm 发布受阻的具体原因

`C:\Users\王文岩\.npmrc` 里的 token 已失效：
```
$ curl -H "Authorization: Bearer npm_CBvu..." https://registry.npmjs.org/-/whoami
→ 401 Unauthorized
```
npm 侧表现：
```
npm error code E404
npm error 404 Not Found - PUT https://registry.npmjs.org/dsh-claude-slider
```
（npm 10 在 token 无效时会把 401 的 PUT 报成 404，实际是鉴权失败，不是包不存在。）

包本身存在且所有权正常：
```
https://registry.npmjs.org/dsh-claude-slider  → 200, latest 2.11.0
maintainers: [{"name":"yicun0316","email":"2821427065@qq.com"}]
dist-tags: {"latest":"2.11.0"}
published versions: 2.9.7, 2.9.8, 2.11.0
```

**需要用户操作**：`npm login`（或换一个有效 token 写进 `.npmrc`），然后二选一：
```bash
cd C:\Users\王文岩\.gemini\antigravity\scratch\dsh-claude-slider
npm publish --access public --registry=https://registry.npmjs.org/

# 或者直接发已经打好的包（等价）
npm publish D:\deepseek\dsh-claude-slider-2.12.0.tgz --access public --registry=https://registry.npmjs.org/
```

## 当前任务（用户 m00001 提出，四项）

| # | 任务 | 状态 |
|---|---|---|
| 1 | 删除「工坊」和「随机」功能 | ✅ 已完成（client.js + demo 双端） |
| 2 | 游标/thumb 加 Q 版人物通用动画（跑步循环 + 惯性 + 大力拖拽刹车不稳） | ✅ 已完成（双端） |
| 3 | 新增「直接拖」模式（不吸附，连续进度条），动效档位递进（Low 静止图 → 递进） | ✅ 已完成（双端） |
| 4 | 加入图一的「思考中」动画（挂宿主思考指示器），支持换图标 + 整套动画（鲸鱼尾巴动效） | ✅ 已完成（双端） |

## 关键事实（勘察结论）

- 仓库根：`C:\Users\王文岩\.gemini\antigravity\scratch\dsh-claude-slider`
- 主文件 `lib/client.js`（当前 6432 行）；`demo/index.html`（当前 10199 行）。**零构建**，直接加载。
- 插件是 **link 安装**：`C:\Users\王文岩\.dsh\profiles\desktop\package.json` 里
  `"dsh-claude-slider": "link:C:\\Users\\王文岩\\.gemini\\antigravity\\scratch\\dsh-claude-slider"`，
  `patchReload: "live"` → **改源码即生效**，无需重装。
- AGENTS.md 硬约束：禁止整文件重写；只允许增量精确编辑；禁止删文件；禁止引入构建步骤；禁止发网络请求。
- 改完必须跑：`node --check lib/client.js` 和 `node scripts/check-undefined.cjs lib/client.js`。
- 文件编码：UTF-8 无 BOM、**纯 LF**、无 CRLF。写回一律 `newline=""`。

## 任务 1：工坊 / 随机删除（已完成）

client.js 删 9 段共 577 行（`CURATED_COMBOS`、随机洗牌袋 + `applyRandomCombo`、
`SHARE_PRESETS`/`applyParsedConfig`/`LiquidGlassShareModal`、工坊 tab、随机按钮、
TAB6 面板、`.dcs-share-modal-*` CSS、`.dcs-workshop-*` CSS）。
demo 删 10 段共 645 行（两份重复的随机帮助函数、工坊面板、随机按钮、分享弹窗、
`.drawerRandomBtn`、以及 `drawerExportBtn`/`drawerImportBtn` 死绑定）。

**保留不动**（不是工坊，是客制粒子工坊功能的一部分）：`.dcs-custom-studio-banner` 等
`.dcs-studio-*` 类。残留「工坊」字样仅为注释。

## 任务 2/3：游标物理动画 + 自由拖拽（已完成）

### 新增配置键（client.js `DEFAULT_CONFIG` 与 demo 常量，9 个）
`dragMode:"free"` / `thumbAnim:"run"` / `thumbSkin:"bubble"` / `thumbInertia:true` /
`thinkEnabled:true` / `thinkIcon:"fish_tail"` / `thinkCustomIcon:""` /
`thinkAnim:"tail_wag"` / `thinkColor:""`

`loadSavedConfig()` 对每个键做了白名单归一化（非法值回落默认）。

### client.js
- `THUMB_ANIMATIONS`（6 项：run/hop/lean/float/spin/none）
- `function ThumbRig({ config, color, isDragging, ratio })` — rAF 物理引擎：
  一阶速度低通 → 速度/加速度估计 → `braking`（骤减速）与 `reversed`（反向）
  触发趔趄 `stAmp`，`wob = sin(stT*27) * exp(-stT*4.4) * stAmp` 驱动
  `rotate/translate/scale`。`prefers-reduced-motion` 时清空 transform 并退出。
- `ClaudeEffortPopover`：`dragMode === "free"` 时 `applyFromClientX` 直接写原始
  ratio（不 round），否则走吸附。历史冗余（`setPointerCapture` /
  `releasePointerCapture` / `pointercancel` 各重复 2 次）已清理。
- CanvasEffect：`lowTierStill = currentRatio < 0.34` → idle 时 `targetDecay` 降到
  0.08/0.45，实现「Low 接近静止图像」。

### demo（原生侧是真实 UI；React 轨是死代码，不渲染）
- `thumbRigLoop(now)`（自续帧 rAF）、`syncDragVisuals()`、`ratioFromClientX()`
- `updateUI()` 里 `isMax` 判定从 `currentTierIdx === TIERS.length-1` 改为
  `currentRatio >= 0.98`（自由拖下档位索引不可靠）
- 新增 `#drawerDragContent` 面板 + `#tabDragBtn`「🏃 拖拽」标签
- CSS：`.slider-thumb-body` / `.slider-thumb-bubble` / `.is-free-drag`（干掉 left 过渡）

### 实测验证（headless Chrome + 真实 PointerEvent）
```
thumbBody transform: translate(0px,-0.05px) rotate(0.07deg) scale(1,1.001)
--thumb-spd: 0.200     拖动到 45% → thumb.style.left = calc(45% + 1.4px)
track is-free-drag: true    thumb classes: slider-thumb is-max is-free has-bubble
thumb transition: transform, box-shadow | 0.1s, 0.2s   ← left 过渡已移除
active tier btns: 1 Low     passed dots: 2
```
档位递进实测（轨道截图条）：Off = 空旷轨道 → Low = 6 粒微光 → High = 半轨粒子流
→ Max = 满轨高亮粒子 + 泛光。与需求「Low 静止图，随档位递进」一致。

## 任务 4：宿主思考指示器注入（已完成）

### 关键发现（与最初假设不同）
宿主 `TurnStatus` **没有图标节点** —— 用户截图的「蓝色小鲸鱼」其实是
`-webkit-background-clip:text` 把文字染色后的渐变形状。正文渲染点在
`dsh-client-ui-chat\lib\client.js:1984`，DOM 为
`div.EvIC1a_turnStatus[role="status"][aria-live="polite"]`，**无任何专用插槽**
（ui-chat 的 11 个插槽里没有 thinking/status 类）→ 只能 DOM 注入。

### client.js 实现
- `THINK_ICONS`（8 项，`svg(c)` 返回 **SVG 字符串**，供 `innerHTML` 用）
- `THINK_ANIMATIONS`（7 项：tail_wag/swim/pulse/spin/bounce/drift/none）
- `safeSvgColor()`（白名单正则，防任意串注入 innerHTML）
- `buildThinkIconDom()`（建 `<span class="dcs-think-icon">`）
- `installThinkIndicator(ctx)` — 在 `ctx.effect` 里：
  - `findStatus()` 优先找带 `EvIC1a_turnStatus` class 的那个
  - `sync()` → `status.insertBefore(node, status.firstChild)`
  - MutationObserver 观察 `document.body {childList, subtree}`，
    **性能护栏**：自家节点已连接且仍在首位时直接 return；外加 60ms 节流
  - `configStore.subscribe` → 图标变化时 `replaceChild` 重建，动画/颜色原地更新
  - 返回清理函数（unsubscribe + disconnect + removeNode）
- CSS：`.dcs-think-icon`（16×16、`margin-right:6px`、
  **`-webkit-text-fill-color: currentColor`（必须显式覆盖宿主染色）**）
  + 7 套 `[data-anim]` 关键帧 + `prefers-reduced-motion` 关闭

### demo 实现
`#tabThinkBtn`「🧠 思考」面板（图标网格 / 上传本地图标 / 7 套动画药丸）+
`.think-showcase-card` 演示卡片，模拟真实状态栏并实时反映设置。

### 实测验证（headless 注入模拟 TurnStatus，8 个场景全过）
```
first child is icon: true    data-anim = tail_wag    svg: true
[heal] icon re-injected: true          ← 宿主重渲染后自愈
[swap icon] data-sig = sparkles
[swap anim] same node: true | data-anim = spin | color = #FF8800
[disable] icon removed / [re-enable] icon back
[custom] is <img>: true
[cleanup] observer disconnected (no re-inject): true
```
浏览器实测：`thinkIcon animationName: dcsThinkTail | duration: 0.86s |
color: rgb(77,107,254) | w: 16px | h: 16px`

## 文件状态（最终）

| 文件 | 行数 | 校验 |
|---|---|---|
| `lib/client.js` | 6432 | `node --check` exit=0；check-undefined「✅ 干净：扫描 21 个全大写标识符」 |
| `demo/index.html` | 10199 | 2 个 `<script>` 块 `node --check` exit=0；dangling ids: NONE |

均 UTF-8 无 BOM、纯 LF。

### 抽屉标签栏（6/7 个标签不换行）

- demo：`.drawer-header-bar` 与 `.drawer-tabs` 都加 `min-width: 0`，`.drawer-tabs`
  加 `flex: 1 1 auto`；`.drawer-tab-btn` 字号 11→10px、`letter-spacing: -0.3px`、
  `padding: 5px 0`。实测 6 个标签各 38×23px、合计 227px，落在 240px 容器内，
  `clipped=false`（修前：6×44=265px > 240px，第 6 个「🧠 思考」被裁）。
- client.js：已有 `.dcs-drawer-header .dcs-drawer-tabs { flex:1; min-width:0 }` +
  `.dcs-drawer-tab { flex-direction: column; padding:4px 1px }`，7 个标签本就单行。

## 备份

`_backups/` 下（`.gitignore` 已排除）：
- `client.js.20261016-224836.bak`、`index.html.20261016-224836.bak`（最初基线）
- `client.js.20261016-230649.bak`、`index.html.20261016-230649.bak`
- `client.js.before-thumb-demo.20261016-233059.bak`（302442B）
- `index.html.before-thumb-demo.20261016-233059.bak`（447433B）

## 下一步（用户操作）

```bash
cd C:\Users\王文岩\.gemini\antigravity\scratch\dsh-claude-slider
git add -A && git commit -m "feat: 游标物理动画 + 直接拖拽模式 + 宿主思考指示器注入；移除工坊与随机"
```

## 收尾补齐（README / AGENTS / catalog，已完成）

- `README.md`（130 → 137 行，增量编辑，未重写）
  - 第 73 行「滑块交互」改为覆盖 `free` / `snap` 双模式（原文只写「拖拽吸附换档」）
  - 新增「**Q 版游标动画**」条目（6 套动作 + 趔趄公式 + 两种皮肤 + reduced-motion）
  - 新增「**思考指示器**」条目（8 图标 × 7 动画 + 自定义上传 + MutationObserver 自愈）
  - 删除宣传已删功能的第 93 行「灵感搭配」与第 95 行「配置分享」，
    原位替换为「**档位递进**」（Low 静止 / High 脊线 / Max 泛光）
  - 「调校参数」表后补一段：9 个新配置键在「🏃 拖拽」「🧠 思考」页调整，存同一
    `localStorage` 键
- `AGENTS.md` 第四节「新增动效必改 4 处」→ 3 处：删掉 `CURATED_COMBOS`（已随工坊删除）
- `D:\deepseek\dsh-catalog-submission\yicun0316__dsh-claude-slider.yml`
  en/zh 描述重写，加入双拖拽模式、Q 版游标物理动画、思考指示器注入三项新特性

### 本轮校验（改完后跑过）

```
node --check lib/client.js                      → exit=0
node scripts/check-undefined.cjs lib/client.js  → ✅ 干净：扫描 21 个全大写标识符
README.md / AGENTS.md / STATUS.md / lib/client.js / demo/index.html
  UTF-8 无 BOM、纯 LF（bom=False crlf=False）
git status --porcelain → M AGENTS.md / M README.md / M STATUS.md / M demo/index.html / M lib/client.js
```

改动生效方式：插件是 link 安装，**改完源码刷新页面即生效**（`patchReload: "live"`）。
若思考图标未出现，确认会话处于「正在推理」状态（宿主只在 running 时渲染 TurnStatus）。

---

## 2026-10-17 紧急修复：THUMB_ANIMATIONS / THINK_ANIMATIONS 类型错误（用户报「完全用不了」）

### 症状
DSH 实机弹窗报错：
- `推理调节组件异常 / THUMB_ANIMATIONS.map is not a function`
- `推理调节组件异常 / THINK_ANIMATIONS.map is not a function`

### 根因
`lib/client.js` 里 `THINK_ANIMATIONS` / `THUMB_ANIMATIONS` 声明成了**对象** `{ id: {...} }`，
而 QuickDrawer 的「拖拽」与「思考」两个 tab 用 `.map(...)` 渲染药丸按钮，对象没有 `.map` → 抛错。

**为什么此前的测试没抓到**：`dcs_smoke.cjs` 只调 `apply()`，从不渲染 React 子树；
这些错误只在 render 期暴露。demo 侧本来就是数组，所以 demo 一切正常。

### 修复
1. `lib/client.js:559` `THINK_ANIMATIONS` → 数组（tail_wag / swim / pulse / spin / bounce / drift / none）
2. `lib/client.js:570` `THUMB_ANIMATIONS` → 数组（run / hop / lean / float / spin / none）
3. 新增 `lib/client.js:580` `function hasAnimationId(list, id)`
4. `loadSavedConfig()` 的归一化改用 `hasAnimationId`（`:811` / `:816`）

### 新增测试：`C:\Users\王文岩\AppData\Local\Temp\dcs_render_browser.html`
用**真实 React 19.3.0 + react-dom/client**在 Chrome 里挂载插件的真实组件，
自动点开推理强度弹窗 → 打开鲸鱼娘抽屉 → 逐个点击全部 7 个 tab。

结果：
- `registered: 2`（设置页 + 模型选择器）
- `tabs: ["✨动效","🎨外观","🏃拖拽","⚡调校","🐳游标","🧠思考","🔊音效"]` 全部 `active: true`
- `finalNotFunction: []`
- `finalBoundary: false`（错误边界未触发）

**教训：mock 冒烟测试必须真实渲染组件，否则会漏掉 render 期错误。**
以后改动组件渲染逻辑，务必跑一次上面这个真实浏览器渲染测试。

---

## 2026-10-17 收尾补齐 2：`thinkColor` 补 UI + 颜色签名修复

### 背景（真实缺口）
README 第 110-112 行把 `thinkColor` 列为可在「🧠 思考」页调整，但代码里它是
**纯内部变量**：`lib/client.js:789` 只有默认值，`:6242` / `:6322` 两处消费，
**没有任何控件**；`demo/index.html:2070` `let thinkColor = ""` 也只被 `:2405` 读取。

### client.js（纯增量，未重写）
「🧠 思考」tab 在「思考动画」药丸之后、「思考图标自检」之前插入一行 `图标颜色`
（`dcs-liquid-row` + `dcs-color-circles-bar`）：
- `dcs-custom-color-chip` 内嵌 `<input type="color" className="dcs-native-color-picker">`
  → `onChange: (e) => configStore.update({ thinkColor: e.target.value })`
- 文字：`config.thinkColor ? config.thinkColor.toUpperCase() : "跟随主题色"`
- 有自定义色时额外渲染「跟随主题色」按钮 → `configStore.update({ thinkColor: "" })`
- **复用既有 CSS**（`.dcs-custom-color-chip` `:5811`、`.dcs-native-color-picker` `:5835`），未加新样式

### 同时修掉一个真实缺陷（关键）
`installThinkIndicator` 的签名函数原本只有图标两项：
```js
const sigOf = () => state.icon + "|" + state.customIcon;
```
但 SVG 的 `fill` 是 `buildThinkIconDom()` 建节点时用 `safeSvgColor(color)` **烧进标签的**，
`node.style.color = state.color` 改不动它 → **只换颜色时 `data-sig` 不变，节点不重建，颜色永远不生效**。
已改为把颜色纳入签名：
```js
// 颜色必须进签名：SVG 的 fill 是建节点时烧进去的，只改 style.color 不会换色
const sigOf = () => state.icon + "|" + state.customIcon + "|" + state.color;
```

### demo（+27 行）
- `#drawerThinkContent` 末尾加「图标颜色」行：`#thinkColorPicker`（`type="color"`）、
  `#thinkColorText`、`#thinkColorReset`
- 新增 `syncThinkColor()`，由 `syncThinkToggle()` 尾调，负责回填 picker / 文字 / reset 显隐
- `applyAccentColor()` 末尾补 `syncThinkColor()` + `if (!thinkColor) updateThinkIcon()`
  —— 主题色变了且未设自定义色时，图标要跟着换色
- `bindNewPanels()` 里绑 picker 的 `input`（实时预览）与 reset 的 `click`

### 实测（headless Chrome + CDP，`D:\deepseek\_cdp.mjs`）
```
openThinkTab        => "block"
thinkColorControls  => { picker:true, pickerValue:"#4d6bfe", text:"跟随主题色", resetVisible:"none" }
setColor(#ff8800)   => { text:"#FF8800", resetDisplay:"block", svgFill:"#ff8800" }
resetColor          => { text:"跟随主题色", resetDisplay:"none", svgFill:"#4D6BFE" }
accentFollows       => { before:"rgb(77,107,254)", after:"rgb(0,200,150)", text:"跟随主题色" }
```
思考抽屉 `clientHeight 559 / scrollHeight 951`，颜色行在动画药丸下方正常显示。

### 真实宿主验证（不止 demo）
DSH 桌面应用窗口（`1294x829`）截图放大后，「深度求索中，用时 17分51秒…」文字左侧
已有 16×16 蓝色鲸鱼尾鳍图标 → **任务④在真实宿主中已生效**。

### 校验
```
node --check lib/client.js                      → exit=0
node scripts/check-undefined.cjs lib/client.js  → ✅ 干净：扫描 21 个全大写标识符
demo 2 个 <script> 块 new Function()            → block0 OK / block1 OK
dangling ids（`D:\deepseek\_checkids.cjs`）     → MISSING: NONE（94 声明 / 78 引用）
new ids present                                 => thinkColorPicker=true thinkColorText=true thinkColorReset=true
```

### 注意：demo 抽屉是页面内联展开，不是浮层
`demo/index.html:1480` 的 `.quick-drawer` 是 `position: relative` 的内联块，由
`#drawerToggle` 点击切换 `style.display`；直接点 tab 不会打开抽屉。CDP 里必须先
`document.getElementById('quickDrawer').style.display='block'` 再点 tab。

---

## 2026-10-17 收尾补齐 3：ThumbRig 补齐 `visibilitychange` 性能护栏

### 背景（违反自家护栏）
`AGENTS.md` 第五十四行明确要求「页面不可见（`visibilitychange`）时必须停掉 `requestAnimationFrame`」。
Canvas 粒子引擎遵守了（`lib/client.js:1010` / demo `:3552`），但**任务②新增的两个游标动画循环都漏了**：

- `lib/client.js` `ThumbRig` 的 `useEffect` 里 `step()` 无条件自续帧，`cleanup` 只 `cancelAnimationFrame`
  → 窗口最小化 / 切到别的标签页时 rAF 仍在跑（浏览器会降频但并非停止，且我们每秒仍在做
  浮点物理计算 + `style.transform` 字符串拼接）。
- `demo/index.html:2323` 的 `thumbRigLoop` 同样是首行就 `requestAnimationFrame(thumbRigLoop)`，
  早于所有提前 return。

### 修复（双端，纯增量）

**`lib/client.js`（`ThumbRig`，+39/-2）**
```js
const isHidden = () => typeof document !== "undefined"
  && (document.visibilityState === "hidden" || document.hidden === true);

const onVisibilityChange = () => {
  if (stopped) return;
  if (isHidden()) {
    if (raf) { cancelAnimationFrame(raf); raf = 0; }
    return;
  }
  if (!raf) {
    lastT = 0; // 重新计时，避免恢复瞬间把整段隐藏时长当成一帧
    raf = requestAnimationFrame(step);
  }
};
```
- `step()` 末尾改为：`if (isHidden()) { raf = 0; return; } raf = requestAnimationFrame(step);`
- 订阅 `document.addEventListener("visibilitychange", onVisibilityChange)`，cleanup 里 `removeEventListener`
- 顺带把每帧的 `node.style.transform = ...` / `setProperty("--dcs-thumb-spd", ...)` 加了
  `lastTransform` / `lastSpd` 脏值比对，值没变就不写 DOM

**`demo/index.html`（+10）**
- 新增模块级 `let thumbRigPaused = false;`
- `thumbRigLoop` 首行改为在 `document.hidden` 时不排下一帧并置 `thumbRigPaused = true`
- 已有的 `visibilitychange` 监听里补：恢复可见且 `thumbRigPaused` 时，`thumbRig.lastT = 0` 后重新起转

### 实测（真实 Chrome + CDP，`D:\deepseek\_cdp.mjs`，用 `Object.defineProperty` 覆写 `document.hidden`）

真实宿主插件（`dcs_render_browser.html` 里的真 React 组件）：
```
sample_anim_default     => { present:8, frames:8, uniqueTransforms:8, distinct:true }
visibility_sim          => { ok:true, simulated:"hidden" }
check_frozen_when_hidden=> { frozen:true }      ← 隐藏后 transform 不再变化
restore_visible         => { restored:true }
check_resumed           => { resumed:true }     ← 恢复后重新动起来
```
demo（`demo/index.html`）：
```
open_demo        => { hasThumbBody:true, transform:"translate(0px, -1.3px) rotate(0.15deg) scale(1, 1.03)" }
sample_running   => { frames:6, present:6, unique:6, distinct:true }
force_hidden     => { state:"hidden" }
confirm_frozen   => { frozen:true }
force_visible    => { state:"visible" }
confirm_resumed  => { resumed:true }
```

### 校验
```
node --check lib/client.js                      → exit=0
node scripts/check-undefined.cjs lib/client.js  → ✅ 干净：扫描 21 个全大写标识符
demo 2 个 <script> 块 new Function()            → block1 OK (1840) / block2 OK (406236)
dangling ids                                    → MISSING: NONE（94 声明 / 78 引用）
真实 React 渲染测试（重新生成后跑）              → registered:2 / windowErrors:[] / 7 tab 全 active
                                                  finalNotFunction:[] / finalBoundary:false
编码                                            → lib/client.js 305510 B、demo 478761 B，均无 BOM、纯 LF
```

---

## 2026-10-17 收尾补齐 4：清掉只写不读的死 CSS 变量

### 问题
`--dcs-thumb-spd`（client.js）与 `--thumb-spd`（demo）这两个自定义属性**只被 setProperty 写入，
全仓库没有任何 `var(--dcs-thumb-spd)` / `var(--thumb-spd)` 读取**，
每帧都白做一次 style 写入（且 setProperty 走的是比 `style.transform =` 更慢的路径）。

验证：
```
Select-String -Path lib\client.js,demo\index.html -Pattern 'var\(--dcs-thumb|var\(--thumb' → No matches found
Select-String -Path lib\client.js,demo\index.html -Pattern 'thumb-spd'                   → 2 处，均在 setProperty 侧
```

### 修复
- `lib/client.js`：删掉 `let lastSpd = ""` 与 step() 内的 `nextSpd` 写回块（连带上一轮加的脏值比对）
- `demo/index.html`：删掉 `thumbBody.style.setProperty("--thumb-spd", st.spd.toFixed(3));`

`st.spd` 本身仍在使用（驱动步频、刹车判定、running 动画幅度），只是不再往 DOM 上写。

### 回归（两个最终产物都重跑）
```
真实 React 渲染测试  → registered:2 / windowErrors:[] / 7 tab 全 active / finalBoundary:false
                       sample_anim_default => { present:8, frames:8, uniqueTransforms:8, distinct:true }
                       check_frozen_when_hidden => { frozen:true }
                       check_resumed => { resumed:true }
demo                 → sample_running => { frames:6, unique:6, distinct:true }
                       confirm_frozen => { frozen:true } / confirm_resumed => { resumed:true }
## 2026-10-17 收尾补齐 5：把「思考图标自检」行改成真正的实时预览

### 问题（真实的文案/功能错配）
「🧠 思考」tab 最后一行标题写着 **思考图标自检**，按钮文字却是 **试听音效**，
点击执行的是 `playDialTick()` —— 这是从「🔊 音效」tab 复制粘贴时留下的残骸。
更关键的是：它**什么也没自检**。用户换完图标/动画/颜色后，只有等
宿主真的进入「深度求索中…」才能看到效果，抽屉里没有任何即时反馈。

### 修复（`lib/client.js`，纯增量 +20/-8）
把这一行换成 **思考图标预览**：用与 `buildThinkIconDom()` 完全同源的方式
（`THINK_ICONS[...].svg(safeSvgColor(...))` + `data-anim` + `style.color`）
渲染一枚 `<span class="dcs-think-icon dcs-think-icon-preview">`，
所以换图标、换动画、换颜色都会**立刻**在同一枚图标上生效：
- 自定义图标走 `<img src={config.thinkCustomIcon}>`，与宿主注入分支一致
- `data-anim` 直接取 `config.thinkAnim`，CSS 里的 7 组 keyframes 全部复用
- `style.marginRight = 0` —— `.dcs-think-icon` 的 6px 是给宿主文字旁留的间距，抽屉里多余
- 未新增任何 CSS

### 实测（headless Chrome + 真实 `react-dom/client`，`D:\deepseek\_cdp.mjs`）
```
rowPreview   => { tag:"SPAN", anim:"tail_wag", animName:"dcsThinkTail", dur:"0.86s",
                  iter:"infinite", svgFill:"#4D6BFE", svgViewBox:"0 0 24 24" }
animates     => { a:"matrix(0.993189,0.116514,...)", b:"matrix(0.996822,0.0796601,...)",
                  changed:true }                       # 动画真的在跑，不是静态图标
toSpin       => { anim:"spin", animName:"dcsThinkSpin", dur:"1.6s", timing:"linear" }
toBrain      => { hasSvg:true, animName:"dcsThinkSpin" }   # 换图标后动画保持
colorLive    => { styleColor:"rgb(34, 204, 136)", svgFill:"none" }  # 描边类图标 fill=none 正常
previewMargin=> { marginRight:"0px", w:30 }               # 6px 已归零
tabSwitch    => 离开「思考」再回来，预览行仍在且动画/颜色保持
oldLabelGone => { selfCheck:-1, audition:-1 }             # 旧文案已彻底消失
```

### 校验
```
node --check lib/client.js                      → exit=0
node scripts/check-undefined.cjs lib/client.js  → ✅ 干净：扫描 21 个全大写标识符
真实 React 渲染测试                              → registered:2 / windowErrors:[] / 7 tab 全 active
                                                  finalNotFunction:[] / finalBoundary:false
```

## 2026-10-17 收尾补齐 6：`ICONS.maid_chibi` 别名去重（React 重复 key）

### 问题（真实产品缺陷，非测试假象）
把渲染测试从 React **production** 换成 **development** 构建后（production 会剥掉
prop/children 校验告警，之前「0 告警」是假阴性），页面加载期立刻报：

```
Encountered two children with the same key, `whale_chibi`.
```

根因是 `ICONS` 收尾那行历史别名：
```js
ICONS.maid_chibi = ICONS.whale_chibi;   // 同一对象引用 → 第二个可枚举键
```
而游标页用 `Object.values(ICONS).map(item => ..., key: item.id)` 渲染，
于是同一个对象被遍历出两次，生成**两个 `id` 都是 `whale_chibi` 的按钮**；
标签又都走 `item.name.split(" ")[0]`，两个都显示成「DeepSeek」。

打进 tarball 的也是这份代码 —— 真实宿主里同样会多出一个重复按钮，
所以这是发布前必须修的产品问题。

### 修复（`lib/client.js`，+9/-1）
```js
// 历史别名：老配置里可能还残留 icon:"maid_chibi"。必须设成不可枚举，
// 否则 Object.values(ICONS) 会把同一个对象返回两次 → 游标页多出一个
// 同名「DeepSeek」按钮，React 也会报 "Encountered two children with the same key"。
Object.defineProperty(ICONS, "maid_chibi", {
  value: ICONS.whale_chibi,
  enumerable: false,
  configurable: true,
  writable: true
});
```
`loadSavedConfig()` 里的 `if (saved.icon === "maid_chibi") saved.icon = "whale_chibi";`
保留，老配置照常迁移；别名本身仍在，任何按名取 `ICONS.maid_chibi` 的代码不受影响。

### 实测（`D:\deepseek\_cdp_audit.mjs` + React 19.3.0 development 构建）
```
修复前  iconGrid => { count:11, labels:["DeepSeek","Claude","DeepSeek",...] }
        page load console => 1 条 error: two children with the same key `whale_chibi`
修复后  iconGrid => { count:10, labels:["DeepSeek","Claude","DeepSeek",...] }   # 少一个重复项
        page load console => 0 error / 0 warning（只剩 1 条 React DevTools info）
        altCount => { imgs:1, alts:["鲸鱼娘"] }
```
注：剩下的两个「DeepSeek」标签是 `whale_chibi`（DeepSeek 鲸鱼娘）与
`whale`（DeepSeek 鲸鱼）的首词截断，属既有文案问题，**未改动**（需用户确认 UI 文案）。

### 校验
```
node --check lib/client.js                      → exit=0
node scripts/check-undefined.cjs lib/client.js  → ✅ 干净：扫描 23 个全大写标识符
真实 React dev 渲染 + 7 tab 逐个巡检              → 0 error / 0 warning
```

### 提交
`243c975 fix: ICONS.maid_chibi 别名改为不可枚举，修掉游标页重复按钮与 React 重复 key`

## 2026-10-17 收尾补齐 7：v2.13.0「粉发少女」立绘游标（朝右）

### 需求（用户原话）
> 提取图2的人物模型，做出类似图1的，然后人物模型朝向向右符合向右走，可以和我的插件图标兼容

- 图1 = README 首图（蓝紫轨道上有个 Q 版小人在跑）
- 图2 = 409x522 粉发双马尾少女立绘（粉蓝渐变长发、冰蓝缎带星饰、白×藏青未来风连衣裙、白手套、白色过膝长靴）

### 产出（两个 base64 常量 + 一个 ICONS 条目 + 一种新皮肤）
| 资产 | 尺寸 | 用途 |
|---|---|---|
| `CHIBI_HERO_ART` | 218×361 PNG，b64 8588 | 立绘皮肤用的全身小人（朝右奔跑） |
| `CHIBI_HERO_ICON` | 128×128 PNG，b64 14208 | 图标网格 / 抽屉头像的圆形半身像 |

生成管线在仓库**外部**：`D:\deepseek\_hero_sprite\gen_hero.py`（PIL 手绘，S=8 超采样）
+ `export_assets.py`（`trim` + 48 色 FASTOCTREE 量化 + 写 `.b64`）。
关键：**半身像单独画**（`render_bust()`），不能从跑步帧裁 —— 双马尾向后拉出 50 个单位，
任何裁切都无法居中。

### 代码改动（`lib/client.js`，全部增量）
1. `CHIBI_HERO_ART` / `CHIBI_HERO_ICON` 两个常量，紧跟在 `CHIBI_MAID_AVATAR` 之后。
2. `ICONS` 新增 `hero_chibi`：`{ id, name:"粉发少女 朝右", art: CHIBI_HERO_ART, svg: 18px 圆形 <img> }`。
   位于 `whale_chibi` 之后、`claude` 之前 → 图标网格里排第二位。
3. `DEFAULT_CONFIG.thumbSkin` 注释加 `"art"`；`loadSavedConfig()` 白名单加 `saved.thumbSkin !== "art"`。
4. `ThumbIcon` 新增分支：`if (config.thumbSkin === "art" && item?.art) return <img class="dcs-thumb-art">`。
5. 抽屉「游标皮肤」三选一：`art` / `bare` / `bubble`。
6. thumb 节点改成 IIFE，`isArt` 时 `boxShadow: void 0`，className 追加 `is-art`。
7. 新增 CSS：`.dcs-thumb.is-art`（背景/边框/圆角/阴影全部清空）、`.dcs-thumb-art`
   （绝对定位 + `bottom:0` + `height:44px`）、`.dcs-thumb.is-art .dcs-thumb-body { transform-origin: 50% 100% }`
   （摆动轴落在脚底）、`.is-max-thumb .dcs-thumb-art`（Max 光晕改画在人物剪影上）。
   **注意：不要覆写 `transition`** —— 会丢掉 `left` 的缓动，游标变瞬移。

### 踩过的坑（都已在代码里留注释）
- 手柄本体的 `box-shadow: 0 0 0 2px #ffffff` 会在人物脚下浮出一个空心圆角方块 →
  必须 `box-shadow: none !important` **且不加 `:not()` 条件**，否则 Max 态漏网。
- `translateY(4px)` / `translateY(-10px)` 都是错的（在 `place-items:center` 的 grid 里会往下溢出），
  正解是 `position:absolute; bottom:0` 让底边贴着手柄底。
- `transform-origin: 50% 76%`（插件默认）在人身上落在腰部，跑动时像在飘 → 改到 `50% 100%`。
- demo 的 `.slider-thumb` 与插件 `.dcs-thumb` 是两套独立 CSS，改动要各写一份。

### demo 同步（`demo/index.html`，4 处）
常量（`CHIBI_HERO_ICON` 同步为新的 128px 版）、`ICONS.hero_chibi`（`render()` 返回 HTML 字符串）、
`let thumbSkin` 注释、`updateThumbIcon()` 的 `art` 分支、`syncThumbSkin()` 的 `is-art` toggle、
CSS（`.slider-thumb.is-art` / `.thumb-art-img` / `transform-origin`）。
图标网格由 `Object.values(ICONS).map()` 自动生成，无需单独改网格代码。

### 校验（全部通过）
```
node --check lib/client.js                      → exit=0
node scripts/check-undefined.cjs lib/client.js  → ✅ 干净：扫描 23 个全大写标识符
demo 两个 <script> 块 node --check              → 1840 chars OK / 429808 chars OK
CRLF / BOM（两个文件）                          → 均无
真实 React dev 渲染（D:\deepseek\_render_hero4.cjs）
  thumbInfo => [{ cls:"dcs-thumb is-free is-art", imgCls:"dcs-thumb-art",
                  srcLen:8610, rect:[223,637,28,28] }]
  iconBtns  => 11 个，粉发少女 imgLen:14230 sel:true
  registered:2 / errs:[]
```
截图确认：深色面板里粉发少女站在轨道上、**面朝右**、双脚踩轨道下沿；
图标网格里她的圆形半身像与鲸鱼娘并列显示正常。

### 文档
`README.md`：Q 版游标动画段落改为「三种皮肤」；游标图标 `10 款` → `11 款`，说明立绘皮肤用法。



