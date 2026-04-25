---
title: AD-SensorDataFactory 合成数据生成器设计方案 (v0)
type: method
last_updated: 2026-04-25
status: working_hypothesis
sources:
  - raw/source_docs/plan_2026-03-13.md
  - code/scripts/legacy/baseline48_generate_synthetic_ad.py
  - raw/sensor_data/synthetic_4.8/
  - raw/sensor_data/synthetic_v0/
see_also:
  - wiki/methods/synthetic_data_review.md
  - wiki/methods/synthetic_data_methods_landscape.md
  - wiki/synthesis/what_we_dont_know.md
---

> ⚠️ **Status: Working hypothesis — under review (registered 2026-04-25).**
> The user has flagged the synthetic-data design as not necessarily correct.
> Treat any claim on this page as provisional. Before relying on it, read
> [`synthetic_data_review.md`](synthetic_data_review.md) — the open-questions
> ledger that lists what these rules assume, why those assumptions might be
> wrong, and what we'd need to verify them. The CSVs under
> `raw/sensor_data/synthetic_4.8/` and `raw/sensor_data/synthetic_v0/` are
> preserved as artifacts of this v0 design but should not be treated as
> validated training data.

---

# AD-SensorDataFactory 合成数据生成器设计方案

**Parametric Synthetic Sensor Data Generator for AD Wearable Glove System**


---

# 一、设计背景

## 1.1 为什么需要一个专门的DataFactory

当前项目合成数据面临三个核心问题：

1. 格式不一致：现有 `synthetic.py` 生成的是预处理后的特征值（gait_speed, sdnn, ttr），但硬件手套产出的是原始传感器信号（`gsr_filtered`, `ppg_ir`, `imu_ax/ay/az_mps2`），两者格式完全不同
2. 缺乏模块化：所有生成逻辑混在一个文件中，难以独立测试、扩展和版本管理
3. 与真实数据脱节：参数来自文献统计量，未与实际硬件采集的信号范围校准

## 1.2 VBVR DataFactory 的启示

VBVR (A Very Big Video Reasoning Suite, arXiv:2602.20159) 虽然面向视频推理，但其 DataFactory 架构是合成数据工程的典范。该项目包含 150+ 独立 data generator，每个是自包含的GitHub 仓库，通过统一接口 `Generator(seed, params) → standardized output` 实现参数化、确定性、无限量的数据生成。

### VBVR 核心设计原则与本项目映射

| VBVR 设计原则 | VBVR 实现 | 本项目映射 |
|--------------|----------|-----------|
| **模块化生成器** | 150+ 独立 generator，每个一个仓库，自包含运行 | 每种活动/BPSD 事件 = 一个独立 generator 模块 |
| **参数化无限生成** | `Generator(seed, params) → data`，无固定数据集大小 | `ActivityGenerator(seed, stage, profile) → CSV rows`，无限生成 |
| **确定性可复现** | 相同 seed 产生完全相同的输出 | `np.random.default_rng(seed)` 控制所有随机过程 |
| **认知分类学** | 5 大认知类别（感知/抽象/空间/变换/知识） | AD 临床维度（运动/自主神经/情绪行为/BPSD事件） |
| **标准化输出接口** | 统一 `first_frame.png + prompt.txt + ground_truth.mp4 + metadata.json` | 统一 CSV 行（与硬件格式一致）+ `metadata.json` |
| **模板驱动开发** | `template-data-generator` 基础模板，所有 generator 继承 | `BaseActivityGenerator` 基类，所有活动 generator 继承 |
| **质量元数据** | `question_metadata.json` 记录生成参数和分类标签 | `generation_metadata.json` 记录 seed、stage、profile、事件注入列表 |

### VBVR 的关键洞察

VBVR 将合成数据生成分解为**独立的、参数化的、可组合的生成器**。每个 generator：

1. 接受**语义参数**（物理定律系数、空间关系），不是低层噪声
2. 内部实现**确定性模拟引擎**，程序化生成数据
3. 产出**标准化格式**的输出，下游系统直接消费
4. 可独立开发、测试、版本管理

这些原则直接适用于传感器数据合成。

---

# 二、真实传感器数据基线

## 2.1 数据来源

文件：`data/all_sensors_log_withLabel20260326_093901.csv`

- **采集对象**：正常人（健康志愿者）
- **采集时长**：约 4 分钟（240.6 秒）
- **采样率**：~50Hz（间隔 ~20ms）
- **总数据量**：26,776 行
- **活动序列**：坐→走→跑→坐→走→手抖→坐
- **CSV 列**：`t_ms, gsr_filtered, ppg_ir, hr_bpm_avg, imu_ax_mps2, imu_ay_mps2, imu_az_mps2, imu_steps, env_temp_c, env_humidity_rh, env_pressure_pa, env_altitude_m, label`

## 2.2 各活动的统计参数（Normal 阶段 Ground Truth）

以下参数直接从真实采集数据中提取，作为合成数据的正常人基线：

| 特征 | idle (N=9961) | walking (N=9967) | running (N=2925) | trembling (N=3923) |
|------|:---:|:---:|:---:|:---:|
| **SVM 均值** | 9.70 | 10.47 | 12.95 | 10.16 |
| **SVM 标准差** | 0.37 | 1.45 | 5.53 | 2.91 |
| **GSR 均值** | 1688 | 1705 | 1598 | 1678 |
| **GSR 标准差** | 79 | 58 | 44 | 39 |
| **PPG_IR 均值** | 91145 | 90812 | 91195 | 91084 |
| **PPG_IR 标准差** | 1130 | 991 | 562 | 464 |
| **HR 均值 (bpm)** | 69 | 64 | 67 | 76 |
| **HR 标准差** | 10 | 5 | 12 | 5 |
| **Temp 均值 (°C)** | 25.62 | 25.79 | 25.70 | 25.60 |
| **Temp 标准差** | 0.81 | 0.75 | 0.39 | 0.23 |
| **Humidity 均值 (%)** | 31.69 | 30.85 | 30.97 | 32.31 |
| **Humidity 标准差** | 0.71 | 0.63 | 0.49 | 0.56 |

### 关键发现（指导合成策略）

1. **SVM 是活动区分的主特征**：idle(9.70) → walking(10.47) → running(12.95)，差异显著
2. **trembling 的特征在变异性而非均值**：SVM 均值 10.16（接近 idle 的 9.70），但标准差 2.91（是 idle 0.37 的 8 倍）→ 合成 trembling 时关键是增大方差，不是增大均值
3. **GSR 在高强度运动时下降**：running(1598) < idle(1688)，可能是血流再分配效应 → 合成时不能简单假设"运动↑→GSR↑"
4. **HR 在 trembling 态最高(76)**：可能反映焦虑/紧张状态 → 合成 BPSD 相关震颤时应同步提升 HR
5. **环境传感器变化缓慢**：温度 25.6-25.8°C、湿度 30.9-32.3%，活动间差异微小 → 合成时环境通道用缓慢漂移模型即可
6. **PPG_IR 的活动差异不大**：各活动间均值差异 <0.5% → PPG_IR 本身不是活动区分特征，HR 的提取才是关键

---

# 三、架构设计

## 3.1 目录结构

```
AD-SensorDataFactory/
│
├── generators/                        # 独立生成器模块
│   ├── base_generator.py             # 基类 BaseActivityGenerator
│   ├── idle_generator.py             # 静坐态
│   ├── walking_generator.py          # 行走态
│   ├── tremor_generator.py           # 震颤态（AD 特异性）
│   ├── sundowning_generator.py       # 日落综合征事件
│   ├── agitation_generator.py        # 激越事件
│   ├── wandering_generator.py        # 徘徊事件
│   ├── apathy_generator.py           # 淡漠态
│   └── sleep_disorder_generator.py   # 睡眠障碍事件
│
├── composers/                         # 组合器
│   ├── daily_composer.py             # 一天的活动序列编排 + 昼夜节律
│   └── longitudinal_composer.py      # 多日/多月的疾病进展轨迹
│
├── profiles/                          # 参数配置
│   ├── normal_baseline.py            # 正常人基线（来自真实采集）
│   ├── stage_profiles.py             # 各 AD 阶段的调制参数
│   ├── bpsd_templates.py             # BPSD 事件模板
│   └── patient_templates.py          # 个性化患者模板
│
├── coupling/                          # 跨模态耦合
│   ├── physiological_rules.py        # 生理耦合规则引擎
│   └── covariance_model.py           # 数据驱动的协方差模型
│
├── validators/                        # 质量验证
│   └── quality_checks.py             # 统计一致性 + 跨模态相关性检查
│
└── factory.py                         # 主入口
```

## 3.2 BaseActivityGenerator（模板类）

参照 VBVR 的 `template-data-generator`，定义所有 generator 的统一接口：

```python
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

class BaseActivityGenerator(ABC):
    """
    传感器活动数据生成器基类。

    设计原则（借鉴 VBVR）：
    1. 参数化：接受语义参数（AD阶段、基线值），不是低层噪声
    2. 确定性：相同 seed 产生相同输出
    3. 标准化输出：CSV 列与硬件采集格式完全一致
    """

    # 标准输出列（与硬件 CSV 一致）
    COLUMNS = [
        't_ms', 'gsr_filtered', 'ppg_ir', 'hr_bpm_avg',
        'imu_ax_mps2', 'imu_ay_mps2', 'imu_az_mps2', 'imu_steps',
        'env_temp_c', 'env_humidity_rh', 'env_pressure_pa', 'env_altitude_m',
        'label'
    ]

    def __init__(self, seed: int, stage: str, patient_profile: dict):
        """
        Args:
            seed: 随机种子（确定性可复现）
            stage: AD 阶段 ('normal', 'scd', 'mci', 'mild_ad', 'moderate_ad', 'severe_ad')
            patient_profile: 个性化参数 {
                'baseline_hr': float,      # 静息心率基线
                'baseline_gsr': float,     # GSR 基线
                'baseline_ppg_ir': float,  # PPG IR 基线
                'baseline_temp': float,    # 环境温度基线
                'baseline_humidity': float, # 环境湿度基线
                'age': int,
                'gender': str,
            }
        """
        self.rng = np.random.default_rng(seed)
        self.seed = seed
        self.stage = stage
        self.profile = patient_profile
        self.stage_modifier = self._get_stage_modifier()

    def generate(self, duration_seconds: float,
                 start_t_ms: int = 0,
                 sampling_rate: int = 50) -> pd.DataFrame:
        """
        生成一段活动的多模态传感器数据。

        Args:
            duration_seconds: 持续时长（秒）
            start_t_ms: 起始时间戳（毫秒）
            sampling_rate: 采样率（Hz），默认50
        Returns:
            pd.DataFrame，列与硬件 CSV 完全一致
        """
        n_samples = int(duration_seconds * sampling_rate)
        interval_ms = 1000 / sampling_rate

        # 各模态独立生成
        imu_data = self._generate_imu(n_samples)
        ppg_data = self._generate_ppg(n_samples)
        eda_data = self._generate_eda(n_samples)
        env_data = self._generate_env(n_samples)

        # 时间戳
        timestamps = [int(start_t_ms + i * interval_ms) for i in range(n_samples)]

        # 组装 DataFrame
        df = pd.DataFrame({
            't_ms': timestamps,
            'gsr_filtered': eda_data['gsr_filtered'],
            'ppg_ir': ppg_data['ppg_ir'],
            'hr_bpm_avg': ppg_data['hr_bpm_avg'],
            'imu_ax_mps2': imu_data['ax'],
            'imu_ay_mps2': imu_data['ay'],
            'imu_az_mps2': imu_data['az'],
            'imu_steps': imu_data['steps'],
            'env_temp_c': env_data['temp'],
            'env_humidity_rh': env_data['humidity'],
            'env_pressure_pa': env_data['pressure'],
            'env_altitude_m': env_data['altitude'],
            'label': self.label
        })

        return df

    @property
    @abstractmethod
    def label(self) -> str:
        """活动标签（与硬件采集的 label 列一致）"""

    @abstractmethod
    def _generate_imu(self, n_samples: int) -> dict:
        """生成 IMU 数据：ax, ay, az, steps"""

    @abstractmethod
    def _generate_ppg(self, n_samples: int) -> dict:
        """生成 PPG 数据：ppg_ir, hr_bpm_avg"""

    @abstractmethod
    def _generate_eda(self, n_samples: int) -> dict:
        """生成 EDA 数据：gsr_filtered"""

    def _generate_env(self, n_samples: int) -> dict:
        """生成环境数据（所有活动共享 — 缓慢漂移模型）"""
        base_temp = self.profile.get('baseline_temp', 25.7)
        base_hum = self.profile.get('baseline_humidity', 31.5)

        # 缓慢随机漂移（布朗运动）
        temp_drift = np.cumsum(self.rng.normal(0, 0.001, n_samples))
        hum_drift = np.cumsum(self.rng.normal(0, 0.002, n_samples))

        return {
            'temp': base_temp + temp_drift,
            'humidity': base_hum + hum_drift,
            'pressure': np.full(n_samples, 101943.0) + self.rng.normal(0, 0.5, n_samples),
            'altitude': np.full(n_samples, -53.5) + self.rng.normal(0, 0.05, n_samples),
        }

    def _get_stage_modifier(self) -> dict:
        """获取 AD 阶段调制因子"""
        modifiers = {
            'normal': {'activity': 1.0, 'stride_var': 1.0, 'hr': 1.0, 'gsr': 1.0, 'tremor_prob': 1.0},
            'scd':    {'activity': 0.92, 'stride_var': 1.4, 'hr': 1.0, 'gsr': 0.95, 'tremor_prob': 1.5},
            'mci':    {'activity': 0.80, 'stride_var': 2.0, 'hr': 1.05, 'gsr': 0.90, 'tremor_prob': 3.0},
            'mild_ad':    {'activity': 0.67, 'stride_var': 2.8, 'hr': 1.10, 'gsr': 0.85, 'tremor_prob': 5.0},
            'moderate_ad': {'activity': 0.50, 'stride_var': 4.0, 'hr': 1.15, 'gsr': 0.80, 'tremor_prob': 8.0},
            'severe_ad':   {'activity': 0.25, 'stride_var': 6.0, 'hr': 1.20, 'gsr': 0.75, 'tremor_prob': 12.0},
        }
        return modifiers.get(self.stage, modifiers['normal'])

    def get_metadata(self) -> dict:
        """生成元数据（类比 VBVR 的 question_metadata.json）"""
        return {
            'generator': self.__class__.__name__,
            'seed': self.seed,
            'stage': self.stage,
            'patient_profile': self.profile,
            'stage_modifier': self.stage_modifier,
            'label': self.label,
        }
```

## 3.3 具体 Generator 实现示例

### IdleGenerator（静坐态）

```python
class IdleGenerator(BaseActivityGenerator):
    """
    静坐态生成器。

    参数来源：真实数据 idle 态统计
    - SVM: 9.70 ± 0.37（极低变异 — 静止状态）
    - GSR: 1688 ± 79
    - HR: 69 ± 10 bpm
    - PPG_IR: 91145 ± 1130
    """

    @property
    def label(self) -> str:
        return 'idle'

    def _generate_imu(self, n_samples):
        mod = self.stage_modifier
        # 静坐时 IMU 主要是重力分量 + 微小抖动
        # 真实数据: ax~1.39, ay~1.05, az~-9.55 (重力方向)
        ax = 1.39 + self.rng.normal(0, 0.05 * mod['stride_var'], n_samples)
        ay = 1.05 + self.rng.normal(0, 0.05 * mod['stride_var'], n_samples)
        az = -9.55 + self.rng.normal(0, 0.03 * mod['stride_var'], n_samples)

        # AD 患者静坐时可能有不自主震颤叠加
        if self.rng.random() < 0.1 * mod['tremor_prob']:
            tremor_mask = self._inject_micro_tremor(n_samples)
            ax += tremor_mask * self.rng.normal(0, 0.3, n_samples)
            ay += tremor_mask * self.rng.normal(0, 0.3, n_samples)

        return {
            'ax': ax, 'ay': ay, 'az': az,
            'steps': np.zeros(n_samples, dtype=int)
        }

    def _generate_ppg(self, n_samples):
        mod = self.stage_modifier
        baseline_hr = self.profile.get('baseline_hr', 69) * mod['hr']
        baseline_ppg = self.profile.get('baseline_ppg_ir', 91145)

        # HR: 缓慢波动（呼吸性窦性心律不齐 + 随机漂移）
        hr = baseline_hr + self.rng.normal(0, 3, n_samples)
        hr = np.clip(hr, 45, 120)

        # PPG_IR: 基线 + 与 HR 轻微反相关
        ppg_ir = baseline_ppg + self.rng.normal(0, 500, n_samples)

        return {'ppg_ir': ppg_ir.astype(int), 'hr_bpm_avg': hr.astype(int)}

    def _generate_eda(self, n_samples):
        mod = self.stage_modifier
        baseline_gsr = self.profile.get('baseline_gsr', 1688) * mod['gsr']

        # GSR: tonic 缓慢漂移 + 偶尔的 phasic 响应（NS-SCR）
        tonic = baseline_gsr + np.cumsum(self.rng.normal(0, 0.1, n_samples))

        # 非特异性 SCR: 每分钟 1-5 次随机 spike
        scr_rate = 3 / 60 / 50  # 3次/分钟, 50Hz采样
        scr_events = self.rng.random(n_samples) < scr_rate
        scr_signal = np.zeros(n_samples)
        for i in np.where(scr_events)[0]:
            decay = np.exp(-np.arange(min(100, n_samples - i)) / 30)  # 2秒衰减
            scr_signal[i:i+len(decay)] += self.rng.uniform(5, 30) * decay

        return {'gsr_filtered': (tonic + scr_signal).astype(int)}

    def _inject_micro_tremor(self, n_samples):
        """注入微弱的不自主震颤（AD 患者特有）"""
        # 3-6Hz 的不规则震颤
        t = np.arange(n_samples) / 50.0
        freq = self.rng.uniform(3, 6)
        tremor = np.sin(2 * np.pi * freq * t + self.rng.uniform(0, 2*np.pi))
        # 间歇性出现（不是持续的）
        envelope = np.zeros(n_samples)
        burst_starts = self.rng.choice(n_samples, size=max(1, n_samples//500), replace=False)
        for start in burst_starts:
            burst_len = self.rng.integers(25, 150)  # 0.5-3秒
            end = min(start + burst_len, n_samples)
            envelope[start:end] = 1.0
        return tremor * envelope
```

### WalkingGenerator（行走态）

```python
class WalkingGenerator(BaseActivityGenerator):
    """
    行走态生成器。

    参数来源：真实数据 walking 态统计
    - SVM: 10.47 ± 1.45（周期性步态模式）
    - GSR: 1705 ± 58
    - HR: 64 ± 5 bpm
    - 特征: 步态周期性（~2Hz正常步频）
    """

    @property
    def label(self) -> str:
        return 'walking'

    def _generate_imu(self, n_samples):
        mod = self.stage_modifier
        t = np.arange(n_samples) / 50.0  # 时间轴（秒）

        # 步态基频: 正常 ~1.8-2.0 Hz, AD 患者逐步降低
        cadence_hz = self.rng.uniform(1.8, 2.0) * mod['activity']

        # 步态周期性信号 + 随机变异
        # 步态变异性 (stride-to-stride CV) 是 AD 的核心指标
        stride_noise = self.rng.normal(0, 0.1 * mod['stride_var'], n_samples)
        gait_signal = np.sin(2 * np.pi * cadence_hz * t + np.cumsum(stride_noise))

        # 三轴加速度（手部佩戴 → 摆臂运动模式）
        ax = 1.39 + 0.8 * gait_signal + self.rng.normal(0, 0.3 * mod['stride_var'], n_samples)
        ay = 1.05 + 0.5 * np.sin(2 * np.pi * cadence_hz * t * 2) + self.rng.normal(0, 0.2, n_samples)
        az = -9.55 + 0.3 * gait_signal + self.rng.normal(0, 0.15, n_samples)

        # 步数累计（每个步态周期 +1）
        peaks = np.diff(np.sign(np.diff(gait_signal))) < -1
        steps = np.cumsum(np.concatenate([[0, 0], peaks.astype(int)]))

        return {'ax': ax, 'ay': ay, 'az': az, 'steps': steps}

    def _generate_ppg(self, n_samples):
        mod = self.stage_modifier
        baseline_hr = self.profile.get('baseline_hr', 64) * mod['hr']

        # 行走时 HR 轻微提升 + 步态耦合的微小波动
        hr_walk = baseline_hr + self.rng.uniform(3, 8)
        hr = hr_walk + self.rng.normal(0, 2, n_samples)

        ppg_ir = self.profile.get('baseline_ppg_ir', 90812) + self.rng.normal(0, 400, n_samples)

        return {'ppg_ir': ppg_ir.astype(int), 'hr_bpm_avg': hr.astype(int)}

    def _generate_eda(self, n_samples):
        mod = self.stage_modifier
        baseline_gsr = self.profile.get('baseline_gsr', 1705) * mod['gsr']

        # 行走时 GSR 轻微上升（轻度交感激活）
        tonic = baseline_gsr + np.cumsum(self.rng.normal(0, 0.05, n_samples))
        return {'gsr_filtered': tonic.astype(int)}
```

### TremorGenerator（震颤态 — AD 特异性）

```python
class TremorGenerator(BaseActivityGenerator):
    """
    震颤态生成器。

    参数来源：真实数据 trembling 态统计
    - SVM 均值: 10.16 (接近 idle)
    - SVM 标准差: 2.91 (是 idle 的 8 倍 — 核心区分特征)
    - HR: 76 ± 5 bpm (高于其他活动)
    - GSR: 1678 ± 39

    AD 震颤特点 (vs 帕金森):
    - 不规则、无节律 (PD 是规则的 4-6Hz)
    - 主要是姿势性/意向性震颤
    - 频率 3-12Hz, 混合多频率成分
    """

    @property
    def label(self) -> str:
        return 'trembling'

    def _generate_imu(self, n_samples):
        mod = self.stage_modifier
        t = np.arange(n_samples) / 50.0

        # AD 震颤: 多频率叠加 + 不规则包络
        n_components = self.rng.integers(2, 5)  # 2-4 个频率成分
        tremor_signal = np.zeros(n_samples)
        for _ in range(n_components):
            freq = self.rng.uniform(3, 12)  # 3-12 Hz
            amp = self.rng.uniform(0.3, 1.5) * mod['stride_var']
            phase = self.rng.uniform(0, 2 * np.pi)
            # 频率和幅度都在缓慢变化（不规则性）
            freq_var = freq + np.cumsum(self.rng.normal(0, 0.01, n_samples))
            amp_var = amp * (1 + 0.3 * np.sin(2 * np.pi * 0.1 * t))
            tremor_signal += amp_var * np.sin(2 * np.pi * freq_var * t + phase)

        # 间歇性包络（震颤不是持续的，有强弱变化）
        envelope = np.ones(n_samples)
        n_gaps = self.rng.integers(1, 4)
        for _ in range(n_gaps):
            gap_start = self.rng.integers(0, max(1, n_samples - 100))
            gap_len = self.rng.integers(25, 200)
            gap_end = min(gap_start + gap_len, n_samples)
            envelope[gap_start:gap_end] *= self.rng.uniform(0.1, 0.5)

        tremor_signal *= envelope

        # 基线 + 震颤叠加
        ax = 1.39 + tremor_signal + self.rng.normal(0, 0.1, n_samples)
        ay = 1.05 + tremor_signal * 0.7 + self.rng.normal(0, 0.1, n_samples)
        az = -9.55 + tremor_signal * 0.3 + self.rng.normal(0, 0.05, n_samples)

        return {'ax': ax, 'ay': ay, 'az': az, 'steps': np.zeros(n_samples, dtype=int)}

    def _generate_ppg(self, n_samples):
        mod = self.stage_modifier
        # trembling 态 HR 偏高（76 bpm），反映焦虑/紧张
        baseline_hr = self.profile.get('baseline_hr', 69) * mod['hr']
        hr_tremor = baseline_hr + self.rng.uniform(5, 12)  # 比静息高 5-12 bpm
        hr = hr_tremor + self.rng.normal(0, 2, n_samples)

        ppg_ir = self.profile.get('baseline_ppg_ir', 91084) + self.rng.normal(0, 200, n_samples)
        return {'ppg_ir': ppg_ir.astype(int), 'hr_bpm_avg': hr.astype(int)}

    def _generate_eda(self, n_samples):
        mod = self.stage_modifier
        baseline_gsr = self.profile.get('baseline_gsr', 1678) * mod['gsr']

        # 震颤伴随的交感神经激活 → GSR 微升
        tonic = baseline_gsr + self.rng.uniform(10, 50)
        gsr = tonic + np.cumsum(self.rng.normal(0, 0.08, n_samples))

        # 偶尔的焦虑相关 SCR spike
        scr_rate = 5 / 60 / 50  # 5次/分钟
        scr_events = self.rng.random(n_samples) < scr_rate
        for i in np.where(scr_events)[0]:
            decay_len = min(75, n_samples - i)
            decay = np.exp(-np.arange(decay_len) / 25)
            gsr[i:i+decay_len] += self.rng.uniform(10, 40) * decay

        return {'gsr_filtered': gsr.astype(int)}
```

## 3.4 BPSD 事件 Generator（叠加式）

BPSD 事件不是独立的活动，而是**叠加在基础活动上的修饰器**。

```python
class BPSDEventGenerator:
    """
    BPSD 事件叠加生成器。

    不直接生成数据，而是对已有的基础活动数据施加 BPSD 事件效应。
    参考: Lazarou 2024 (PsyCo + BePhyEn 双模型), Spasojevic 2021 (事件模板)
    """

    # 事件模板（文献参数 + 真实数据校准）
    TEMPLATES = {
        'agitation': {
            'duration_range': (20*60, 60*60),     # 20-60分钟（秒）
            'gsr_modifier': (1.5, 2.0),            # GSR ×1.5-2.0
            'hr_modifier': (1.15, 1.30),           # HR ×1.15-1.30
            'imu_svm_modifier': (1.5, 2.0),       # 活动 ×1.5-2.0
            'imu_var_modifier': (2.0, 4.0),        # IMU 方差 ×2-4
            'onset_shape': 'sigmoid',              # 渐进性发作
        },
        'sundowning': {
            'duration_range': (60*60, 120*60),     # 60-120分钟
            'time_window': (16, 18),               # 16:00-18:00
            'gsr_modifier': (1.3, 1.8),
            'hr_modifier': (1.10, 1.25),
            'imu_var_modifier': (1.5, 3.0),
            'onset_shape': 'gradual',              # 极缓慢发展
        },
        'anxiety': {
            'duration_range': (15*60, 45*60),
            'gsr_modifier': (1.4, 1.8),           # GSR 先于 HR 变化
            'hr_modifier': (1.10, 1.20),
            'imu_var_modifier': (1.2, 1.8),
            'onset_shape': 'sharp',                # 较快发作
        },
        'apathy': {
            'duration_range': (60*60, 240*60),     # 1-4小时
            'gsr_modifier': (0.6, 0.8),            # GSR 下降
            'hr_modifier': (0.95, 1.0),
            'imu_svm_modifier': (0.3, 0.6),       # 活动显著减少
            'imu_var_modifier': (0.5, 0.8),
            'onset_shape': 'gradual',
        },
        'wandering': {
            'duration_range': (15*60, 60*60),
            'gsr_modifier': (1.1, 1.3),
            'hr_modifier': (1.05, 1.15),
            'imu_svm_modifier': (1.3, 1.8),
            'imu_var_modifier': (2.0, 4.0),       # 步态高度不规则
            'onset_shape': 'sigmoid',
        },
        'sleep_disorder': {
            'duration_range': (30*60, 180*60),
            'time_window': (23, 5),                # 夜间 23:00-05:00
            'gsr_modifier': (1.0, 1.2),
            'hr_modifier': (1.05, 1.15),
            'imu_svm_modifier': (2.0, 4.0),       # 夜间异常活动
            'onset_shape': 'intermittent',         # 间歇性
        },
    }

    def __init__(self, seed: int, event_type: str, intensity: float = 1.0):
        """
        Args:
            seed: 随机种子
            event_type: BPSD 事件类型（对应 TEMPLATES 的 key）
            intensity: 事件强度 0.0-2.0（1.0 为标准强度）
        """
        self.rng = np.random.default_rng(seed)
        self.event_type = event_type
        self.template = self.TEMPLATES[event_type]
        self.intensity = intensity

    def apply(self, df: pd.DataFrame, event_start_idx: int) -> pd.DataFrame:
        """
        将 BPSD 事件叠加到已有数据上。

        Args:
            df: 基础活动数据（来自 BaseActivityGenerator）
            event_start_idx: 事件开始的行索引
        Returns:
            修改后的 DataFrame（BPSD 效应已叠加）
        """
        duration_samples = self.rng.integers(
            self.template['duration_range'][0] * 50,  # 秒→样本数
            self.template['duration_range'][1] * 50
        )
        end_idx = min(event_start_idx + duration_samples, len(df))

        # 生成事件包络（bell curve / sigmoid / gradual）
        envelope = self._make_envelope(end_idx - event_start_idx)

        # 施加修饰
        if 'gsr_modifier' in self.template:
            lo, hi = self.template['gsr_modifier']
            modifier = self.rng.uniform(lo, hi) * self.intensity
            delta = (modifier - 1.0) * envelope
            df.loc[event_start_idx:end_idx-1, 'gsr_filtered'] *= (1 + delta)

        if 'hr_modifier' in self.template:
            lo, hi = self.template['hr_modifier']
            modifier = self.rng.uniform(lo, hi) * self.intensity
            delta = (modifier - 1.0) * envelope
            df.loc[event_start_idx:end_idx-1, 'hr_bpm_avg'] *= (1 + delta)

        if 'imu_var_modifier' in self.template:
            lo, hi = self.template['imu_var_modifier']
            modifier = self.rng.uniform(lo, hi) * self.intensity
            # 增大 IMU 方差（注入额外噪声）
            n = end_idx - event_start_idx
            extra_noise = self.rng.normal(0, 0.5 * modifier, n) * envelope
            df.loc[event_start_idx:end_idx-1, 'imu_ax_mps2'] += extra_noise

        return df

    def _make_envelope(self, n_samples: int) -> np.ndarray:
        """生成事件强度包络"""
        t = np.linspace(0, 1, n_samples)
        shape = self.template.get('onset_shape', 'sigmoid')

        if shape == 'sigmoid':
            # S 形：渐起 → 平台 → 渐落
            return np.sin(np.pi * t)
        elif shape == 'gradual':
            # 极缓慢上升 → 缓慢下降
            return np.sin(np.pi * t) ** 0.5
        elif shape == 'sharp':
            # 快速上升 → 缓慢下降
            return np.exp(-3 * (t - 0.2) ** 2 / 0.1) * (t > 0.05)
        elif shape == 'intermittent':
            # 间歇性爆发
            bursts = np.zeros(n_samples)
            n_bursts = self.rng.integers(3, 8)
            for _ in range(n_bursts):
                center = self.rng.uniform(0.1, 0.9)
                width = self.rng.uniform(0.02, 0.1)
                bursts += np.exp(-((t - center) ** 2) / (2 * width ** 2))
            return np.clip(bursts, 0, 1)
        else:
            return np.ones(n_samples)
```

## 3.5 DailyComposer（一天活动编排器）

```python
class DailyComposer:
    """
    将多个 generator 的输出组合成一整天的传感器数据。

    编排逻辑:
    1. 定义一天的活动时间表（活动类型 + 时长）
    2. 依次调用对应的 generator
    3. 在活动之间插入平滑过渡
    4. 叠加 BPSD 事件
    5. 应用昼夜节律调制
    """

    # 正常老人一天的典型活动模式
    DAILY_SCHEDULE_NORMAL = [
        # (起始时间, 活动, 持续分钟)
        ('07:00', 'idle', 30),      # 起床静坐
        ('07:30', 'walking', 15),   # 晨间活动
        ('07:45', 'idle', 135),     # 早餐+休息
        ('10:00', 'walking', 20),   # 散步
        ('10:20', 'idle', 100),     # 静坐休息
        ('12:00', 'idle', 60),      # 午餐
        ('13:00', 'idle', 90),      # 午休
        ('14:30', 'walking', 15),   # 下午活动
        ('14:45', 'idle', 135),     # 休息
        ('17:00', 'walking', 10),   # 傍晚活动
        ('17:10', 'idle', 110),     # 晚餐+休息
        ('19:00', 'idle', 120),     # 晚间休息
        ('21:00', 'idle', 60),      # 睡前
    ]

    def compose(self, seed: int, stage: str, patient_profile: dict,
                bpsd_events: list = None) -> pd.DataFrame:
        """
        生成一整天的合成传感器数据。

        Args:
            seed: 主种子
            stage: AD 阶段
            patient_profile: 患者参数
            bpsd_events: BPSD 事件列表 [{'type': 'agitation', 'time': '15:30', 'intensity': 1.2}, ...]
        Returns:
            一天的完整 DataFrame
        """
        rng = np.random.default_rng(seed)
        schedule = self._modify_schedule_for_stage(stage, rng)

        all_segments = []
        current_t_ms = 0

        for time_str, activity, duration_min in schedule:
            gen_seed = rng.integers(0, 2**31)
            generator = self._get_generator(activity, gen_seed, stage, patient_profile)
            segment = generator.generate(
                duration_seconds=duration_min * 60,
                start_t_ms=current_t_ms,
                sampling_rate=50
            )
            all_segments.append(segment)
            current_t_ms = segment['t_ms'].iloc[-1] + 20  # 20ms interval

        df = pd.concat(all_segments, ignore_index=True)

        # 叠加 BPSD 事件
        if bpsd_events:
            for event in bpsd_events:
                evt_gen = BPSDEventGenerator(
                    seed=rng.integers(0, 2**31),
                    event_type=event['type'],
                    intensity=event.get('intensity', 1.0)
                )
                # 找到对应时间的索引
                start_idx = self._time_to_index(event['time'], df)
                df = evt_gen.apply(df, start_idx)

        # 昼夜节律调制
        df = self._apply_circadian(df)

        return df
```

---

# 四、跨模态耦合规则引擎

## 4.1 生理耦合规则

Di Martino & Delmastro (2025) 指出跨模态一致性是当前深度生成模型的关键失败点。本方案使用领域知识手动编码生理耦合，确保合成数据中多传感器之间保持生理合理的相关性。

```python
class PhysiologicalCouplingEngine:
    """
    跨模态生理耦合规则引擎。

    在各 generator 独立生成数据后，对全天数据施加耦合修正。
    """

    RULES = {
        'motion_to_hr': {
            'description': '运动强度 → 心率提升',
            'delay_samples': 250,   # 5秒延迟 (250 samples @ 50Hz)
            'formula': 'HR += 0.3 * max(0, SVM - 9.7) * baseline_HR / 70',
            'source': 'Physiological: exercise-induced tachycardia',
        },
        'motion_to_gsr': {
            'description': '运动强度 → GSR 变化（非线性）',
            'note': '轻度运动 GSR↑（交感激活），剧烈运动 GSR↓（血流再分配）',
            'threshold_svm': 11.5,
            'source': '真实数据: running GSR(1598) < idle GSR(1688)',
        },
        'emotion_to_gsr_hr': {
            'description': 'BPSD 情绪事件 → GSR 先于 HR 变化',
            'gsr_delay_samples': 25,   # 0.5秒（交感快速通路）
            'hr_delay_samples': 375,   # 7.5秒（心血管响应）
            'source': 'Setz et al. 2010; autonomic nervous system pathways',
        },
        'activity_to_env': {
            'description': '活动 → 手套内温湿度变化',
            'temp_increase_per_svm': 0.02,  # °C per SVM unit
            'humidity_increase_per_svm': 0.1,  # % per SVM unit
            'source': '推断: 运动→出汗→手套内微环境变化',
        },
        'circadian_rhythm': {
            'description': '昼夜节律对所有通道的调制',
            'periods': {
                '07-09': {'activity': 0.7, 'hr': 0.95, 'gsr': 0.9},
                '09-12': {'activity': 1.0, 'hr': 1.0, 'gsr': 1.0},
                '12-14': {'activity': 0.85, 'hr': 0.98, 'gsr': 0.95},
                '14-16': {'activity': 0.95, 'hr': 1.0, 'gsr': 1.0},
                '16-18': {'activity': 1.0, 'hr': 1.05, 'gsr': 1.15},  # sundowning window
                '18-20': {'activity': 0.85, 'hr': 1.0, 'gsr': 1.0},
                '20-22': {'activity': 0.7, 'hr': 0.95, 'gsr': 0.9},
            },
            'source': 'Lazarou 2024: circadian BPSD patterns',
        },
    }
```

## 4.2 协方差矩阵（数据驱动补充）

从真实采集数据估计多传感器间的协方差，用于给合成数据注入统计相关性：

```python
def estimate_covariance_from_real_data(csv_path: str) -> np.ndarray:
    """从真实传感器数据估计跨模态协方差矩阵"""
    import pandas as pd
    import numpy as np

    df = pd.read_csv(csv_path)
    df['imu_svm'] = np.sqrt(df['imu_ax_mps2']**2 + df['imu_ay_mps2']**2 + df['imu_az_mps2']**2)

    features = ['gsr_filtered', 'ppg_ir', 'hr_bpm_avg', 'imu_svm', 'env_temp_c', 'env_humidity_rh']
    cov = df[features].cov()
    return cov
```

---

# 五、质量验证框架

## 5.1 统计一致性检验

合成数据应通过以下检验：

| 检验项 | 方法 | 通过标准 |
|--------|------|---------|
| 均值一致性 | 合成 vs 真实（同活动）的 t-test | p > 0.05 |
| 方差一致性 | Levene's test | p > 0.05 |
| 分布一致性 | KS test (Kolmogorov-Smirnov) | p > 0.05 |
| 跨模态相关性 | Pearson correlation matrix 比较 | 相关系数差 < 0.15 |
| 时序自相关 | ACF (Auto-Correlation Function) 比较 | 前10阶 ACF 差 < 0.1 |
| 下游任务效用 | TSTR (Train Synthetic, Test Real) | 准确率下降 < 10% |

## 5.2 VBVR 式元数据

每次生成附带完整元数据（类比 VBVR 的 `question_metadata.json`）：

```json
{
  "generator_version": "1.0.0",
  "seed": 42,
  "stage": "mci",
  "patient_profile": {
    "age": 72,
    "gender": "female",
    "baseline_hr": 72,
    "baseline_gsr": 1650
  },
  "daily_schedule": [...],
  "bpsd_events_injected": [
    {"type": "sundowning", "time": "16:30", "intensity": 1.2, "duration_min": 85}
  ],
  "stage_modifiers_applied": {...},
  "coupling_rules_active": ["motion_to_hr", "circadian_rhythm"],
  "quality_checks_passed": true,
  "generation_timestamp": "2026-03-26T12:00:00"
}
```

---

# 六、分阶段升级路径

| Phase | 数据量 | 合成方法 | 目的 |
|-------|--------|---------|------|
| **Phase 0（当前）** | 文献参数 + 正常人基线（26K行） | 参数化 Generator + BPSD 模板 + 规则耦合 | Agent 逻辑验证、管道测试 |
| **Phase 1** | 30 例 AD 患者 | + SMOTE 增强 + 真实协方差矩阵 | 分类器初训、个性化基线 |
| **Phase 2-3** | 100 例多阶段患者 | + TimeGAN / 条件扩散模型 | 高保真增强、隐私保护共享 |
| **Phase 4** | 200+ 纵向随访 | + SynLS 扩散 + 疾病进展模型 | 临床试验仿真 |

**关键原则**：规则引擎始终保留作为"相关性骨架"。即使升级到深度生成模型，规则引擎也用于后处理校验——如果生成的数据违反生理耦合规则（如运动↑但HR↓），则标记为低质量或重新生成。

---

*文档版本: v1.0 · 创建日期: 2026-03-26*
*基于 VBVR DataFactory 架构 + 真实传感器基线数据 (all_sensors_log_withLabel20260326_093901.csv)*
