# dsh-claude-slider

DeepSeek Harness (DSH Desktop & Web) 的推理强度调节滑块插件。  
将默认的思考模式/推理强度下拉选择器替换为横向滑块交互，并提供动效、音效、图标及参数自定义功能。

---

## 📸 功能面板概览

| ✨ 动效与定制工坊 | 🎨 主题色彩与拾色器 |
| :---: | :---: |
| <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/panel_effect.png" width="380" alt="动效面板" /> | <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/panel_color.png" width="380" alt="色彩面板" /> |
| ⚡ **参数调校与音效** | 🐟 **手柄图标选择** |
| <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/panel_tuning.png" width="380" alt="调校面板" /> | <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/panel_icon.png" width="380" alt="图标面板" /> |

---

## 🌟 动效实机效果

| 动效类型 | 实机运行截图 | 说明 |
| :--- | :---: | :--- |
| **🌊 玻璃水银**<br>`(Liquid Mercury)` | <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/effect_mercury.png" width="450" alt="玻璃水银实测截图" /> | 液态金属光泽、旋转多面玻璃晶片与十字星芒闪烁 |
| **🌸 落樱春水**<br>`(Sakura Flutter)` | <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/effect_sakura.png" width="450" alt="落樱春水实测截图" /> | 绯粉水流渐变、翻滚花瓣微元与水波涟漪 |
| **⚡ 科技流光**<br>`(Tech Stream)` | <img src="https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/effect_tech.png" width="450" alt="科技流光实测截图" /> | 高能等离子流光、动态矩阵粒子推进与外发光晕染 |

---

## 🔊 档位吸附音效

滑块切换档位吸附时即时发声，支持在【调校】页面中调节音量大小（0% ~ 150%）或静音。

![音效展示卡片](https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/sound_showcase.svg)

| 音效名称 | 台词 / 声效 | 风格特色 | 试听与音频文件 |
| :--- | :--- | :--- | :--- |
| **🐟 杂鱼 (Zako)** | `ざぁ～こ♡ ざぁ～こ♡` | 傲娇嘲讽萌系声线 | <audio src="assets/sounds/zako.mp3" controls preload="none"></audio><br>[▶ 试听 / 下载 zako.mp3](assets/sounds/zako.mp3) |
| **🐳 哦鲸鲸 (Ochinchin)** | `お～ちんちん♡` | 软萌声线，DeepSeek 谐音梗 | <audio src="assets/sounds/ochinchin.mp3" controls preload="none"></audio><br>[▶ 试听 / 下载 ochinchin.mp3](assets/sounds/ochinchin.mp3) |
| **🐥 小黄鸭** | `嘎啾~ 嘎啾~` | 经典捏橡皮鸭解压声 | 内置 Web Audio 物理声学合成 |
| **⚙️ 机械微触感** | `咔哒` | 高频物理齿轮拨动阻尼微触感 | 内置 Web Audio 物理声学合成 |
| **📁 本地自定义音频** | 用户本地音频 | 支持上传任意 MP3 / WAV 作为音效 | 本地持久化存储与即时发声 |

---

## 🎨 全局色彩联动与自定义拾色

提供 9 款预设主题色与原生 Hex 拾色器，动效主色调与光晕随主题色同步切换。

![主题色彩与动效联动展示](https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/color_showcase.svg)

| 色彩类别 | 包含颜色 / 功能 | 说明 |
| :--- | :--- | :--- |
| **预设主题色 (9 款)** | DeepSeek 蓝 (`#4D6BFE`)、幻海晶青 (`#00F2FE`)、Claude 暖陶 (`#D97706`)、Claude 曜金 (`#F59E0B`)、极客翠绿 (`#10B981`)、暗夜幽紫 (`#8B5CF6`)、蔷薇绯粉 (`#F43F5E`)、烈焰赤橙 (`#FF6B4A`)、冷月珠光 (`#E2E8F0`) | 一键应用，全局同步生效 |
| **原生 Hex 拾色器** | 任意 16 进制颜色代码（如 `#FF0055`）或点击色盘直选 | 自动计算渐变与粒子透明度分层 |

---

## ⚡ 调校控制台（音量 / 流速 / 亮度）

在【调校】页面中配备无极微调滑块，实时生效。

![调校控制台展示](https://raw.githubusercontent.com/yicun0316/dsh-claude-slider/main/assets/tuning_showcase.svg)

| 调节参数 | 可调范围 | 默认数值 | 说明 |
| :--- | :--- | :--- | :--- |
| **🔊 吸附音量大小 (Volume)** | `0%` (静音) ~ `150%` | `100%` | 拖拽即时试听，提供独立【试听】与一键【复位】 |
| **⚡ 动效流速倍率 (Speed)** | `0.2x` ~ `2.5x` | `1.0x` | 控制粒子飞行速度与波涌频率，提供一键【复位】 |
| **💡 辉光渲染亮度 (Brightness)** | `0.4x` ~ `2.2x` | `100%` | 调节发光核心透明度与晕染强度，提供一键【复位】 |

---

## 📋 功能列表

### 1. 推理强度控制
- **档位调节**：支持模型预设档位（如 Off / Low / High / Max）的拖拽调节与即时吸附。
- **点击直达**：点击滑块轨道各节点或文字可直接切换。
- **原生兼容**：在调校面板或系统设置中提供总开关；关闭后还原为 DSH 默认下拉菜单。

### 2. 视觉动效
- **预设动效**（5 大类，共 19 款）：
  - **推进**：火箭尾焰、离子飞箭、超载折跃
  - **流体**：幽夜暗潮、玻璃水银、火山喷发
  - **幻境**：落樱春水、极光织锦、深海鲸跃、萤火微光、落雪狂沙
  - **科技**：频谱律动、数据矩阵、雷达扫描、电路脉冲、赛博霓光
  - **质感**：水墨飞白、柔光丝缕、点阵起伏、等高拓扑、流金星河
- **定制动效**：支持自定义混搭，提供启用/禁用切换：
  - 粒子形态（10 种）：炽焰、晶体、星芒、圆点、光雾、花瓣、弧光、气泡、霓虹、碎片
  - 流动轨迹（8 种）：推进、星流、对撞、波涌、涡旋、跃迁、爆发、环绕
- **色彩联动**：动效光效与粒子颜色跟随主题色同步变化。

### 3. 分类栏交互
- **拖拽滑动**：按住分类栏可左右拖动切换。
- **滚轮横滚**：鼠标悬停在分类栏上时滚轮可横向滚动。
- **微翻页控制**：分类栏两侧设有 `‹` 和 `›` 翻页按钮。
- **自动居中**：点击分类标签自动平滑滚动至视口中央。
- **轻扫切换**：在卡片区域左右滑动切换大类。

### 4. 手柄图标
- **内置图标**（10 款）：DeepSeek 鲸鱼娘、Claude 官方星芒、DeepSeek 官方鲸鱼、超级大脑、闪电脉冲、量子原核、炽热烈焰、璀璨宝石、灵动星火、精准瞄准。
- **自定义图标**：支持上传本地图片（PNG / JPG / SVG）或直接输入 Emoji 作为手柄图标。

### 5. 配置导入与导出
- **导出**：将当前所有设置导出为 JSON 文本。
- **导入**：支持粘贴 JSON 配置并一键应用。

---

## 📦 安装与使用

### 方式一：命令行一键安装（推荐）

在终端（PowerShell / CMD / Terminal）中执行以下命令：

```bash
# 从 npm 安装
dsh plugin --profile desktop add dsh-claude-slider

# 或从 GitHub 安装
dsh plugin --profile desktop add github:yicun0316/dsh-claude-slider

# 网页版 (Web Profile)
dsh plugin --profile web add dsh-claude-slider
# 或网页版从 GitHub 安装
dsh plugin --profile web add github:yicun0316/dsh-claude-slider
```

安装完成后，在 DSH 客户端中按下 **`Ctrl + R`** 重新加载即可生效。

---

### 方式二：通过 dsh-market 安装

在 DSH 中安装应用市场插件后，可在界面内直接搜索 `dsh-claude-slider` 一键安装。

```bash
# 安装插件市场
dsh plugin --profile desktop add dshmarket
```

---

### 方式三：本地开发者模式（源码挂载）

1. 克隆本仓库后，运行项目根目录的 `install.bat`，自动创建软链接到 DSH 插件目录；
2. 在 DSH 客户端中按下 `Ctrl + R` 重新加载；
3. 本地浏览器预览：直接打开 `demo/index.html` 即可预览完整功能。

---

### 卸载插件

```bash
# 从桌面版卸载
dsh plugin --profile desktop remove dsh-claude-slider

# 从网页版卸载
dsh plugin --profile web remove dsh-claude-slider
```

---

## 结构说明

```
dsh-claude-slider/
├── package.json          # 插件信息与版本定义
├── cordis.patch.yml      # DSH 插件插槽声明
├── assets/               # 截图与资源文件
│   ├── panel_effect.png  # 动效面板截图
│   ├── panel_color.png   # 色彩面板截图
│   ├── panel_tuning.png  # 调校面板截图
│   ├── panel_icon.png    # 图标面板截图
│   ├── effect_mercury.png# 玻璃水银实机截图
│   ├── effect_sakura.png # 落樱春水实机截图
│   ├── effect_tech.png   # 科技流光实机截图
│   ├── sound_showcase.svg# 音效展示卡片
│   ├── color_showcase.svg# 色彩展示卡片
│   ├── tuning_showcase.svg# 调校展示卡片
│   └── sounds/           # 音频文件（zako.mp3, ochinchin.mp3）
├── lib/
│   ├── index.js          # 服务端入口
│   └── client.js         # 客户端核心实现
└── demo/
    └── index.html        # 本地预览测试页面
```
