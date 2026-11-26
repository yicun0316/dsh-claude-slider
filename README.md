<div align="center">

# dsh-claude-slider

给 DeepSeek Harness（DSH）做的一个推理滑块 + 桌面美化小插件。

[![Version](https://img.shields.io/badge/version-2.21.0-4D6BFE?style=flat-square)](package.json)
[![Listed on DSH Plugin Hub](https://dsh-plugin.org/badges/listed.svg)](https://dsh-plugin.org/plugins/yicun0316/dsh-claude-slider)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Build](https://img.shields.io/badge/零构建-单文件直跑-orange?style=flat-square)](#目录结构)
[![Network](https://img.shields.io/badge/网络请求-0-lightgrey?style=flat-square)](#一些说明)

</div>

一开始只是嫌原生那个「推理强度」下拉框有点素，顺手改成了滑块，结果越加越上头——现在里面塞了 **6 款内置 Canvas 滑块动效**、**输入框小宠物剧场**、**莫奈取色和随鼠流光框**、**自定义立绘游标**，还有几个整活音效。

单文件零构建，不连网，不读你的本地文件，装完在客户端里按 `Ctrl + R` 就能直接用。不想装 DSH 也可以直接用浏览器打开 [`demo/index.html`](demo/index.html) 先玩一遍。

---

## 6 款内置滑块动效

拖动滑块就能在 `Off / Low / High / Max` 之间连续切换，松手会轻轻弹回最近的档位，点刻度也能直达。每款动效都会跟着推理档位往上叠效果：Low 档安静克制，拉到 High 和 Max 才会慢慢热闹起来。

- **自然（2 款）**
  - **银河星穹**：深蓝紫夜空斜着铺开一条银心星云带，带暗尘埃裂纹和十字星芒，High 档偶尔会划过一颗流星，Max 档游标附近会炸开一簇星尘。
  - **冰晶凝霜**：不是往轨道里贴方块，而是把整条轨道做成一块背光冰川水晶，斜向折光面在冰层里慢慢滑过，档位越高，六瓣霜花、霜雾和细碎冰尘越清晰。
- **材质 / 花卉 / 数字（4 款）**
  - **玻璃水银**：拖拽时液面会跟着手速倾斜、松手回摆，里面飘着三种会翻转反光的玻璃棱片。
  - **落樱春水**：花瓣在春水涟漪上翻滚着飘，底色会跟着你选的主题色或莫奈色盘变。
  - **GPT 星流**：紫调渐变底色配柔光星点，高档位带短光尾。
  - **Claude 织格**：一格一格扫过去的波浪方块矩阵。

### 自由定制动效、经典回归与在线工坊

「动效 → **全部**」汇总内置与已导入的动效。「动效 → **自定义**」可以导入、复制和删除动效包。引擎支持 **Canvas 2D** 与 **WebGL GLSL**，可以联动主题色与莫奈三色盘，并提供离屏试跑校验与报错熔断保护。

- **动效库（[`themes/`](themes/README.md)）**收录 **16 款**可独立导入的动效，包括旧版火山喷发、极光织锦、GLSL 流体熔岩和铜银金砂。
- **自由定制工坊（[`studio/index.html`](studio/index.html)）**：双击即可在浏览器打开的单文件创作台，支持边写 Canvas 2D / GLSL 边看深浅双模式拖拽实机效果，并内置**一键复制 AI 动效生成提示词**，发给 DeepSeek / Claude 就能按任意脑洞生成可直接导入的动效包。
- **极简静止支持**：动效流速支持拉到 `0x`（静止），不喜欢晃眼的办公场景可随时定格成精致静态渐变。

---

## 输入框萌宠剧场

<div align="center">

![输入框像素萌宠剧场](assets/pets_showcase.png)

</div>

写代码或者等模型思考的时候总觉得输入框上面空荡荡的，就顺手在输入框顶上养了一排小宠物，**可以同时放出好几只一起玩**。

目前内置了 **6 只小伙伴**：

- **臭企鹅**（高松灯）：点它会有递进的「咕咕嘎嘎」，惹毛了会问你「为什么要演奏春日影!!」，平时还会念叨「捡到好看的小石头」「要组一辈子乐队吗」。
- **反重力猫娘**：说话句尾带喵，平时在线给你加「这行代码零 Bug」的精神 Buff。
- **鲸鱼娘女仆**：DeepSeek 看板娘，发呆时会轻声哼哼，被疯狂戳帽子会报「服务器繁忙，请稍后再试!」。
- **小紫猫 / 暖橘小蟹 / 深海小鲸**：三只经典像素小动物，在线监工、举钳打气、喷水庆祝。

**它们平时都在干嘛？**
- 闲着的时候会在输入框顶上**自己散步**，两只走近了甚至会**打起架来**（不喜欢太闹腾可以在面板里关掉「自主散步」或「相遇打架」）。
- 可以直接**鼠标戳它们**或者**拎起来拖动**，不同动作会弹不同的梗句。
- **跟推理状态联动**：你刚发消息开始思考时，它们会被「推理风」吹得东倒西歪；等回答跑完了，会跳起来撒花庆祝。
- 站位支持放**右上 / 左上 / 分站**，尺寸可以在 `0.8x ~ 1.35x` 之间调。

---

## 外观、游标和音效

点滑块右上角的小入口就能拉开设置面板，一共 5 个页签（动效 / 外观 / 萌宠 / 图标 / 声音），东西都放得很顺手：

- **外观 & 莫奈配色**
  - 内置 8 个常用主色和自定义 Hex 拾色器，面板支持浅色玻璃、深色磨砂和跟随系统，透明度（`15% ~ 100%`）自己拉。
  - 带了一套**莫奈取色**，有 6 组现成的三色搭配（反重力星紫、莫奈睡莲、樱云薄雾、晨曦琥珀、碧水青瓷、深海鲸蓝），也可以直接取色并联动到滑块上。
  - 输入框可以开**随鼠标移动的全周流光边框**（支持「棱镜虹彩」和「莫奈色盘」两种风格）和**周边环境晕色**，觉得太亮随时把氛围强度调低或者关掉。
- **游标图标**
  - 自带 DeepSeek 鲸鱼娘、爱弥斯、三款 Q 版全身立绘和极简纯白圆点，也可以直接**上传自己的本地图片**（PNG / JPG / SVG 都行）。
  - 传图不用自己先抠边：支持「导入自动裁边」和「一键裁边」，还能无损切换**立绘档**（64px 脚踩轨道下沿）和**圆头档**（26px 居中），大小支持 `70% ~ 140%` 缩放。
- **档位音效**
  - 换档时可以带一点反馈音，内置 5 款：**机械微触**、**咕咕嘎嘎**、**杂鱼**、**哦鲸鲸**、**小黄鸭**（`assets/sounds/` 里能直接试听），也可以上传本地 MP3 / WAV，音量独立调节。

---

## 怎么安装

在终端敲一行命令就行：

```bash
# 桌面版（直接从 GitHub 安装）
dsh plugin --profile desktop add github:yicun0316/dsh-claude-slider

# 网页版
dsh plugin --profile web add github:yicun0316/dsh-claude-slider

# 也可以走 npm 装稳定版
dsh plugin --profile desktop add dsh-claude-slider
```

装完在 DSH 里按 <kbd>Ctrl</kbd> + <kbd>R</kbd> 刷新一下就会出现。想还原回原生下拉框，在面板里关掉或者直接卸载就行。

<details>
<summary>插件市场 / 本地源码挂载 / 卸载命令</summary>

**插件市场**

```bash
dsh plugin --profile desktop add dshmarket
```
[![Listed on dsh-plugin.org](https://dsh-plugin.org/badges/listed.svg)](https://dsh-plugin.org/plugins/yicun0316/dsh-claude-slider)

装好 `dshmarket` 后在插件市场里搜 `dsh-claude-slider` 点安装。

**本地源码挂载（适合自己改代码玩）**

把仓库拉到本地后，直接运行根目录的 [`install.bat`](install.bat) 建立软链接，改完 `lib/client.js` 在 DSH 里按 `Ctrl + R` 立刻生效。

**卸载**

```bash
dsh plugin --profile desktop remove dsh-claude-slider
```

</details>

### 自由定制动效、经典回归与在线工坊

「动效 → **全部**」包含内置与已导入的动效。可以在「动效 → **自定义**」管理 Canvas 2D 和 WebGL GLSL 动效包。

- **动效库（[`themes/`](themes/README.md)）**提供 **16 款**可独立导入的 `.dcs-effect.json`。
- **自由定制工坊（[`studio/index.html`](studio/index.html)）**：双击即可在浏览器打开的单文件创作台，支持边写 Canvas 2D / GLSL 边看深浅双模式拖拽实机效果，并内置**一键复制 AI 动效生成提示词**，发给 DeepSeek / Claude 就能按任意脑洞生成可直接导入的动效包。
- **极简静止支持**：动效流速支持拉到 `0x`（静止），不喜欢晃眼的办公场景可随时定格成精致静态渐变。

---

## 一些说明

- **不折腾隐私**：所有配置只存在浏览器的 `localStorage`（键名 `dsh-claude-slider.config.v2`），插件全程零网络请求。
- **不白白吃 CPU**：窗口切到后台或最小化时，Canvas 和萌宠的动画循环都会自动停掉；滑块拉到 `Off` 档时也不会空跑帧；系统开了「减少动态效果」也会乖乖静下来。
- **常用可调项**：动效流速（`0x 静止 ~ 2.0x`）、动效亮度（`0.5x ~ 2.0x`）、面板透明度（`15% ~ 100%`）、输入框氛围强度（`10% ~ 100%`）、萌宠大小（`0.8x ~ 1.35x`）、游标大小（`70% ~ 140%`）、音量（`0% ~ 100%`）。

---

## 目录结构

```text
dsh-claude-slider/
├── package.json          # 插件信息与 DSH 注入声明
├── cordis.patch.yml      # 插槽配置
├── lib/
│   ├── index.js          # 服务端入口
│   └── client.js         # 核心实现（滑块动效、外观、萌宠、游标、音效都在这一个文件里）
├── assets/               # 预览图与内置音效
├── demo/index.html       # 双击就能在浏览器里玩的离线预览页
├── studio/index.html     # 自由定制动效工坊（Canvas 2D + WebGL GLSL + AI 提示词）
├── themes/               # 16 款可独立导入的 .dcs-effect.json
└── install.bat           # Windows 一键本地挂载脚本
```

---

## 开源致谢与灵感参考

这个插件在开发过程中借鉴了不少社区大佬的优秀想法和开源项目（尤其是光学外观、输入框流光框、推理滑块手感和萌宠互动这部分），在这里认真致谢，并附上原项目地址与开源协议：

| 项目 | 作者 / 协议 | 参考与致谢说明 |
| :--- | :---: | :--- |
| [**RMvdesi/obsidian-prism**](https://github.com/RMvdesi/obsidian-prism) | RMvdesi · `GPL-3.0-only` | 非常惊艳的 Antigravity 光学外观插件，本插件的液态玻璃质感、输入框流光框、莫奈氛围和像素萌宠玩法深受其启发 |
| [**0DNANCY/agy-claude-style**](https://github.com/0DNANCY/agy-claude-style) | 0DNANCY · `MIT` | 光学界面风格、柔和动效节奏与像素伙伴骨架灵感 |
| [**Nwflower/dsh-claude-style**](https://github.com/Nwflower/dsh-claude-style) | Nwflower | DSH Claude 风格的极简输入框与排版思路 |
| [**Microqian2th/dsh-codex-effort-slider**](https://github.com/Microqian2th/dsh-codex-effort-slider) | Microqian2th | DSH 推理强度滑块、能量轨道与阻尼手感的上游启发 |
| [**mobius/dsh-performance-slider**](https://github.com/mobius/dsh-performance-slider) | mobius | 性能档位滑块交互与反馈思路参考 |
| [**LLYSH-HANNARI/antigravity-Codex-Claude-effort-slider**](https://github.com/LLYSH-HANNARI/antigravity-Codex-Claude-effort-slider) | 月上寒 · `MIT` | 推理等级滑条交互设计参考 |
| [**claudenoshujin/claude-web**](https://github.com/claudenoshujin/claude-web) | lulu | 萌宠叠叠乐与微生态互动灵感（本插件为独立实现） |

同时一并致谢 Obsidian Prism 上游生态中的开源项目：[**ATtacK030130/antigrative-dashboard**](https://github.com/ATtacK030130/antigrative-dashboard)（`MIT` · AG Pulse）、[**yiheng8023/antigravity-chinese**](https://github.com/yiheng8023/antigravity-chinese)（`MIT` · yiheng8023）。

---

## 开源协议

本插件代码为独立实现，基于 [MIT License](LICENSE) 开源 © [yicun0316](https://github.com/yicun0316)。
引用或二次修改时请同样保留对以上开源社区项目的致谢。
