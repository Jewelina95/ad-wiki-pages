---
title: 外部公开数据集登记
type: dataset
last_updated: 2026-04-25
status: settled
sources:
  - wiki/methods/synthetic_data_v1_plan.md
  - wiki/methods/synthetic_data_review.md
---

# 外部公开数据集登记

我们用的所有外部数据集统一登记在这里。每个数据集回答 4 个问题：

1. **是什么**——n、模态、采集协议
2. **状态**——下载/申请中/已规划/未启动
3. **校准什么**——对接合成数据 v1 的哪个参数
4. **限制**——人群差异 / 可比性边界

## 总览

| 数据集 | 模态 | n | 优先级 | 状态 | 角色 |
|---|---|---|---|---|---|
| **ds004504** | EEG · AD/FTD/Healthy | 88 | ⭐⭐⭐ | ✅ 已下载 | MMSE 三组分布主校准源 |
| **ds007427** | EEG · 家族性 AD (PSEN1) | 138 | ⭐⭐⭐ | ✅ 已下载 | MCI/at-risk 中度区间校准 |
| **ds006095** | 高密 EEG + EMG + IMU + 不平地形 | 71 | ⭐⭐⭐ | ✅ 已下载 | **★ 最关键** — 老年人 IMU + MoCA baseline |
| **ds004796** | EEG + fMRI + APOE + 生活方式 | 192 | ⭐⭐⭐ | ✅ 已下载 | SCD/早期建模 + APOE 风险分层 |
| **ds002778** | Resting EEG · PD vs Healthy | 31 | ⭐⭐ | ✅ 已下载 | PD 对照桶 / 鉴别诊断 |
| ds005363 | （EEG 备选） | — | ⭐ | ✅ 已下载 | 备选参考 |
| ds005892 | （EEG 备选） | — | ⭐ | ✅ 已下载 | 备选参考 |
| ds006036 | （EEG 备选） | — | ⭐ | ✅ 已下载 | 备选参考 |
| ds006466 | （EEG 备选） | — | ⭐ | ✅ 已下载 | 备选参考 |
| **MultiConAD** | 语音对话 · 4 语言含中文 | 16 dataset 合并 | ⭐⭐⭐ | ✅ 已下载 | Audio Agent 中文校准 + 训练集 |
| **WearGait-PD** | 13 IMU + 鞋垫压力 · PD/Ctrl | 100 PD + 85 ctrl | ⭐⭐⭐ | ⏳ 待下载（DOI 链接待核） | **手套 IMU 步态分布主校准源** |
| Clinical Gait DS | 4 IMU · 多病种 | 260 | ⭐⭐ | ⏳ 待下载（联系作者） | AD vs PD vs 骨科鉴别 |
| TAUKADIAL 2024 | 中文语音挑战赛 | — | ⭐⭐ | ⏳ 待下载 | Audio Agent 中文 baseline 备选 |
| OASIS-3 | MRI + 认知 · 30 年纵向 | 1098 | ⭐⭐ | 📝 待申请（1–2 周） | 量表纵向变化标定 |
| ADNI | MRI/PET/CSF/认知 | 数千 | ⭐ | 🚫 暂不申请 | **paper draft 阶段再申**（4–8 周审批） |

**已下载的 5 个 OpenNeuro 数据集组合起来覆盖了一条完整的认知谱：**

```
正常 (ds004504 ctrl 67y, ds004796 健康中年, ds006095 老年)
  ↓
SCD/早期风险 (ds004796 APOE+ + 生活方式)
  ↓
MCI/中度 (ds007427 paisa 家族性队列)
  ↓
AD (ds004504 AD 组)
  
横向鉴别：PD (ds002778) vs FTD (ds004504) vs AD
```

## 已生成的校准产物

实际跑出来的分布数据：

- [`code/data/distributions_master.json`](../../../code/data/distributions_master.json)（19 KB）—— 5 数据集联合分布，含每组的 age/MMSE/gender/EEG 频段功率
- [`code/data/distributions_ds004504.json`](../../../code/data/distributions_ds004504.json)（1.6 KB）—— 单数据集校准

提取脚本：

- [`code/scripts/extract_all_distributions.py`](../../../code/scripts/extract_all_distributions.py)
- [`code/scripts/extract_ds004504_distributions.py`](../../../code/scripts/extract_ds004504_distributions.py)

## 已知 MMSE 真实分布（从 ds004504 + ds007427 提取）

| 组别 | 来源 | n | MMSE μ | MMSE σ | 用途 |
|---|---|---:|---:|---:|---|
| Healthy ctrl | ds004504 ctrl | 29 | 30.0 | 0.0 | 正常分桶 |
| FTD | ds004504 ftd | 23 | 22.17 | 8.22 | MCI/早期代理 |
| AD | ds004504 ad | 36 | 17.75 | 4.50 | AD 阶段锚点 |
| Paisa MCI/at-risk | ds007427 | 138 | 24.0 | 3.84 | MCI 中度区间 |

合成数据 v1 的 `progression → MMSE` 映射函数将以这套真实分布做参数。详见 [`synthetic_data_v1_plan.md`](../../methods/synthetic_data_v1_plan.md)。

## 短板

⚠️ **真正对手套项目最关键的可穿戴/IMU 数据还差一步**：

- ✅ ds006095 有 IMU（71 例老年）—— 已下载，给了我们老年健康基线
- ⏳ WearGait-PD 还没下载（13 IMU × 185 例 PD/ctrl）—— 当前最该补的
- ⏳ MultiConAD 中文部分还没拉下来跑（虽然下载了，特征还没提取）
- 🚫 没有真实 AD 可穿戴标注数据（这是 [OQ #4](../../synthesis/what_we_dont_know.md) 的核心）

## 引用模板（论文 method 章节）

参见 `AD相关公开数据集汇总.md` 末尾的 LaTeX 模板。当我们 paper draft 时，这一段会改写为正式 method 引用。
