---
title:  pilot 3.30 30min protocol
type: dataset
last_updated: 2026-04-25
status: settled
---

# 正常人 Baseline 数据采集 — 30 分钟精简版

> 版本 2.1 | 2026-03-31
> 完整版见：正常人Baseline数据采集实验方案.md

---

## 精简原则

从完整版 24 个动作 / 50 分钟中，按 **AD 鉴别效应量** 排序，优先保留核心层动作，精简如下：

| 层级 | 完整版 | 精简版 | 精简策略 |
|------|--------|--------|---------|
| 核心层 | 10 个动作 | **7 个** | 合并慢速/快速步态为常速步态（保留变异性最强的）；保留全部 BPSD 模拟（合成数据必需） |
| 中间层 | 8 个动作 | **3 个** | 仅保留效应量最大的：坐站转移 (d=1.0)、精细运动、书写 |
| 外围层 | 5 个动作 | **2 个** | 仅保留坐姿静息基线 + 恢复期 |
| **总计** | **23 个 / ~50 min** | **12 个 / ~28 min** | — |

---

## 动作清单（12 个动作，按采集顺序）

### Phase 1：静态基线（2 min）

| # | label | 时长 | 目的 |
|---|-------|------|------|
| B1 | `idle_sitting` | **2 min** | 所有通道静息基线（GSR、HR、IMU-SVM） |

### Phase 2：核心步态系列（8 min）  ← AD 鉴别力最强

| # | label | 时长 | AD 差异 | 效应量 |
|---|-------|------|--------|--------|
| C2 | `walking_normal` | **2 min** | 步速↓15-20%, 步态变异性↑ (CV: 2-3% → 6-8%) | d=1.0 |
| C5 | `turning` | **1.5 min** | 转身步数↑, 峰值角速度↓20-30%, 冻结停顿 | d=0.7-0.9 |
| C6 | `balance_standing` | **1.5 min** | 闭眼摇摆↑30-60%（睁眼45s + 闭眼45s） | d=0.8-1.1 |
| C1 | `walking_dual_task` | **3 min** | **DTC 30-50%**，步频变异急剧增大，可能停步 | **AUC=0.84** |

> C1 放最后：避免认知疲劳影响前面的纯运动任务

### Phase 3：ADL 功能精选（5 min）

| # | label | 时长 | AD 差异 | 效应量 |
|---|-------|------|--------|--------|
| M1 | `sit_to_stand` | **1.5 min** (8次) | 完成时间↑30-50%, 躯干角速度↓ | d=1.0 |
| M2 | `hand_fine_motor` | **1.5 min** | 手部震颤↑, jerk↑, 完成时间↑ | d=0.4-0.8 |
| M5 | `writing` | **2 min** | 书写速度↓, 停顿↑, 字体不规则 | 82-88% acc |

### Phase 4：BPSD 模拟（6 min）

| # | label | 时长 | AD 差异 | 效应量 |
|---|-------|------|--------|--------|
| C9 | `trembling` | **1.5 min** | 方差是核心（8倍于idle），频率不规则 | ★★ |
| C10 | `repetitive_motion` | **0.5 min** | 低熵周期性运动，额叶损伤标志 | 82% acc |
| C7 | `agitation_simulate` | **1 min** | GSR↑ + HR↑ + IMU方向变化↑（三通道联合） | AUC=0.87 |
| C8 | `wandering_simulate` | **3 min** | 路径无规律, 方向变化频繁, 步频不规则 | 88% sens |

### Phase 5：恢复（2 min）

| # | label | 时长 | 目的 |
|---|-------|------|------|
| B5 | `recovery` | **2 min** | 心率恢复曲线 (HRR)，AD 自主神经受损→恢复更慢 |

---

## 时间预算

```
准备期：传感器佩戴 + 信号检查             2 min
                                          ─────
Phase 1：B1 idle_sitting                  2 min
Phase 2：C2+C5+C6+C1 步态+平衡+双任务     8 min
Phase 3：M1+M2+M5 ADL 功能               5 min
Phase 4：C9+C10+C7+C8 BPSD 模拟          6 min
Phase 5：B5 recovery                      2 min
动作间过渡（11次 × 20s）                   ~4 min
                                          ─────
总计                                      ~29 min
```

---

## 采集流程图

```
传感器佩戴(2min)
    │
    ▼
B1  idle_sitting ────── 2 min ── 静息基线
    │ (20s)
    ▼
C2  walking_normal ──── 2 min ── ★★★ 步态变异性
    │ (20s)
    ▼
C5  turning ─────────── 1.5min ── ★★★ 转身犹豫/冻结
    │ (20s)
    ▼
C6  balance_standing ── 1.5min ── ★★ 闭眼摇摆
    │ (20s)
    ▼
C1  walking_dual_task ─ 3 min ── ★★★ 最强鉴别指标
    │ (30s 休息，认知任务后给更多恢复)
    ▼
M1  sit_to_stand ────── 1.5min ── ★★ 转移能力
    │ (20s)
    ▼
M2  hand_fine_motor ─── 1.5min ── ★★ 精细运动
    │ (20s)
    ▼
M5  writing ─────────── 2 min ── ★★ 书写动力学
    │ (20s)
    ▼
C9  trembling ───────── 1.5min ── ★★ 震颤（方差特征）
    │ (20s)
    ▼
C10 repetitive_motion ─ 0.5min ── ★★ 重复行为
    │ (20s)
    ▼
C7  agitation_simulate  1 min ── ★★★ BPSD激越
    │ (20s)
    ▼
C8  wandering_simulate  3 min ── ★★★ BPSD游走
    │ (直接过渡)
    ▼
B5  recovery ────────── 2 min ── 心率恢复
    │
    ▼
  结束（总计 ~29 min）
```

---

## 与完整版的标签对照

| label | 精简版保留 | 完整版对应 | 保留理由 |
|-------|----------|-----------|---------|
| `idle_sitting` | Yes | B1 | 唯一静息基线 |
| `walking_normal` | Yes | C2 | 步态变异性 d=1.0 |
| `walking_slow` | **No** | C3 | 与 normal 信息重叠 |
| `walking_fast` | **No** | C4 | 与 normal 信息重叠 |
| `walking_dual_task` | Yes | C1 | **AUC=0.84, 不可省** |
| `turning` | Yes | C5 | 转身冻结 d=0.7-0.9 |
| `balance_standing` | Yes | C6 | 闭眼摇摆 d=0.8-1.1 |
| `agitation_simulate` | Yes | C7 | BPSD AUC=0.87 |
| `wandering_simulate` | Yes | C8 | 游走 sens=88% |
| `trembling` | Yes | C9 | 方差特征 + AD/PD 鉴别 |
| `repetitive_motion` | Yes | C10 | 额叶损伤标志 |
| `sit_to_stand` | Yes | M1 | d=1.0 |
| `hand_fine_motor` | Yes | M2 | MCI 早期指标 |
| `writing` | Yes | M5 | 82-88% acc |
| `drinking_water` | **No** | M3 | 中度 AD 才退化，优先级低 |
| `eating_motion` | **No** | M4 | 重度才退化，优先级低 |
| `phone_using` | **No** | M6 | 重要但传感器特异性不如 M2/M5 |
| `fall_simulate` | **No** | M7 | 不直接区分 AD |
| `stair_climbing` | **No** | M8 | 场地依赖，优先级低 |
| `idle_standing` | **No** | B2 | 与 C6 合并 |
| `lying_down` | **No** | B3 | 精简版不需要 HRV 卧位基线 |
| `running` | **No** | B4 | SVM 天花板标定非必需 |
| `recovery` | Yes | B5 | 自主神经恢复指标 |

---

## 精简版仍覆盖的 AD 鉴别维度

| AD 鉴别维度 | 对应动作 | 可检出阶段 |
|------------|---------|-----------|
| 运动-认知耦合 | C1 双任务步态 | **MCI** |
| 步态变异性 | C2 常速步态 | **MCI** |
| 转身犹豫/冻结 | C5 转身 | MCI→轻度 |
| 姿势控制 | C6 平衡站立 | MCI→轻度 |
| 精细运动控制 | M2 精细动作 | MCI→轻度 |
| 书写动力学 | M5 书写 | **MCI** |
| 转移功能 | M1 坐站转移 | 轻度→中度 |
| BPSD 激越 | C7 激越模拟 | 中度 |
| BPSD 游走 | C8 游走模拟 | 中度 |
| BPSD 震颤/重复 | C9+C10 | 中度 |
| 自主神经功能 | B5 恢复期 | 轻度→中度 |

**精简版保留了完整版 ~90% 的 AD 鉴别信息量**，核心层动作几乎全部保留。

---

## 被试要求（同完整版）

| 项目 | 要求 |
|------|------|
| 年龄 | 55-75 岁健康老年人 |
| 认知状态 | MMSE ≥ 27 且 MoCA ≥ 26 |
| 排除标准 | 神经/精神疾病、严重关节/骨科疾病 |
| 知情同意 | 本人签字（无创无损伤） |

## 数据输出格式（同完整版）

```csv
t_ms,gsr_filtered,ppg_ir,hr_bpm_avg,imu_ax_mps2,imu_ay_mps2,imu_az_mps2,imu_steps,env_temp_c,env_humidity_rh,env_pressure_pa,env_altitude_m,label
```

---

*文档版本: 2.1（30min精简版）| 创建日期: 2026-03-31*
*完整版: 正常人Baseline数据采集实验方案.md (v2.0, ~50min)*
