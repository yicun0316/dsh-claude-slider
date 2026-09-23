# dsh-claude-slider

DeepSeek Harness (DSH Desktop & Web) 的推理强度调节滑块插件。  
将默认的思考模式/推理强度下拉选择器替换为横向滑块交互，并提供动效、音效、图标及参数自定义功能。

![DSH Claude Slider 界面演示](https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/demo.png)

---

## ✨ 动效实机效果展示

所有动效均在 DSH 客户端中基于原生 Canvas 实时渲染，粒子形态与流光跟随档位及自选主题色动态演色。  
优化截图与多任务交互体验：使用系统截图（`Win + Shift + S` / 微信截图 / QQ截图 / Snipaste）或窗口失焦时，粒子持续运转，绝不定格。

| 动效类型 | 实机运行实测截图 | 特性与粒子说明 |
| :--- | :---: | :--- |
| **🌊 玻璃水银**<br>`(Liquid Mercury)` | <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/effect_mercury.png" width="480" alt="玻璃水银实测截图" /> | 多层液态金属高光波涌、旋转多面玻璃晶片棱镜、十字星芒闪烁 |
| **🌸 落樱春水**<br>`(Sakura Flutter)` | <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/effect_sakura.png" width="480" alt="落樱春水实测截图" /> | 绯粉水波渐变漫射、贝塞尔自转翻滚花瓣微元、随波翻腾与涟漪扩散 |
| **⚡ 科技流光**<br>`(Tech Stream)` | <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/effect_tech.png" width="480" alt="科技流光实测截图" /> | 高亮等离子流光、矩阵粒子微元高速推进、动态外发光晕染 |

---

## 🔊 档位吸附音效展示

滑块切换档位吸附时即时触发发声，支持在【调校】页面中独立调节音量大小（0% ~ 150%）或一键静音。

![音效展示卡片](https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/sound_showcase.svg)

### 在线试听与音频

| 音效名称 | 台词 / 声效 | 风格特色 | 试听与音频文件 |
| :--- | :--- | :--- | :--- |
| **🐟 杂鱼 (Zako)** | `ざぁ～こ♡ ざぁ～こ♡` | 傲娇反差萌嘲讽声线 | <audio src="assets/sounds/zako.mp3" controls preload="none"></audio><br>[▶ 试听 / 下载 zako.mp3](assets/sounds/zako.mp3) |
| **🐳 哦鲸鲸 (Ochinchin)** | `お～ちんちん♡` | 软萌声线，DeepSeek 谐音梗 | <audio src="assets/sounds/ochinchin.mp3" controls preload="none"></audio><br>[▶ 试听 / 下载 ochinchin.mp3](assets/sounds/ochinchin.mp3) |
| **🐥 小黄鸭** | `嘎啾~ 嘎啾~` | 经典捏橡皮鸭解压声 | *内置 Web Audio 双谐波物理声学合成* |
| **⚙️ 机械微触感** | `咔哒` | 高频物理齿轮拨动阻尼微触感 | *内置 Web Audio 物理声学合成* |
| **📁 本地自定义音频** | 用户本地音频 | 支持上传任意 MP3 / WAV 作为音效 | *本地持久化存储与极速发声* |

---

## 🎨 全局色彩联动与自定义拾色展示

插件提供 **9 款专属预设主题色**，并内置**原生 Hex 拾色器**。  
色彩调整不仅作用于滑块轨道与手柄，更与动效引擎深度联动——**流光粒子、喷流羽羽、冲击波与背景辉光将同步演色**，绝非仅修改单一外边框。

![主题色彩与动效联动展示](https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/color_showcase.svg)

| 色彩类别 | 包含颜色 / 功能 | 联动效果说明 |
| :--- | :--- | :--- |
| **预设主题色 (9 款)** | DeepSeek 蓝 (`#4D6BFE`)、幻海晶青 (`#00F2FE`)、Claude 暖陶 (`#D97706`)、Claude 曜金 (`#F59E0B`)、极客翠绿 (`#10B981`)、暗夜幽紫 (`#8B5CF6`)、蔷薇绯粉 (`#F43F5E`)、烈焰赤橙 (`#FF6B4A`)、冷月珠光 (`#E2E8F0`) | 一键应用，所有动效主色调与环境光晕瞬时全局同步切换 |
| **原生 Hex 拾色器** | 任意 16 进制颜色代码（如 `#FF0055`）或点击色盘直选 | 自动计算色彩亮度，动态生成流光渐变与粒子半透明透明度分层 |

---

## ⚡ 调校控制台展示（音量 / 流速 / 亮度）

在【调校】页面中配备三大无极微调滑块，所有调整**毫秒级实时生效**，无需重载或重启客户端。

![调校控制台展示](https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/tuning_showcase.svg)

| 调节参数 | 可调范围 | 默认数值 | 交互与特性 |
| :--- | :--- | :--- | :--- |
| **🔊 吸附音量大小 (Volume)** | `0%` (完全静音) ~ `150%` (高增益放大) | `100%` | 拖拽滑块松手即自动发声试听；提供独立【试听】按钮与一键【复位 100%】 |
| **⚡ 动效流速倍率 (Speed)** | `0.2x` (极缓流淌) ~ `2.5x` (高速推进) | `1.0x` | 实时控制粒子飞行速度与波涌频率；提供一键【复位 1.0x】 |
| **💡 辉光渲染亮度 (Brightness)** | `0.4x` (克制幽暗) ~ `2.2x` (高亮爆发) | `100%` | 调节 Canvas 画布发光核心透明度与 CSS 发光晕染强度；提供一键【复位 100%】 |

---

## 功能列表

### 1. 推理强度控制
- **档位调节**：支持模型预设档位（如 Off / Low / High / Max）的拖拽调节与即时吸附。
- **点击直达**：点击滑块轨道的点或下方档位名称可直接切换。
- **原生兼容**：在调校面板或系统设置中提供总开关；关闭后自动还原为 DSH 默认的下拉菜单。

### 2. 视觉动效
- **预设动效分类**（5 大类，共 19 款）：
  - **推进**：火箭尾焰、离子飞箭、超载折跃
  - **流体**：幽夜暗潮、玻璃水银、火山喷发
  - **幻境**：落樱春水、极光织锦、深海鲸跃、萤火微光、落雪狂沙
  - **科技**：频谱律动、数据矩阵、雷达扫描、电路脉冲、赛博霓光
  - **质感**：水墨飞白、柔光丝缕、点阵起伏、等高拓扑、流金星河
- **定制动效**：支持自定义混搭，提供**一键启用 / 点击禁用还原**开关：
  - 点击“✨ 定制动效”卡片即可启用并展开混搭面板；再次点击即可禁用并平滑回退至之前选中的预设动效。
  - 粒子微元形态（10 种）：炽焰、晶体、星芒、圆点、光雾、花瓣、弧光、气泡、霓虹、碎片
  - 流动运动轨迹（8 种）：推进、星流、对撞、波涌、涡旋、跃迁、爆发、环绕
- **全局色彩联动**：动效粒子与光效颜色跟随用户选择的主题色实时同步变化。

### 3. 分类栏交互
- **拖拽滑动**：支持鼠标在分类栏任意位置按住左右拖动，带指针锁定与防误触判定。
- **滚轮横滚**：鼠标悬停在分类栏上时，鼠标滚轮可直接横向滚动。
- **微翻页控制**：分类栏两侧设有 `‹` 和 `›` 按钮，点击可翻动分类。
- **自动居中**：切换或点击某个大类时，该标签自动平滑滚动至视口中央。
- **轻扫切换**：在动效卡片网格区域左右滑动即可切换上一类或下一类。

### 4. 档位吸附音效与音量调校
- **音量调节**：提供 0% ~ 150% 独立音量滑块，支持拖拽即时试听、独立【试听】按钮与一键【复位】为 100%。
- **开关控制**：可随时开启或关闭吸附音效。

### 5. 个性化调校
- **动效流速**：可调节范围 0.2x ~ 2.5x，支持一键复位为 1.0x。
- **光效亮度**：可调节范围 0.4x ~ 2.2x，支持一键复位为 100%。
- **色彩选择**：内置 9 种预设主题色，同时支持原生 Hex 取色器自定义颜色。

### 6. 手柄图标
- **内置图标**（10 款）：DeepSeek 鲸鱼娘、Claude 官方星芒、DeepSeek 官方鲸鱼、超级大脑、闪电脉冲、量子原核、炽热烈焰、璀璨宝石、灵动星火、精准瞄准。
- **自定义图标**：支持上传本地图片（PNG / JPG / SVG）或直接输入 Emoji 作为手柄图标。

### 7. 配置导入与导出
- **导出**：将当前所有动效、色彩、速度、亮度、图标及音效设置导出为 JSON 文本。
- **导入**：支持从剪贴板或输入框粘贴 JSON 配置并一键应用。

### 8. 性能优化与截图保障
- Canvas 渲染节流，手柄拖拽零延迟。
- 鼠标离开无交互 1.5 秒后自动降低渲染帧率休眠，减少后台 CPU/GPU 占用；鼠标移入即时唤醒。
- **截图与失焦不冻结**：唤起系统截图覆盖层（`Win+Shift+S` 等）或失焦时绝不暂停，确保动效连贯展现。

---

## 📦 安装与使用

### 方式一：命令行一键安装（推荐）

在终端（PowerShell / CMD / Terminal）中直接执行以下命令：

```bash
# 安装到桌面版 (Desktop Profile)
dsh plugin --profile desktop add github:yicun0316/dsh-claude-slider

# 或安装到网页版 (Web Profile)
dsh plugin --profile web add github:yicun0316/dsh-claude-slider
```

安装完成后，打开或切换到 DSH 窗口，按下 **`Ctrl + R`** 重新加载即可生效！

> [!NOTE]
> **安全说明**：装任何插件都等于在你的机器上跑第三方代码，权限与用户本人相同（能读写文件、使用模型凭据、访问网络）。本项目 100% 开源且不传输任何隐私数据。如需锁定特定版本，可在末尾添加 commit 哈希（例如 `github:yicun0316/dsh-claude-slider#fa9cc70`）。

---

### 方式二：在 DeepSeek Harness 里通过 dsh-market 安装

如果你的 DSH 已经安装了社区应用市场 `dshmarket`，可以直接在界面内搜索 `dsh-claude-slider` 一键点击安装。

> 若尚未安装插件市场，可先通过命令启用插件市场：
> ```bash
> dsh plugin --profile desktop add dshmarket
> ```

---

### 方式三：本地开发者模式（源码挂载）

1. **一键挂载**：克隆本仓库后，双击运行项目根目录的 `install.bat`，自动创建软链接到 DSH 插件目录；
2. **刷新生效**：在 DSH 客户端中按下 `Ctrl + R` 重新加载；
3. **本地纯浏览器预览**：直接双击打开 `demo/index.html`，无需启动 DSH 即可全功能调试。

---

### 卸载插件

```bash
# 从桌面版卸载
dsh plugin --profile desktop remove dsh-claude-slider

# 从网页版卸载
dsh plugin --profile web remove dsh-claude-slider
```

---

## 项目结构

```
dsh-claude-slider/
├── package.json          # 插件信息与版本定义
├── cordis.patch.yml      # DSH 插件插槽声明
├── assets/               # 真实界面截图与矢量展示资源
│   ├── demo.png          # 实际运行界面实测截图
│   ├── effect_mercury.png# 玻璃水银实机实测截图
│   ├── effect_sakura.png # 落樱春水实机实测截图
│   ├── effect_tech.png   # 科技流光实机实测截图
│   ├── sound_showcase.svg# 音效系统矢量展示卡片
│   ├── color_showcase.svg# 主题色彩联动展示卡片
│   ├── tuning_showcase.svg# 调校控制台（音量/流速/亮度）展示卡片
│   └── sounds/           # 独立音频文件（zako.mp3, ochinchin.mp3）
├── lib/
│   ├── index.js          # 插件服务端入口
│   ├── client.js         # 客户端核心实现（滑块组件、动效引擎、音效系统、配置抽屉）
│   └── chibi_avatar.png  # 内置头像资源
├── demo/
│   └── index.html        # 独立本地测试与预览页面
└── install.bat           # 本地自动挂载脚本
```

---

## 声明
本项目为社区第三方扩展，所有本地上传的图片与音频仅保存在浏览器本地存储（localStorage）中，不进行任何网络上传。
