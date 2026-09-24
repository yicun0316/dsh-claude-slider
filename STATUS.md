# STATUS.md — 当前状态快照

> **给 AI agent 的用法**：上下文被压缩/丢失后，以这份文件为准确来源，不要凭记忆推断。
> 每次做较大改动后更新对应条目。

_最后更新：2026-09-24 16:03_

## 一、项目是什么

DSH（DeepSeek Harness）客户端插件 `dsh-claude-slider`：把推理强度（reasoning effort）的选择
做成 Claude 风格的滑块，并附带一整套 Canvas 动效、主题配色、手柄图标与音效。

- 形态：**零构建**、单文件客户端插件（`lib/client.js`，现约 6.5k 行）
- 演示页：`demo/index.html`（约 10k 行，自带 `.demo-*` 样式与独立 DOM 滑块，非 React 挂载）
- 装载方式：通过 `dsh plugin --profile desktop add link:<本目录>` 软链接进 profile
- 仓库：https://github.com/yicun0316/dsh-claude-slider （已创建，`main` 分支）
- 存储：配置写在 `localStorage`，键 `dsh-claude-slider.config.v2`
- 网络：**零请求**；不读写用户文件（图标上传仅走本地压缩后存 localStorage）

## 二、功能清单（截至本快照）

### 动效：14 款精选纯净动效，分 5 个家族

| 家族 | 成员 |
|---|---|
| 🚀 推进 rocket | 龟派气功 `kamehameha`、火箭尾焰 `rocket_thrust`、超载折跃 `warp_boost` |
| 🌊 流体 fluid | 玻璃水银 `liquid_mercury`、火山喷发 `volcano_magma` |
| 🌸 幻境 nature | 落樱春水 `sakura_flutter`、极光织锦 `aurora_veil`、深海鲸跃 `deep_whale`、萤火微光 `firefly_swarm`、落雪狂沙 `snow_sandstorm` |
| 💻 科技 tech | 频谱律动 `spectrum_bars`、雷达扫描 `radar_sweep` |
| 🎨 质感 art | 星流碎钻 `jet_stream`、流金星河 `chrono_gold` |

> 2026-09-24 重大升级：原生液态玻璃抽屉重构与透明度调节 + 设置中心极简适配
> - **第一张图（输入框上方快捷调控抽屉 QuickDrawer）重构**：
>   - **原生磨砂液态玻璃质感**：`backdrop-filter: blur(36px) saturate(190%)`，透光卡片结合 `--glass-opacity` 动态变量，高光描边、平滑圆角 `border-radius: 20px`，斜向微光流转动效 (`@keyframes dcsLiquidSheen`)；
>   - **玻璃透明度动态调节**：在「外观」与「调校」中提供「玻璃透明度」发光滑块（10% ~ 100%），抽屉背景透明度实时联动；
>   - **下架旧定制动效入口**：彻底移除抽屉内的「✨ 定制动效」横幅与旧微元调节器，保持纯净；
>   - **修复游标图标点击崩溃**：修复 `item.svg` 与 `item.render` 属性兼容，点击「游标」标签安全平滑渲染，杜绝任何报错崩溃与页面消失；
> - **第二张图（DSH 设置中心 ClaudeSettingsPage）极简重构**：
>   - **严格按照用户需求收敛**：去除非必要的 6 标签页，**只保留滑块总开关与主题模式适配**；
>   - **滑块主开关**：「高级推理滑块调节」极简胶囊开关，控制滑块开启或恢复 DSH 原生设计；
>   - **三档外观模式自适应**：「☀️ 浅色模式」、「🌙 深色模式」、「💻 跟随系统」，通过 `useResolvedTheme` 实时监听系统/应用深浅色属性，深度完美适配；
>   - **状态质感预览**：实时显示当前生效的模式及快捷操作指引。

> 2026-09-23 精简：下架 9 款（`ion_stream` / `surging_current` / `data_stream` / `circuit_pulse` /
> `cyber_pulse` / `ink_wash` / `silk_ribbon` / `dot_matrix_wave` / `contour_lines`），
> 它们的 id 已在 `LEGACY_EFFECT_MAP` 中做了重定向（如 `cyber_pulse → chrono_gold`、
> `circuit_pulse → radar_sweep`），老用户配置不会失效。
> `chrono_gold` 此前**只有注释没有绘制分支**（一直走兜底），本次已补上真实实现。

### 档位三阶递进（本次新增的核心机制）

渲染循环由填充比例派生出三阶权重，**逐档解锁视觉层**（不是"量变"，低档严格为 0）：

```js
const tierT = currentRatio * 3;                       // demo 中为 renderedRatio
const L1 = Math.min(1, Math.max(0, tierT));           // Low  解锁：基础层
const L2 = Math.min(1, Math.max(0, tierT - 1));       // High 解锁：结构层
const L3 = Math.min(1, Math.max(0, tierT - 2));       // Max  解锁：高能层
```

- **L1 基础层**：主体形态 + 主题色底衬 + 主粒子
- **L2 结构层**：全轨高光脊线 + 上下边缘细描边 + 匀速掠过的扫描光带，
  以及**各效果自己的次级元素**（火箭的马赫激波环、落樱的水波涟漪、频谱的柱顶白帽、
  水银的折射条纹、雷达的回波点、极光的补幕与星点、鲸跃的上升气泡、萤火的拖尾、
  落雪的额外阵风、火山的熔岩泡、流金的额外细丝）
- **L3 高能层**：全轨泛光 + 12 道旋转能量射线 + 18 颗环绕火花 + 3 道扩散脉冲环 +
  边缘流转光晕，各效果同时进入终极形态
- **切入 Max 瞬间**：径向冲击波 + 全轨高光冲洗（原有的 burst 机制）
- 粒子预算约 6 → 18 → 60 → 128；`speedBoost = 1 + L1*0.12 + L2*0.22 + L3*0.46 + burst`

> 实现位置：三阶权重在渲染循环前置（两个文件各自一份，**不参与 graft 同步**）；
> 共用附加层放在效果分发链之后、爆发特效之前；逐效果追加层写在各自分支体末尾。
> 统计：`L2 > 0.01` 与 `L3 > 0.01` 各 14 处（13 款 + 1 处共用层）。

### 随机灵感搭配（洗牌袋）

- `CURATED_COMBOS`：**13 套**，每款效果各配一套专属的主题色 / 手柄图标 / 流速 / 辉光
- 抽取用**洗牌袋**（`shuffleList` 打乱 → `pop()` → 抽空才重洗）：
  连续 13 次会把 13 款各抽到一次、绝不重复；重洗后若首抽与上轮末尾相同则与中间一项对调；
  另有一道"绝不与当前展示效果相同"的兜底
- 实测：26 次连抽 → 每轮 13 次 `dup=0`、相邻重复 `0`、配色变化 12 种

### 动效背景介质（液态玻璃与高斯模糊，独立开关）

- **🧊 液态玻璃 (`liquidGlass`)**：高透微晶胶囊轨道，包含顶部高光镜面反光导轨、内部流动光斑焦散以及微晶反光内描边。默认关闭（`false`），随开随关，与当前所选的任何动效有机叠合。
- **🌫️ 高斯模糊 (`gaussianBlur`)**：轨道漫射辉光雾化介质，通过双层环境光雾在滑块轨道四周形成柔光晕染。默认关闭（`false`）。

### 液态玻璃工坊与预设导入导出系统

- **3 标签页结构**：
  1. **📥 导入动效**：支持文本框粘贴、从剪贴板一键读取，具备**实时配置识别徽章**（即时预览预设名称、动效、联动色、速度倍率与介质开关），并内置「⚡ 极速霓虹」、「🔮 量子折跃」、「🌊 幽海潮涌」、「🌸 绯樱之舞」、「💥 龟派神光」等精选试玩预设。
  2. **📤 导出分享**：一键生成纯净易读的 JSON 预设配置，支持一键复制到剪贴板，方便跨设备或与好友即时分享。
  3. **💡 制作教程与标准模板**：详细列出支持的 7 项字段属性定义、类型与说明，并提供一键式「📋 复制此模板并进入导入」按钮，新手零门槛上手。

### 其他

- 档位：off / low / high / max（DeepSeek 适配器实际只有这四档；表里保留 medium 供其他 provider）
- 算力预算释义：`EFFORT_DESCRIPTIONS`
- 流速倍率 / 辉光倍率 / 全家桶配色（9 预设 + 全色谱拾色器）
- 手柄图标：官方矢量图（Claude 星芒 / DeepSeek 鲸鱼 / 鲸鱼娘）+ Emoji + 本地图片上传（Canvas 压缩到 96×96）
- 音效：Web Audio 合成（杂鱼 / 哦鲸鲸 / 小黄鸭 / 机械触感 / 自定义）
- 迁移：`LEGACY_EFFECT_MAP` 把历代旧 id 映射到现行 id（**不要删**）

## 三、工程护栏（已实现，勿回退）

- 帧率无关动画：`time += 0.035 * dt * speed`（`speed` 现由 `speedBoost` 按档位给出）
- **0 档休眠**：填充比例 < 0.005 时清空画布并**停止 RAF**；只能靠
  `pointermove / pointerdown / keydown / visibilitychange / focus` 唤醒
  （⚠️ 截图/自动化脚本注意：设成 Off 后不派发交互事件，画布会一直空白）
- 不可见即暂停：`visibilitychange` + 清理
- 无障碍：`prefers-reduced-motion` 命中时降级
- 混合模式：`globalCompositeOperation` 仅深色用 `lighter`，浅色回 `source-over`
- 粒子预算按档位分档；`devicePixelRatio` 上限 2
- 改动后必须跑：`node --check lib/client.js` 与 `node scripts/check-undefined.cjs lib/client.js`

## 四、已修复的事故（供追溯）

| 日期 | 症状 | 原因 | 处理 |
|---|---|---|---|
| 2026-09-23 | 「推理调节组件异常：EFFORT_DESCRIPTIONS is not defined」 | 整文件重写时连同定义一起删掉，只剩引用 | 补回 `EFFORT_DESCRIPTIONS`；并预修同类地雷 `CUSTOM_PARTICLES` / `CUSTOM_MOTIONS` |
| 2026-09-23 | `demo/index.html` 打开后完全无交互、画布永久空白 | ① 6943~7008 行混入插件 CJS 打包片段（含顶层 `return module.exports` 与游离 `});`）→ 整段脚本 SyntaxError；② 7009~7287 行是音频模块旧副本，与正本重复声明 6 个 `const`；③ 缺宿主注入的 `react` / `h` 全局，脚本在 `class ... extends react.Component` 处中断；④ `animLoop` 里 `brightness`（应为 `selectedBrightness`）与未声明的 `speedMultiplier` → 首帧抛错，RAF 永久停止 | ① 注释隔离游离块；② 两份重复声明统一降级为 `var`；③ 加入仅在缺失时生效的兼容层；④ 修正变量名 |
| 2026-09-23 | demo 效果面板是无样式的默认按钮、筛选按钮也不成胶囊 | 第 925 行 `.quick-tool-btn {` **少了闭合 `}`**，CSS 解析器把第 956 行之后约 20 条规则整块吞掉（该缺陷在最早备份中即存在） | 补上 `}`，样式表规则数 128 → 150 |
| 2026-09-23 | demo 里「🎲 随机」从不改变配色 | 写的是 `selectedColor`，该变量在 demo 中从未声明（隐式全局），真正生效的 `selectedAccentColor` 未被更新 | 改为调用 `applyAccentColor(pick.color)` |
| 2026-09-23 | 「随机动效重复率很高，点两下就出现之前的」 | ① 随机池 `CURATED_COMBOS` 只有 6 套，13 款里有 7 款根本抽不到（6 选 1 相邻重复概率约 17%）；② 插件侧只排除"完全等于当前组合"的项，demo 侧完全没有去重 | 池子扩到 13 套 + 改为洗牌袋抽取 |
| 2026-09-24 | 「插件呢，怎么点一下就没了」 | ① `SliderErrorBoundary` 组件类在重构中遗失只剩引用，点击「推理 Max」弹窗时调用 `h(undefined)` 触发致命 React 运行时抛错，宿主槽位捕获崩溃卸载组件回退到 DSH 原生 `DeepSeek-V41-Flash Max ▾`；② 设置中心关闭滑块或误触开关时，回退视图未提供重新启用按钮 | ① 补全 `SliderErrorBoundary`，并在根部注入 `ClaudeModelSelectErrorBoundary` 双层坚固护栏；② 回退模式与设置页增加「⚡ 开启滑块」及一键恢复按钮，状态清晰标注 |
| 2026-09-24 | 「只留一个可以调整背景透明度开关，然后优化一下过渡」「就是第一个框和第二个框」 | ① 弹窗由外层容器 `.dcs-popover`（第一个框）和内层抽屉 `.dcs-quick-drawer`（第二个框）双层叠加，边框阴影重复嵌套；② 抽屉「外观」与「调校」两个标签页各有一个透明度滑块造成冗余；③ 拖拽滑块时背景带 `transition: background` 引发掉帧抖动；④ 浅色与低透明度下缺少文字对比度衬底 | ① 样式层面消除内层边框与背景，外层与内层融为一体纯净单框（Single Liquid Card）；② 收敛透明度控制：只在「外观」保留单一「背景透明度」发光滑块，移除冗余控制；③ 移除拖拽时背景渐变动画实现 0 延迟跟手，加入弹簧展开动画 `dcsDrawerReveal` 与低透明度文字抗干扰投影 |
| 2026-09-24 | 「调校里面加入动效亮度调节，把这个随机对齐，把制作模板删除」 | ① 调校面板缺少动效自身辉光强度的调节滑块；② 抽屉头部分段标签栏继承了 `margin-bottom: 20px`，导致「🎲 随机」按钮和关闭按钮在 Flex 布局中被挤压下沉下垂，且缺少 `white-space: nowrap` 导致汉字单字垂直拆开折行；③ 工坊弹窗中的「💡 制作教程与模板」占用过多垂直空间干扰用户日常体验 | ① 在「⚡ 调校」页加入「动效亮度」调节滑块（0.5x ~ 2.0x），精准联动粒子/光效辉光；② 彻底重构抽屉顶栏布局：清空误继承的 bottom margin，将 6 个标签页与「🎲 随机」按钮统一重构为上下图标+双字标签胶囊卡片（高度严格锁定 42px，垂直基线 100% 齐平，杜绝任何汉字单字换行与下垂）；③ 彻底删除工坊弹窗与抽屉工坊内的「💡 制作教程与模板」标签页及关联代码模板，保持工坊仅保留「📥 导入动效」与「📤 导出分享」 |
| 2026-09-23 | 批量改分支时把新旧代码混在一起导致语法报错 | ① 批量替换用了一次性算好的行号，前一款变长后后面全部偏移；② `find_headers` 用 `\s*\} else \{\s*$` 收集分支边界，把**分支体内部的嵌套 `} else {`** 也算进去了 | 每次替换前重算行号；分支边界只认真正的分支头，默认分支用"下一行含 `const bg = ctx.createLinearGradient`"严格判定 |

修复前的完整备份都在 `_backups/`（该目录已被 .gitignore 排除）。

## 五、待办

- [x] 本机绝对路径已从仓库文件中清除（README 重写时移除）
- [x] 补齐 `LICENSE`（MIT）+ README「非官方插件」免责声明 + 给外部用户的安装命令
- [x] 上传 GitHub（仓库已创建：`yicun0316/dsh-claude-slider`）
- [x] README 的动效名单与代码同步（现为 5 大类共 13 款，并补了档位递进与随机机制说明）
- [ ] `demo/index.html` 与 `lib/client.js` 的渲染分支需要人工保持同步。
      **注意**：本次是用仓库外的脚本（`patch_*.py` + `graft2.py`）做的批量同步，
      这与 AGENTS.md 第五节「不要写脚本改源码的工具」相抵触——脚本没进仓库，
      但下次改动建议回到 `lib/client.js` 直接精确编辑，或先把同步方案确认清楚。
- [ ] 效果 id 已冻结；今后只允许通过 `LEGACY_EFFECT_MAP` 改名
- [ ] npm 发布（包名 `dsh-claude-slider` 在 npm 上仍为空闲）
- [ ] 可选：给 demo 加入「档位递进」的自动化回归脚本（现有关卡：Off 档会休眠，脚本必须先派发 `pointermove`）

## 六、已知问题 / 可继续做的方向

- 「落樱春水」的花瓣仍是左右对称的贝塞尔"叶形"，缺少樱花顶端缺口
- 「火山喷发」完全跟随主题色，蓝色主题下会退化成"雪山"观感
- 「幽夜暗潮」类的水流感效果已下架，如需可参考 `_backups` 里的旧实现
- 粒子池 `genericParticles` 的 `x` 仍按 0~360px 初始化；已改造过的效果都用归一化
  `relDist` 规避了高 DPI 下的左侧堆积，未改造的少数效果仍受影响
- 早期评审记录见工作区 `动效评审报告.html`（对应 22 款时代，仅作历史审计）
