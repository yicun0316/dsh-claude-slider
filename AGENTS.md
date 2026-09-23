# AGENTS.md — dsh-claude-slider 修改纪律

> 这份文件是给 AI 编码助手（Antigravity / 其他 agent）看的**硬约束**。
> 项目背景：这是一个 DSH（DeepSeek Harness）客户端插件，核心是 `lib/client.js`（单文件、约 5000 行、手写未压缩的 Canvas + React 代码）。

## 一、最重要的三条（曾经因此出过事故）

1. **禁止整文件重写。**
   不允许 `write_to_file` 覆盖 `lib/client.js` 或 `demo/index.html`。
   只允许**增量修改**（`replace_file_content` / `str_replace` / 精确 patch）。
   *事故记录：2026-09-23，一次整文件重写把 `EFFORT_DESCRIPTIONS`、`CUSTOM_PARTICLES`、`CUSTOM_MOTIONS`
   三个模块级常量连同定义一起删掉，只留下引用，导致「推理调节组件异常：… is not defined」。*

2. **禁止删除文件。**
   需要清理任何文件（脚本、临时产物、图片）时，先列出完整清单并说明理由，等用户确认后再动。

3. **不认识的东西不要动。**
   如果你不确定某个常量/函数是干什么的，先在文件里搜它的引用，理解了再改；不要因为"看起来没用"就删。

## 二、每次修改的标准流程

1. 改之前先读（`view_file`）确认当前版本，不要凭记忆。
2. 只改用户指定的部分，不顺手重构、不顺手改名。
3. 改完**必须**跑这两个检查，并把输出贴出来：
   ```bash
   node --check lib/client.js
   node scripts/check-undefined.cjs lib/client.js
   ```
   第二个脚本专抓"引用了但没声明的大写常量"——就是上面那类事故。
4. 报告 diff 摘要：改了哪几行、为什么、影响哪个功能。
5. 提醒用户 `git commit`（本仓库有 git，任何一次改动都应该留下痕迹）。

## 三、必须保留的模块级定义（禁止删除或改名）

| 名称 | 作用 |
|---|---|
| `EFFORT_DESCRIPTIONS` | 档位算力预算与释义（悬浮胶囊用），键：off/low/medium/high/max |
| `CUSTOM_PARTICLES` | 客制动效的 10 种粒子形态，id 必须与 CanvasEffect 的绘制分支一一对应 |
| `CUSTOM_MOTIONS` | 客制动效的 8 种运动动力学，id 必须与 CanvasEffect 的运动分支一一对应 |
| `EFFECT_MODES` | 全部动效模式（id/name/family），是设置面板与家族筛选的唯一数据源 |
| `LEGACY_EFFECT_MAP` | 旧版本 effect id → 新 id 的迁移映射，删了会让老用户配置失效 |
| `CONFIG_KEY` | localStorage 配置键（当前 `dsh-claude-slider.config.v2`） |

## 四、动效相关的约定

- **id 是契约**：动效 id 一旦发布就不能再改。要改名，就新增 `LEGACY_EFFECT_MAP` 条目，把旧 id 映射到新 id。
- **新增一个动效，必须同时改 4 处**：
  1. `EFFECT_MODES`（id / 中文名 / family）
  2. `CanvasEffect` 里的绘制分支
  3. `CURATED_COMBOS`（如果要进"灵感搭配"）
  4. `demo/index.html`（离线演示页）
- **性能护栏**（别突破）：
  - 粒子数按档位分预算（低档少量、MAX 才放开），复用预分配池，不要每帧 `new`
  - 渐变对象尽量预建或缓存，不要每帧大量创建
  - `globalCompositeOperation` 只在深色主题用 `lighter`；浅色主题必须回到 `source-over`
  - 高频闪烁频率 < 3Hz；尊重 `prefers-reduced-motion`
  - 页面不可见（`visibilitychange`）时必须停掉 `requestAnimationFrame`

## 五、禁止引入的东西

- ❌ 不要写 `build_vNN.cjs` / `apply_vNN.py` / `rewrite_*.py` 这类"脚本改源码"的工具。
  直接在 `lib/client.js` 里做精确编辑。历史上这类脚本已经堆到 v29，最后把项目搞得无法 diff、无法回滚。
- ❌ 不要引入构建步骤（打包器 / 转译器 / TS）。当前插件是零构建、直接加载 `lib/client.js`。
- ❌ 不要在插件里发网络请求、读写用户文件、申请额外权限。

## 六、长对话之前

上下文被压缩后你会丢失细节。开始一段长工作前，先把当前状态写进 `STATUS.md`
（动效清单、待办、已确认的设计决策、已知 bug），并**以文件为准**，不要依赖记忆。
