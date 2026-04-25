---
title: 硬件路线图 / 原型状态
type: synthesis
last_updated: 2026-04-25
status: draft
sources:
  - wiki/concepts/glove_form_factor.md
  - wiki/concepts/eda_signal.md
  - wiki/concepts/ppg_hrv.md
  - wiki/concepts/imu_gait.md
  - wiki/concepts/voice_acoustic_linguistic.md
---

# 硬件路线图 / 原型状态

> 硬件是 [open question #5](what_we_dont_know.md) 的核心。这里集中记录当前进度与下一步。

## 当前状态（2026-04-25）

| 模块 | 状态 | 备注 |
|---|---|---|
| ESP32 音频原型 | ✅ 已通 | `raw/code_archives/esp32-audio-ai-main/` |
| 整合 EDA + PPG + IMU + 麦克风手套 | 🔧 设计阶段 | 未制造 |
| BoM 选型 | 📝 草案中 | 选型未冻结 |
| 电池续航目标 | 📝 ≥7 天 | 来自用户偏好研究（PMC8072390 n=21） |
| 皮肤耐受测试 | 🚫 未启动 | 等原型出来再做 |
| 防水 / 抗汗 | 🚫 未启动 | — |

## 设计目标（不变）

- **不阻塞 wiki / Agent / Demo 开发**——硬件是并行轨。Agent 逻辑用 (a) 现有 4 例 baseline + (b) 外部 IMU 数据（ds006095, WearGait-PD）+ (c) 合成数据 跑通；硬件造出来后只是把"现有 CSV → Agent" 换成"实时流 → Agent"。
- **传感器布局** 见 [glove_form_factor](../concepts/glove_form_factor.md)：手指 EDA · 手腕/手背 PPG + IMU · 近口麦克风。
- **形态约束**：
  - 半指棉手套（用户偏好研究 53.8% 把外观排第一）
  - 续航 ≥ 7 天（42.9% 排第二）
  - 不影响日常触感

## 与软件栈的关系

```
未来:                              现在:
[实时传感器流]                     [合成 / 外部 CSV]
       ↓                                  ↓
[edge preprocessing on ESP32]      [code/src/sensors/preprocessing.py]
       ↓                                  ↓
       └──────── 同一份特征 bundle ───────┘
                       ↓
              Unified Clinical Agent (一样)
```

软件层完全不依赖硬件 ready，只依赖**传感器 schema 一致**。schema 定义在 [`wiki/methods/agent_data_loader_interface.md`](../methods/agent_data_loader_interface.md)。

## 下一步

短期（4–6 周）：
1. 用 ds006095 老年 IMU 数据替换现有 4 例年轻 baseline 做 reference range——这一步**不依赖硬件**
2. 锁定 BoM（EDA 模块 / PPG 模块 / IMU 模块 / mic 选型）

中期（2–3 个月）：
3. 第一版整合手套打样
4. 自我测试 → 临床合作伙伴小规模可用性测试
5. 启动伦理招募阶段（30 → 200 → 60）

## 不做的事

- ❌ **不等硬件 ready 再做软件**——并行做才能 paper 阶段同时拿出系统 + 验证
- ❌ **不把 N=4 baseline 扩到 N=10 健康年轻人**——ROI 低；ds006095 71 例老年人价值大 10 倍
- ❌ **现在不申请 ADNI / OASIS-3**——4–8 周审批，paper draft 阶段再申请理由更充分

## 引用

- 用户偏好研究：PMC8072390 n=21，4 款腕戴比较
- ESP32 音频参考：`raw/code_archives/esp32-audio-ai-main/`
