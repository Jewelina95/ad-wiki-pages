---
title: 合成数据 v1 校准计划
type: method
last_updated: 2026-04-25
status: working_hypothesis
sources:
  - wiki/datasets/external/_external_datasets_registry.md
  - wiki/methods/synthetic_data_v0_rules.md
  - wiki/methods/synthetic_data_review.md
  - wiki/synthesis/what_we_dont_know.md
---

# 合成数据 v1 校准计划

> **关闭路径**：解决 [OQ #1 合成数据 v0 是否合理](../synthesis/what_we_dont_know.md) 的方案。
> 当前状态：v1 正在执行（5 个 OpenNeuro 数据集已 clone，分布参数已提取）。

## 背景

[v0 合成数据](synthetic_data_v0_rules.md) 的核心问题：参数全是手工估计的，没有真实分布锚点；源人群是 N=4 健康年轻人，与 AD 老年患者不匹配。

v1 的解法：**用公开数据集的真实分布做参数锚点**，让合成出来的患者在统计上与真实人群无显著差异（KS 检验 p > 0.05）。

## v1 校准源（已下载）

5 个 OpenNeuro 数据集，覆盖完整认知谱：

| 数据集 | 校准什么 | 状态 |
|---|---|---|
| **ds004504** (88) | MMSE 三组分布主源（ctrl 30 / FTD 22.17 / AD 17.75） | ✅ 提取完成 |
| **ds007427** (138) | Paisa 家族性 AD MCI/at-risk 桶（μ=24.0, σ=3.84） | ✅ 提取完成 |
| **ds006095** (71) | **老年人 IMU + MoCA baseline ★ 与手套最对得上** | ✅ 已下载，IMU 提取待做 |
| **ds004796** (192) | SCD/早期建模 + APOE 风险分层 | ✅ 已下载 |
| **ds002778** (31) | PD 对照桶 / 鉴别诊断 | ✅ 已下载 |

完整登记见 [`wiki/datasets/external/_external_datasets_registry.md`](../datasets/external/_external_datasets_registry.md)。

## 校准流程

### Step 1: 提取分布（已完成）

```bash
cd code/scripts
python3 extract_all_distributions.py
# 产出: code/data/distributions_master.json (19 KB, 5 数据集联合分布)
```

每个数据集提取：年龄分布、性别比、MMSE 分布、EEG 频段功率（如适用）、IMU 步态参数（ds006095 待做）。

### Step 2: 替换 v0 中的硬编码阈值（待做）

v0 [`generate_synthetic_ad.py`](../../code/scripts/legacy/baseline48_generate_synthetic_ad.py) 里的退化系数都是手工估计：

```python
# v0 (硬编码)
svm_noise_mult = {"MCI": 1.2, "mild_AD": 1.5, "moderate_AD": 2.0}
```

v1 改读 distributions_master.json：

```python
# v1
import json
dists = json.load(open("data/distributions_master.json"))
mmse_mci = dists["datasets"]["ds007427"]["mmse"]  # μ=24.0, σ=3.84
mmse_ad  = dists["datasets"]["ds004504"]["groups"]["ad"]["mmse"]  # μ=17.75, σ=4.5

def progression_to_mmse(p, age, edu):
    if p < 0.30: target = (30.0, 0.0)              # ctrl
    elif p < 0.50: target = (mmse_mci["mean"], mmse_mci["sd"])
    elif p < 0.85: target = (mmse_ad["mean"], mmse_ad["sd"])
    return np.clip(np.random.normal(*target), 0, 30)
```

### Step 3: 补齐 IMU 校准（关键，下周做）

ds006095 有 71 例老年人的 IMU（4 个传感器：头/腰/双脚背） + MoCA。需要写一个新脚本：

```python
# scripts/extract_imu_baseline.py (待写)
# 从 ds006095 的 IMU 数据提取:
# - 老年健康人步速分布: μ_speed, σ_speed
# - 步频变异性: μ_cv, σ_cv
# - 跨步抖动 (jerk): μ_jerk, σ_jerk
# 写入 distributions_master.json["imu_baseline_elderly"]
```

然后 v1 生成器用这个替换 v0 用的 N=4 年轻人 baseline。**这是最关键的一步**——它让合成 AD 患者建立在真实老年基线上，不再是"年轻人 + 退化系数"。

### Step 4: WearGait-PD 校准退化幅度（待下载）

WearGait-PD（100 PD + 85 ctrl，13 IMU）当前还没下载。论文里给的 DOI 需要再核。下载后：

```python
# 提取 PD 患者步态退化幅度，作为 AD 类似神经退化代理
# 写入 distributions["imu_degradation_pd"]
```

### Step 5: 验证（v0 不可能的事）

```python
# scripts/validate_v1.py (待写)
# 1. 跑 v1 生成器，产出 84 例合成患者
# 2. 对每个特征跑 KS 检验：合成分布 vs 真实分布
# 3. 报告 p 值；若所有主要特征 p > 0.05 → v1 通过
```

通过后，[`synthetic_data_review.md`](synthetic_data_review.md) 的 OQ #1 状态从 `open_question` 切换到 `resolved`。

## 时间表

| 阶段 | 内容 | 状态 | 完成时间 |
|---|---|---|---|
| ✅ 数据下载 | 5 个 OpenNeuro 数据集 clone | 完成 | 2026-04-25 |
| ✅ 分布提取 | distributions_master.json | 完成 | 2026-04-25 |
| ⏳ Step 3 | ds006095 IMU baseline 提取 | 进行中 | 本周 |
| ⏳ Step 4 | WearGait-PD 下载 + 提取 | 待开始 | 1 周内 |
| ⏳ Step 2 | v0 → v1 generator 改造 | 待开始 | 2 周内 |
| ⏳ Step 5 | KS 检验验证 | 待开始 | 3 周内 |

## v1 完成后

预期可以**关闭** [OQ #1](../synthesis/what_we_dont_know.md)，把所有 `synthetic_data_v0_rules.md` 和 `wiki/datasets/synthetic_84.md` 的 `working_hypothesis` 状态升级为 `settled`，并在 [`log.md`](../../log.md) 追加 resolution 条目。

之后下一个开放问题转为 [OQ #4 真实 AD 患者数据](../synthesis/what_we_dont_know.md)，这一条要等伦理 + 招募，不是合成数据能解决的。

## 引用

- ds004504: Miltiadous et al. 2023, MDPI Data 8(6):95
- ds007427: 哥伦比亚 paisa 家族性 AD 队列（PSEN1 E280A）
- ds006095: Nature Sci Data 高密度多模态步态
- ds004796: PEARL-Neuro Polish risk cohort
- ds002778: Resting-state EEG PD vs Healthy
