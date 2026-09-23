# STATUS.md — 当前状态快照

> **给 AI agent 的用法**：上下文被压缩/丢失后，以这份文件为准确来源，不要凭记忆推断。
> 每次做较大改动后更新对应条目。

_最后更新：2026-09-23 13:45_

## 一、项目是什么

DSH（DeepSeek Harness）客户端插件 `dsh-claude-slider`：把推理强度（reasoning effort）的选择
做成 Claude 风格的滑块，并附带一整套 Canvas 动效、主题配色、手柄图标与音效。

- 形态：**零构建**、单文件客户端插件（`lib/client.js`，约 5000 行）
- 装载方式：通过 `dsh plugin --profile desktop add link:<本目录>` 软链接进 profile
- 存储：配置写在 `localStorage`，键 `dsh-claude-slider.config.v2`
- 网络：**零请求**；不读写用户文件（图标上传仅走本地压缩后存 localStorage）

## 二、功能清单（截至本快照）

### 动效：23 种，分 5 个家族

| 家族 | 成员 |
|---|---|
| 🚀 推进 rocket | 火箭尾焰 `rocket_thrust`、离子飞箭 `ion_stream`、超载折跃 `warp_boost`、客制动效 `custom_flow` |
| 🌊 流体 fluid | 幽夜暗潮 `surging_current`、玻璃水银 `liquid_mercury`、火山喷发 `volcano_magma` |
| 🌿 幻境 nature | 落樱春水 `sakura_flutter`、极光织锦 `aurora_veil`、深海鲸跃 `deep_whale`、萤火微光 `firefly_swarm`、落雪狂沙 `snow_sandstorm` |
| 🔧 科技 tech | 频谱律动 `spectrum_bars`、数据矩阵 `data_stream`、雷达扫描 `radar_sweep`、电路脉冲 `circuit_pulse`、赛博霓光 `cyber_pulse` |
| 🎨 质感 art | 星流碎钻 `jet_stream`、水墨飞白 `ink_wash`、柔光丝缕 `silk_ribbon`、点阵起伏 `dot_matrix_wave`、等高拓扑 `contour_lines`、流金星河 `chrono_gold` |

### 客制动效（`custom_flow`）自由组合

- **10 种粒子形态**（`CUSTOM_PARTICLES`）：炽焰 flame / 晶体 diamond / 星芒 star / 圆点 dot /
  光雾 mist / 花瓣 sakura / 弧光 arc / 气泡 bubble / 霓虹 neon / 碎片 shard
- **8 种运动动力学**（`CUSTOM_MOTIONS`）：推进 thrust / 星流 stream / 对撞 clash / 波涌 wave /
  涡旋 vortex / 跃迁 leap / 爆发 burst / 环绕 orbit
- ⚠️ 这些 id 必须与 `CanvasEffect` 里的渲染分支保持一致，改 id = 改契约

### 其他

- 档位：off / low / high / max（DeepSeek 适配器实际只有这四档；表里保留 medium 供其他 provider）
- 算力预算释义：`EFFORT_DESCRIPTIONS`
- 流速倍率 / 辉光倍率 / 全家桶配色（9 预设 + 全色谱拾色器）
- 手柄图标：官方矢量图（Claude 星芒 / DeepSeek 鲸鱼 / 鲸鱼娘）+ Emoji + 本地图片上传（Canvas 压缩到 96×96）
- 音效：Web Audio 合成（杂鱼 / 哦鲸鲸 / 小黄鸭 / 机械触感 / 自定义）
- 迁移：`LEGACY_EFFECT_MAP` 把历代旧 id 映射到现行 id（**不要删**）

## 三、工程护栏（已实现，勿回退）

- 帧率无关动画：`time += 0.035 * dt * speed`
- 不可见即暂停：`visibilitychange` + 清理
- 无障碍：`prefers-reduced-motion` 命中时降级
- 混合模式：`globalCompositeOperation` 仅深色用 `lighter`，浅色回 `source-over`
- 粒子预算按档位分档；`devicePixelRatio` 上限 2

## 四、已修复的事故（供追溯）

| 日期 | 症状 | 原因 | 处理 |
|---|---|---|---|
| 2026-09-23 | 「推理调节组件异常：EFFORT_DESCRIPTIONS is not defined」 | 整文件重写时连同定义一起删掉，只剩引用 | 补回 `EFFORT_DESCRIPTIONS`；并预修同类地雷 `CUSTOM_PARTICLES` / `CUSTOM_MOTIONS`（当时一开客制动效面板必崩） |

修复前的完整备份：`_backups/client.js.20260923-134335.bak`（该目录已被 .gitignore 排除）

## 五、待办

- [x] 本机绝对路径已从仓库文件中清除（README 重写时移除）
- [x] 补齐 `LICENSE`（MIT）+ README「非官方插件」免责声明 + 给外部用户的安装命令
- [ ] README 的动效名单与代码同步（当前 README 写 23 种，与 `EFFECT_MODES` 一致；历史上换过 4 代命名）
- [ ] `demo/index.html` 是手工同步副本，改 `lib/client.js` 后要一起改（长期建议改成引用同一份渲染代码）
- [ ] 效果 id 已冻结；今后只允许通过 `LEGACY_EFFECT_MAP` 改名
- [ ] 上传 GitHub（仓库尚未创建）
- [ ] npm 发布（包名 `dsh-claude-slider` 在 npm 上仍为空闲）
