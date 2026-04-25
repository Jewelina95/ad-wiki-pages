---
title: preprocessing per modality
type: method
last_updated: 2026-04-25
status: settled
---

# 传感器数据预处理与Agent接口设计

> 完整数据流: 原始传感器信号 → 预处理+特征提取 → CSV存储 → Agent MCP工具自动读取

---

## 1. 数据流全景图

```
┌────────────────────────────────────────────────────────────────────────┐
│  第一阶段: 设备端 (手套MCU + BLE)                                        │
│                                                                         │
│  IMU 50Hz ──┐                                                          │
│  PPG 64Hz ──┤── BLE ──→ 手机App                                        │
│  EDA  4Hz ──┤                                                          │
│  Mic 16kHz ─┘                                                          │
└────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────────┐
│  第二阶段: 手机App / 边缘预处理                                          │
│                                                                         │
│  原始信号 → [preprocessing.py] → 特征提取 (每5分钟聚合)                   │
│                                                                         │
│  IMU 15000点 → 步速/步频/变异性/震颤/活动量  (1行)                       │
│  PPG 19200点 → HR/SpO2/SDNN/RMSSD/LF_HF     (1行)                      │
│  EDA  1200点 → SCL/SCR次数/SCR幅度/NS-SCR率  (1行)                       │
│  Audio(语音段)→ F0/Jitter/Shimmer/HNR/MFCC    (1行)                     │
│           └→ Whisper ASR → 语速/停顿率/TTR/MLU/语义连贯性               │
└────────────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP POST (每5分钟, JSON)
                              ▼
┌────────────────────────────────────────────────────────────────────────┐
│  第三阶段: 后端服务器                                                    │
│                                                                         │
│  FastAPI /api/upload                                                    │
│       │                                                                 │
│       ├─→ data/raw/{patient_id}/{sensor}_{date}.csv    (分传感器原始)     │
│       └─→ data/features/{patient_id}/multimodal_{date}.csv (融合特征)    │
│                                                                         │
│  每小时 Scheduler触发:                                                   │
│       │                                                                 │
│       ▼                                                                 │
│  AgentDataLoader.format_for_agent(patient_id)                           │
│       │  读取: 最新12条特征 + 患者档案 + 基线 + 近期评估                  │
│       │                                                                 │
│       ▼                                                                 │
│  MasterCoordinator.evaluate()                                           │
│       │  7个专科Agent并发评估 → 综合推理 → CoordinatorDecision            │
│       │                                                                 │
│       ├─→ data/assessments/{patient_id}/{date}.jsonl   (评估结果)        │
│       └─→ data/alerts/ (如有红/黄色预警)                                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 预处理详细流程

### 2.1 EDA预处理

```
原始 4Hz EDA信号 (5分钟 = 1200点)
    │
    ▼ 低通滤波 (Butterworth 4阶, cutoff 1Hz)
    │
    ▼ 运动伪迹检测 (一阶差分 > 阈值 → 标记)
    │
    ▼ cvxEDA分解 (NeuroKit2)
    ├─→ Tonic成分 (SCL) → 均值 = scl
    └─→ Phasic成分 (SCR) → 峰值检测
         ├─→ scr_count (峰值个数)
         ├─→ scr_amplitude (峰值均幅)
         └─→ ns_scr_rate (非特异性SCR频率)
```

**关键参数:**
- 采样率: ≥4Hz (Setz 2010: >15Hz无额外信息增益)
- cvxEDA: 凸优化分解, gold standard (Benedek 2010)
- SCR阈值: amplitude > 0.01μS, min_rise_time > 0.1s
- 工具: `neurokit2.eda_process()`

### 2.2 PPG/HRV预处理

```
原始 64Hz PPG信号 (5分钟 = 19200点)
    │
    ▼ 带通滤波 (0.5-8Hz, Butterworth 3阶)
    │
    ▼ 运动伪迹去除 (自适应滤波, IMU参考通道)
    │
    ▼ PPG峰值检测 (NeuroKit2)
    │
    ▼ IBI计算 (峰值间距, ms)
    │
    ▼ IBI去伪迹 (Malik法: 相邻差>20% → 插值)
    │
    ├─→ 心率: heart_rate = 60000 / mean(IBI)
    │
    ├─→ 时域HRV:
    │   ├─→ sdnn = std(IBI)
    │   ├─→ rmssd = sqrt(mean(diff(IBI)²))
    │   └─→ pnn50 = count(|diff(IBI)|>50ms) / count(diff)
    │
    └─→ 频域HRV (Welch PSD):
        ├─→ LF = power(0.04-0.15Hz) → 交感+副交感
        ├─→ HF = power(0.15-0.4Hz) → 副交感
        └─→ lf_hf_ratio = LF/HF → 交感张力指标
```

**关键参数:**
- 采样率: ≥64Hz (Task Force 1996)
- 最小窗口: 5分钟 (短期HRV标准)
- 正常参考: SDNN 141±39ms, RMSSD 27±12ms (Shaffer 2017)
- 工具: `neurokit2.ppg_process()` + `neurokit2.hrv()`

### 2.3 IMU/步态预处理

```
原始 50Hz 三轴加速度 (5分钟 = 15000点×3)
    │
    ▼ 低通滤波 (20Hz, 去高频噪声)
    │
    ▼ 计算SVM = sqrt(ax²+ay²+az²)
    │
    ├─→ 步态分析:
    │   ▼ 带通滤波 (0.5-3Hz, 步态频段)
    │   ▼ 峰值检测 (min_distance=0.33s)
    │   ├─→ cadence = n_steps / duration_min
    │   ├─→ stride_variability = CV(step_intervals) × 100%
    │   └─→ gait_speed = step_length × cadence/60
    │       (Weinberg模型: step_len = 0.4 × Δa^0.25)
    │
    ├─→ 手部震颤:
    │   ▼ 带通滤波 (3-12Hz, 震颤频段)
    │   ▼ FFT功率谱
    │   └─→ hand_tremor_score (0-10, 功率归一化)
    │
    └─→ 活动量:
        ▼ SVM - 9.8 (去重力)
        └─→ activity_level = mean(dynamic_acc) / 3.0
```

**关键参数:**
- 采样率: ≥50Hz (Montero-Odasso 2019)
- 步态变异性CV>5% → 神经退行风险 (Hausdorff 2005)
- 步速下降>0.023m/s/年 → MCI预测 (Buracchio 2010)

### 2.4 语音预处理

```
原始 16kHz 音频 (语音段)
    │
    ▼ 预加重 (0.97系数)
    │
    ├─→ 声学特征 (无需ASR):
    │   ├─→ F0 (pYIN算法, librosa) → f0_mean
    │   ├─→ Jitter (周期变异) → 声带控制
    │   ├─→ Shimmer (幅度变异) → 声带闭合力
    │   ├─→ HNR (谐噪比) → 发声质量
    │   └─→ MFCC (13维) → 语音整体表示
    │
    ├─→ 停顿分析 (基于RMS能量VAD):
    │   └─→ pause_rate = 静默时长 / 总时长
    │
    └─→ 语言学特征 (需ASR转录):
        │  Whisper large-v3 → 中文文本
        │
        ├─→ speech_rate = 词数 / 分钟
        ├─→ ttr = 不同词数 / 总词数 (jieba分词)
        ├─→ mlu = 平均句长 (词/句)
        └─→ semantic_coherence = 相邻句词汇重叠度
```

**关键参数:**
- 停顿率是AD最敏感的单一语音特征 (König 2015, AUC 0.78)
- ADReSS Challenge: 声学+语言学组合 AUC>0.85
- TAUKADIAL 2024: 中文AD语音检测 AUC 0.78-0.85

---

## 3. 代码模块说明

### 3.1 文件结构

```
src/sensors/
├── __init__.py
├── preprocessing.py    # 各传感器预处理函数
│   ├── preprocess_eda()   → EDAProcessedFeatures
│   ├── preprocess_ppg()   → PPGProcessedFeatures
│   ├── preprocess_imu()   → IMUProcessedFeatures
│   └── preprocess_audio() → AudioProcessedFeatures
│
├── data_pipeline.py    # 数据管道与Agent接口
│   ├── SensorDataPipeline   # 统一预处理入口
│   ├── CSVWriter            # 特征→CSV存储
│   ├── AgentDataLoader      # Agent端数据读取
│   └── PipelineRunner       # 端到端管道
│
└── synthetic.py        # 合成数据生成
    ├── STAGE_PROFILES       # 各AD阶段参数分布
    ├── BPSD_EVENT_PROFILES  # BPSD事件模板
    └── SyntheticDataGenerator
        ├── generate_patient_day()     # 一天数据
        ├── generate_patient_profile() # 患者档案
        ├── generate_baseline()        # 个体基线
        └── generate_test_dataset()    # 完整测试集
```

### 3.2 使用示例

**生成测试数据:**
```python
from src.sensors.synthetic import SyntheticDataGenerator

gen = SyntheticDataGenerator(data_root="data", seed=42)

# 生成6个患者×3天的完整测试集
summary = gen.generate_test_dataset(
    n_patients=6,
    stages=["normal", "scd", "mci", "mild_ad", "moderate_ad", "severe_ad"],
    days=3,
    include_bpsd=True,
)
# 或直接运行: python -m scripts.generate_test_data
```

**Agent读取数据:**
```python
from src.sensors.data_pipeline import AgentDataLoader

loader = AgentDataLoader(data_root="data")

# 获取Agent评估所需的全部上下文 (一个字符串)
context = loader.format_for_agent("patient_003")
# 返回: 患者档案 + 最新12条传感器CSV + 基线 + 近期评估

# 或分别获取
df = loader.load_latest_features("patient_003", n_rows=12)
profile = loader.load_patient_profile("patient_003")
baseline = loader.load_baseline("patient_003")
history = loader.load_history("patient_003", days=7)
```

**端到端管道 (真实数据接入时):**
```python
from src.sensors.data_pipeline import PipelineRunner
import numpy as np

runner = PipelineRunner(data_root="data")

# 接收原始信号 → 预处理 → 存储
features = runner.ingest(
    patient_id="patient_001",
    eda_raw=np.random.randn(1200) * 0.5 + 3.0,   # 5分钟@4Hz
    ppg_raw=np.random.randn(19200) * 0.2 + 1.0,   # 5分钟@64Hz
    imu_acc=np.random.randn(15000, 3) * 0.1 + [0, 0, 9.8],  # 5分钟@50Hz
)

# 获取Agent上下文
context = runner.get_agent_context("patient_001")
```

---

## 4. 合成数据设计

### 4.1 各AD阶段的关键参数差异

| 特征 | Normal | SCD | MCI | Mild AD | Moderate AD |
|------|--------|-----|-----|---------|-------------|
| 步速 (m/s) | 1.20±0.15 | 1.10±0.15 | 0.95±0.18 | 0.80±0.20 | 0.60±0.20 |
| 步态变异性 (%) | 2.5±0.8 | 3.5±1.0 | 5.0±1.5 | 7.0±2.0 | 10.0±3.0 |
| SDNN (ms) | 50±12 | 42±10 | 35±10 | 28±8 | 22±7 |
| 停顿率 | 0.15±0.05 | 0.20±0.06 | 0.30±0.08 | 0.40±0.10 | 0.55±0.12 |
| TTR | 0.72±0.05 | 0.65±0.06 | 0.55±0.07 | 0.45±0.08 | 0.35±0.08 |
| 语义连贯性 | 0.82±0.05 | 0.75±0.06 | 0.62±0.08 | 0.48±0.10 | 0.35±0.10 |

### 4.2 BPSD事件注入

合成数据支持在MCI及以上阶段注入BPSD事件:
- **激越**: EDA↑50-100% + HR↑15-30% + 活动↑, 持续20-60分钟
- **日落综合征**: 16:00-18:00渐进性EDA+HR升高
- **焦虑**: EDA↑40-80% + HR↑10-20%, 活动正常
- **淡漠**: 活动↓40-70% + EDA↓20-40%
- **游荡**: 步态变异↑50-100% + 活动↑30-80%
- **睡眠障碍**: 夜间HR↑5-15% + 活动↑100-300%

事件以渐进方式叠加（正弦曲线调制），模拟真实的逐渐加重和缓解过程。

### 4.3 昼夜节律

合成数据包含生理合理的昼夜调制:
- 清晨(7-9h): 活动逐渐升高
- 上午(9-12h): 活跃期
- 午后(13-15h): 轻微低谷
- 下午(15-18h): 回升 + 日落窗口
- 晚间(18-22h): 逐渐降低

---

## 5. 依赖安装

```bash
# 核心依赖
pip install numpy pandas scipy

# 预处理 (处理真实信号时需要)
pip install neurokit2 librosa

# 语音ASR (可选)
pip install openai-whisper jieba

# API服务
pip install fastapi uvicorn

# Agent后端
pip install anthropic
# 或 pip install claude-agent-sdk
```

---

## 6. 快速开始

```bash
# 1. 生成测试数据
python -m scripts.generate_test_data

# 2. 验证数据
ls data/features/patient_003/
cat data/patients/patient_003.json

# 3. 启动FastAPI (如需HTTP接口)
uvicorn src.server:app --port 8000

# 4. Agent可直接通过AgentDataLoader或MCP Tool读取CSV
```
