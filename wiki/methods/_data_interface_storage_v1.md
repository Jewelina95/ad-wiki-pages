---
title:  data interface storage v1
type: method
last_updated: 2026-04-25
status: settled
---

# AD 传感器数据接口与存储方案

> 设计原则：**够用就行，不过度设计**。CSV 存数据，FastAPI 收数据，Claude Agent SDK 跑推理。

---

## 1. 整体架构

```
┌──────────────────┐
│  可穿戴设备 MCU    │  IMU 50Hz / PPG 64Hz / EDA 4Hz / Mic 16kHz
└────────┬─────────┘
         │ BLE
         ▼
┌──────────────────┐
│  手机 App          │  边缘预处理：
│                    │  - 原始信号 → 特征提取（每1-5分钟聚合一次）
│                    │  - 打包成 JSON
└────────┬─────────┘
         │ HTTP POST（每1-5分钟一次）
         ▼
┌──────────────────────────────────────────────────┐
│  后端服务器（你的电脑 / 云服务器）                      │
│                                                    │
│  ┌──────────┐     ┌───────────┐     ┌───────────┐ │
│  │ FastAPI   │────▶│ CSV 文件   │────▶│ Claude    │ │
│  │ 接收数据   │     │ 存储原始+  │     │ Agent SDK │ │
│  │           │     │ 特征数据   │     │ 7个专科    │ │
│  └──────────┘     └───────────┘     │ Agent     │ │
│                                      │ + 协调器   │ │
│                                      └─────┬─────┘ │
│                                            │       │
│                                      ┌─────▼─────┐ │
│                                      │ 评估结果   │ │
│                                      │ JSON 文件  │ │
│                                      └───────────┘ │
└──────────────────────────────────────────────────┘
```

**为什么这样设计**：
- 1-5分钟传一次 = 普通 HTTP 请求，**不需要 MQTT**（MQTT 是给毫秒级实时流用的）
- CSV 人类可读、Excel 能打开、pandas 直接读，**研究阶段完全够用**
- Claude Agent SDK 自带工具系统（读文件、执行代码），天然适合做数据分析后端

---

## 2. 认证与计费说明

**重要**：Claude Agent SDK 和 Anthropic Python SDK 都需要 **API Key**，不支持 Pro Max 订阅。

| 方式 | 认证 | 适用 |
|------|------|------|
| Claude 网页/桌面 | Pro Max 订阅 | 交互式对话 |
| Claude Code CLI | Pro Max 订阅 | 本地编程辅助 |
| `anthropic` Python SDK | API Key（按量付费） | 你当前代码用的 |
| `claude-agent-sdk` | API Key（按量付费） | 本方案推荐 |

```bash
# 获取 API Key: https://console.anthropic.com/
export ANTHROPIC_API_KEY=sk-ant-xxxxx
```

**费用估算**（claude-sonnet-4-20250514）：
- 每次 Agent 评估（7个Agent + 协调器综合）≈ 8 次 API 调用
- 每次调用 ≈ 2K input + 1K output tokens ≈ $0.012
- 每次完整评估 ≈ **$0.10**
- 每5分钟评估一次，每天 ≈ $28.80
- 每小时评估一次，每天 ≈ **$2.40**（推荐起步频率）

---

## 3. 数据格式：CSV

### 3.1 为什么 CSV 就够了

| 考虑 | 说明 |
|------|------|
| 数据频率 | 1-5分钟一条聚合特征，不是 50Hz 原始信号 |
| 数据量 | 每分钟1行 × 24小时 = 1440行/天/患者，CSV 毫无压力 |
| 可读性 | Excel/Numbers 直接打开，方便论文作图 |
| 兼容性 | pandas、R、MATLAB、任何工具都能读 |
| 追加写入 | CSV 天然支持 append，Parquet 不行 |

### 3.2 文件目录结构

```
data/
├── raw/                              # 手机上传的原始聚合数据
│   └── patient_001/
│       ├── imu_2026-03-17.csv
│       ├── ppg_2026-03-17.csv
│       ├── eda_2026-03-17.csv
│       └── audio_2026-03-17.csv
│
├── features/                         # 特征提取后（Agent消费这里）
│   └── patient_001/
│       └── multimodal_2026-03-17.csv  # 多模态融合特征，每行一个时间窗口
│
├── assessments/                      # Agent 评估结果
│   └── patient_001/
│       └── 2026-03-17.jsonl          # 每行一个JSON评估结果
│
├── patients/                         # 患者档案
│   └── patient_001.json
│
└── baselines/                        # 个人基线
    └── patient_001_baseline.json
```

### 3.3 CSV 格式定义

**IMU 特征 CSV**（`raw/patient_001/imu_2026-03-17.csv`）：
```csv
timestamp,gait_speed,cadence,stride_variability,hand_tremor_score,activity_level,quality
2026-03-17T08:00:00,1.15,108,3.2,1.5,0.65,0.95
2026-03-17T08:05:00,1.12,106,3.5,1.6,0.60,0.93
2026-03-17T08:10:00,0.0,0,0.0,0.8,0.10,0.90
```

**PPG 特征 CSV**（`raw/patient_001/ppg_2026-03-17.csv`）：
```csv
timestamp,heart_rate,spo2,sdnn,rmssd,lf_hf_ratio,pnn50,quality
2026-03-17T08:00:00,72.5,98.1,45.2,38.7,1.8,22.3,0.92
2026-03-17T08:05:00,74.1,97.8,42.0,35.2,2.1,19.8,0.94
```

**EDA 特征 CSV**（`raw/patient_001/eda_2026-03-17.csv`）：
```csv
timestamp,scl,scr_count,scr_amplitude,ns_scr_rate,quality
2026-03-17T08:00:00,2.5,3,0.45,0.12,0.88
2026-03-17T08:05:00,2.8,5,0.52,0.18,0.90
```

**Audio 特征 CSV**（`raw/patient_001/audio_2026-03-17.csv`）：
```csv
timestamp,f0_mean,jitter,shimmer,hnr,speech_rate,pause_rate,ttr,mlu,semantic_coherence,quality
2026-03-17T08:00:00,155.2,1.2,3.5,18.5,120,0.25,0.65,8.2,0.78,0.85
```

**多模态融合 CSV**（`features/patient_001/multimodal_2026-03-17.csv`）：
```csv
timestamp,gait_speed,cadence,stride_variability,hand_tremor_score,activity_level,heart_rate,spo2,sdnn,rmssd,lf_hf_ratio,pnn50,scl,scr_count,scr_amplitude,ns_scr_rate,f0_mean,jitter,shimmer,hnr,speech_rate,pause_rate,ttr,mlu,semantic_coherence,quality
2026-03-17T08:00:00,1.15,108,3.2,1.5,0.65,72.5,98.1,45.2,38.7,1.8,22.3,2.5,3,0.45,0.12,155.2,1.2,3.5,18.5,120,0.25,0.65,8.2,0.78,0.92
```

---

## 4. 数据上传接口：FastAPI

手机 App 每 1-5 分钟 POST 一次 JSON，服务端追加写入 CSV。

### 4.1 完整 FastAPI 服务

```python
# src/server.py

import csv
import json
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AD Sensor Data API")
DATA_ROOT = Path("data")


# ── 请求模型 ────────────────────────────────────

class IMUData(BaseModel):
    gait_speed: float
    cadence: float
    stride_variability: float
    hand_tremor_score: float
    activity_level: float

class PPGData(BaseModel):
    heart_rate: float
    spo2: float
    sdnn: float
    rmssd: float
    lf_hf_ratio: float
    pnn50: float

class EDAData(BaseModel):
    scl: float
    scr_count: int
    scr_amplitude: float
    ns_scr_rate: float

class AudioData(BaseModel):
    f0_mean: float
    jitter: float
    shimmer: float
    hnr: float
    speech_rate: float = 0.0
    pause_rate: float = 0.0
    ttr: float = 0.0
    mlu: float = 0.0
    semantic_coherence: float = 0.0

class SensorUpload(BaseModel):
    """手机端每1-5分钟上传一次"""
    patient_id: str
    timestamp: str                  # ISO格式 "2026-03-17T08:00:00"
    imu: IMUData | None = None
    ppg: PPGData | None = None
    eda: EDAData | None = None
    audio: AudioData | None = None
    quality: float = 1.0


# ── CSV 写入 ────────────────────────────────────

def append_csv(filepath: Path, row: dict):
    """追加一行到 CSV，文件不存在则自动创建表头"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    file_exists = filepath.exists()

    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# ── API 端点 ────────────────────────────────────

@app.post("/api/upload")
def upload_sensor_data(data: SensorUpload):
    """
    手机 App 调用此接口上传传感器特征。
    每1-5分钟调一次，数据追加写入当天的 CSV 文件。
    """
    date_str = data.timestamp[:10]  # "2026-03-17"
    patient_dir = DATA_ROOT / "raw" / data.patient_id

    # 分别写入各传感器 CSV
    if data.imu:
        row = {"timestamp": data.timestamp, **data.imu.model_dump(), "quality": data.quality}
        append_csv(patient_dir / f"imu_{date_str}.csv", row)

    if data.ppg:
        row = {"timestamp": data.timestamp, **data.ppg.model_dump(), "quality": data.quality}
        append_csv(patient_dir / f"ppg_{date_str}.csv", row)

    if data.eda:
        row = {"timestamp": data.timestamp, **data.eda.model_dump(), "quality": data.quality}
        append_csv(patient_dir / f"eda_{date_str}.csv", row)

    if data.audio:
        row = {"timestamp": data.timestamp, **data.audio.model_dump(), "quality": data.quality}
        append_csv(patient_dir / f"audio_{date_str}.csv", row)

    # 写入融合特征 CSV（Agent 消费这个）
    merged = {"timestamp": data.timestamp}
    for sensor in [data.imu, data.ppg, data.eda, data.audio]:
        if sensor:
            merged.update(sensor.model_dump())
    merged["quality"] = data.quality

    features_dir = DATA_ROOT / "features" / data.patient_id
    append_csv(features_dir / f"multimodal_{date_str}.csv", merged)

    return {"status": "ok", "timestamp": data.timestamp}


@app.get("/api/patients/{patient_id}/latest")
def get_latest_features(patient_id: str):
    """获取某患者最新一条特征（调试用）"""
    import pandas as pd

    today = datetime.now().strftime("%Y-%m-%d")
    path = DATA_ROOT / "features" / patient_id / f"multimodal_{today}.csv"
    if not path.exists():
        raise HTTPException(404, f"No data for {patient_id} today")

    df = pd.read_csv(path)
    return df.iloc[-1].to_dict()


@app.get("/api/patients/{patient_id}/history")
def get_feature_history(patient_id: str, days: int = 7):
    """获取历史特征（趋势分析用）"""
    import pandas as pd

    features_dir = DATA_ROOT / "features" / patient_id
    if not features_dir.exists():
        raise HTTPException(404, f"No data for {patient_id}")

    dfs = []
    for csv_file in sorted(features_dir.glob("multimodal_*.csv")):
        dfs.append(pd.read_csv(csv_file))

    if not dfs:
        raise HTTPException(404, "No feature files found")

    df = pd.concat(dfs, ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    cutoff = datetime.now() - pd.Timedelta(days=days)
    df = df[df["timestamp"] >= cutoff]
    return df.to_dict(orient="records")


@app.get("/api/patients/{patient_id}/assessments")
def get_assessments(patient_id: str, date: str | None = None):
    """获取 Agent 评估历史"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    path = DATA_ROOT / "assessments" / patient_id / f"{date}.jsonl"
    if not path.exists():
        return []

    results = []
    with open(path) as f:
        for line in f:
            results.append(json.loads(line))
    return results
```

### 4.2 手机端调用示例

```python
# 手机 App / 边缘设备 Python 脚本
import requests
import json

def upload_features(server_url, patient_id, imu, ppg, eda, audio=None):
    """每1-5分钟调一次"""
    payload = {
        "patient_id": patient_id,
        "timestamp": datetime.now().isoformat(),
        "imu": imu,    # dict: {"gait_speed": 1.15, "cadence": 108, ...}
        "ppg": ppg,     # dict: {"heart_rate": 72.5, "spo2": 98.1, ...}
        "eda": eda,     # dict: {"scl": 2.5, "scr_count": 3, ...}
        "audio": audio, # dict or None
        "quality": 0.95
    }
    resp = requests.post(f"{server_url}/api/upload", json=payload)
    return resp.json()

# 用法
upload_features(
    server_url="http://localhost:8000",
    patient_id="patient_001",
    imu={"gait_speed": 1.15, "cadence": 108, "stride_variability": 3.2,
         "hand_tremor_score": 1.5, "activity_level": 0.65},
    ppg={"heart_rate": 72.5, "spo2": 98.1, "sdnn": 45.2,
         "rmssd": 38.7, "lf_hf_ratio": 1.8, "pnn50": 22.3},
    eda={"scl": 2.5, "scr_count": 3, "scr_amplitude": 0.45, "ns_scr_rate": 0.12},
)
```

### 4.3 启动服务

```bash
pip install fastapi uvicorn pandas
uvicorn src.server:app --host 0.0.0.0 --port 8000

# 测试
curl -X POST http://localhost:8000/api/upload \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient_001",
    "timestamp": "2026-03-17T08:00:00",
    "imu": {"gait_speed": 1.15, "cadence": 108, "stride_variability": 3.2,
            "hand_tremor_score": 1.5, "activity_level": 0.65},
    "ppg": {"heart_rate": 72.5, "spo2": 98.1, "sdnn": 45.2,
            "rmssd": 38.7, "lf_hf_ratio": 1.8, "pnn50": 22.3},
    "eda": {"scl": 2.5, "scr_count": 3, "scr_amplitude": 0.45, "ns_scr_rate": 0.12}
  }'
```

---

## 5. Agent 后端：Claude Agent SDK

### 5.1 架构概念

Claude Agent SDK 的核心优势：**你定义 Tool，Agent 自主决定何时调用**。

```
你定义的 MCP Tools:
  - read_patient_csv    → 读取 CSV 传感器数据
  - read_patient_profile → 读取患者档案
  - read_baseline       → 读取个人基线
  - save_assessment     → 保存评估结果
  - send_alert          → 发送预警通知

Claude Agent SDK:
  - 自动调用上述 Tools 获取数据
  - 用 system prompt 定义 7 个专科 Agent 的角色
  - 协调器综合推理，输出最终决策
  - 结果通过 save_assessment Tool 持久化
```

### 5.2 自定义 MCP Tools（数据读取）

```python
# src/agent_tools.py

import json
import pandas as pd
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import tool, create_sdk_mcp_server

DATA_ROOT = Path("data")


@tool(
    "read_sensor_features",
    "读取某患者最近N条多模态传感器特征数据，返回 CSV 格式文本",
    {
        "patient_id": str,
        "n_rows": int,       # 读取最近几条，默认传 10
        "date": str,         # 可选，默认今天 "2026-03-17"
    }
)
async def read_sensor_features(args):
    patient_id = args["patient_id"]
    date = args.get("date", datetime.now().strftime("%Y-%m-%d"))
    n = args.get("n_rows", 10)

    path = DATA_ROOT / "features" / patient_id / f"multimodal_{date}.csv"
    if not path.exists():
        return {"content": [{"type": "text", "text": f"没有找到 {patient_id} 在 {date} 的数据"}]}

    df = pd.read_csv(path)
    latest = df.tail(n)
    return {"content": [{"type": "text", "text": latest.to_csv(index=False)}]}


@tool(
    "read_raw_sensor",
    "读取某患者某个传感器的原始特征CSV（imu/ppg/eda/audio）",
    {
        "patient_id": str,
        "sensor_type": str,  # "imu", "ppg", "eda", "audio"
        "date": str,
        "n_rows": int,
    }
)
async def read_raw_sensor(args):
    patient_id = args["patient_id"]
    sensor = args["sensor_type"]
    date = args.get("date", datetime.now().strftime("%Y-%m-%d"))
    n = args.get("n_rows", 20)

    path = DATA_ROOT / "raw" / patient_id / f"{sensor}_{date}.csv"
    if not path.exists():
        return {"content": [{"type": "text", "text": f"没有 {sensor} 数据: {path}"}]}

    df = pd.read_csv(path)
    latest = df.tail(n)
    return {"content": [{"type": "text", "text": latest.to_csv(index=False)}]}


@tool(
    "read_patient_profile",
    "读取患者档案（年龄、性别、诊断、用药等）",
    {"patient_id": str}
)
async def read_patient_profile(args):
    path = DATA_ROOT / "patients" / f"{args['patient_id']}.json"
    if not path.exists():
        return {"content": [{"type": "text", "text": "患者档案不存在"}]}

    with open(path) as f:
        profile = json.load(f)
    return {"content": [{"type": "text", "text": json.dumps(profile, ensure_ascii=False, indent=2)}]}


@tool(
    "read_baseline",
    "读取患者个人基线数据（28天均值/标准差）",
    {"patient_id": str}
)
async def read_baseline(args):
    path = DATA_ROOT / "baselines" / f"{args['patient_id']}_baseline.json"
    if not path.exists():
        return {"content": [{"type": "text", "text": "尚未建立基线"}]}

    with open(path) as f:
        baseline = json.load(f)
    return {"content": [{"type": "text", "text": json.dumps(baseline, ensure_ascii=False, indent=2)}]}


@tool(
    "read_assessment_history",
    "读取最近的 Agent 评估历史",
    {"patient_id": str, "n_records": int}
)
async def read_assessment_history(args):
    patient_id = args["patient_id"]
    n = args.get("n_records", 5)
    assess_dir = DATA_ROOT / "assessments" / patient_id

    if not assess_dir.exists():
        return {"content": [{"type": "text", "text": "无历史评估"}]}

    records = []
    for jsonl_file in sorted(assess_dir.glob("*.jsonl"), reverse=True):
        with open(jsonl_file) as f:
            for line in f:
                records.append(json.loads(line))
        if len(records) >= n:
            break

    records = records[:n]
    return {"content": [{"type": "text", "text": json.dumps(records, ensure_ascii=False, indent=2)}]}


@tool(
    "save_assessment",
    "保存本次 Agent 评估结果",
    {
        "patient_id": str,
        "assessment": str,   # JSON string
    }
)
async def save_assessment(args):
    patient_id = args["patient_id"]
    today = datetime.now().strftime("%Y-%m-%d")
    path = DATA_ROOT / "assessments" / patient_id / f"{today}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)

    record = json.loads(args["assessment"])
    record["saved_at"] = datetime.now().isoformat()

    with open(path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {"content": [{"type": "text", "text": f"评估结果已保存: {path}"}]}


@tool(
    "send_alert",
    "发送紧急预警通知（红色/黄色）给护理人员",
    {
        "patient_id": str,
        "alert_level": str,  # "yellow" or "red"
        "message": str,
    }
)
async def send_alert(args):
    # TODO: 对接实际通知渠道（微信/短信/邮件）
    # 目前仅写入日志文件
    path = DATA_ROOT / "alerts" / f"{args['patient_id']}_alerts.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "patient_id": args["patient_id"],
        "level": args["alert_level"],
        "message": args["message"],
    }
    with open(path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {"content": [{"type": "text", "text": f"预警已发送: [{args['alert_level']}] {args['message']}"}]}


# ── 注册所有 Tools 到一个 MCP Server ─────────────

sensor_mcp_server = create_sdk_mcp_server(
    name="ad-sensor-tools",
    version="1.0.0",
    tools=[
        read_sensor_features,
        read_raw_sensor,
        read_patient_profile,
        read_baseline,
        read_assessment_history,
        save_assessment,
        send_alert,
    ]
)
```

### 5.3 Agent 定义与运行

```python
# src/run_agent.py

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition
from src.agent_tools import sensor_mcp_server


# ── System Prompt（协调器角色）───────────────────

COORDINATOR_PROMPT = """你是 AD（阿尔茨海默病）多智能体监测系统的总协调器。

## 你的工作流程

每次被调用时，你需要：

1. 用 read_patient_profile 获取患者档案
2. 用 read_sensor_features 获取最新传感器数据
3. 用 read_baseline 获取个人基线（如有）
4. 用 read_assessment_history 获取近期评估（看趋势）
5. 从 7 个专科视角分别分析数据：
   - 运动认知（IMU）：步态、震颤、MCR 评估
   - 语言认知（Audio）：语速、词汇多样性、语义连贯性
   - 自主神经（PPG+EDA）：HRV、交感/副交感平衡
   - 情绪行为（多模态融合）：BPSD 检测、激越预测
   - 临床诊断：AD 分期、认知轨迹
   - 干预建议：非药物干预方案
   - 护理管理：报告生成、预警通知
6. 综合推理，输出最终评估
7. 用 save_assessment 保存结果
8. 如有红色/黄色预警，用 send_alert 通知

## 情境推理框架
- 同时考虑：传感器数据 + 时间（日落综合征多在16:00-18:00）+ 活动状态 + 用药情况
- HR↑ + EDA↑ + 步态稳 + 有访客 → 情绪激动（非病理）
- HR↑ + EDA↑ + 步态不稳 + 下午4:30 → 日落综合征可能
- 安全优先：任何维度出现异常都应提高预警等级

## 输出格式
用 save_assessment 保存 JSON，包含：
- final_stage: normal/scd/mci/mild_ad/moderate_ad/severe_ad
- bpsd_detected: [] 或 ["agitation", "sundowning", ...]
- alert_level: green/yellow/red
- confidence: 0.0-1.0
- reasoning_chain: 完整中文推理过程
- recommendations: ["建议1", "建议2"]
- agent_analyses: {各专科分析摘要}

全部用中文回答。"""


async def run_evaluation(patient_id: str):
    """对某患者执行一次完整评估"""
    prompt = f"请对患者 {patient_id} 执行完整的多智能体评估。读取最新传感器数据，从7个专科视角分析，输出综合诊断。"

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="claude-sonnet-4-20250514",
            system_prompt=COORDINATOR_PROMPT,
            mcp_servers={"ad-sensor-tools": sensor_mcp_server},
            allowed_tools=[
                "mcp__ad-sensor-tools__read_sensor_features",
                "mcp__ad-sensor-tools__read_raw_sensor",
                "mcp__ad-sensor-tools__read_patient_profile",
                "mcp__ad-sensor-tools__read_baseline",
                "mcp__ad-sensor-tools__read_assessment_history",
                "mcp__ad-sensor-tools__save_assessment",
                "mcp__ad-sensor-tools__send_alert",
            ],
            max_turns=20,
        )
    ):
        # 打印 Agent 的推理过程（调试用）
        if hasattr(message, "content"):
            print(message.content)


async def main():
    # 评估单个患者
    await run_evaluation("patient_001")

if __name__ == "__main__":
    asyncio.run(main())
```

### 5.4 定时调度（每N分钟自动评估）

```python
# src/scheduler.py

import asyncio
import schedule
import time
from src.run_agent import run_evaluation


MONITORED_PATIENTS = ["patient_001", "patient_002"]
EVAL_INTERVAL_MINUTES = 60  # 每小时评估一次（控制 API 成本）


def trigger_evaluation():
    """同步包装器，供 schedule 调用"""
    for patient_id in MONITORED_PATIENTS:
        print(f"[{time.strftime('%H:%M:%S')}] 开始评估 {patient_id}")
        asyncio.run(run_evaluation(patient_id))
        print(f"[{time.strftime('%H:%M:%S')}] 完成评估 {patient_id}")


def main():
    # 启动时立即评估一次
    trigger_evaluation()

    # 定时调度
    schedule.every(EVAL_INTERVAL_MINUTES).minutes.do(trigger_evaluation)

    print(f"调度器已启动，每 {EVAL_INTERVAL_MINUTES} 分钟评估一次")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
```

### 5.5 用子 Agent 实现多专科（可选进阶）

如果你想让 7 个专科 Agent 各自独立推理再汇总：

```python
# src/run_multi_agent.py

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition
from src.agent_tools import sensor_mcp_server

# 定义 7 个子 Agent
SUB_AGENTS = {
    "motor-cognitive-agent": AgentDefinition(
        description="运动认知专家：分析IMU数据，评估步态、震颤、MCR",
        prompt="你是神经运动学专家。分析IMU数据，评估步态速度、步频、变异性、手部震颤，判断是否存在MCR（运动认知风险综合征）。输出JSON评估。",
        tools=[
            "mcp__ad-sensor-tools__read_sensor_features",
            "mcp__ad-sensor-tools__read_raw_sensor",
            "mcp__ad-sensor-tools__read_patient_profile",
            "mcp__ad-sensor-tools__read_baseline",
        ],
    ),
    "language-cognitive-agent": AgentDefinition(
        description="语言认知专家：分析语音数据，评估语言功能退化",
        prompt="你是临床语言学专家。分析语音特征（基频、语速、停顿率、TTR、MLU、语义连贯性），判断语言认知功能状态。输出JSON评估。",
        tools=[
            "mcp__ad-sensor-tools__read_sensor_features",
            "mcp__ad-sensor-tools__read_patient_profile",
        ],
    ),
    "autonomic-agent": AgentDefinition(
        description="自主神经专家：分析PPG+EDA，评估自主神经功能",
        prompt="你是自主神经功能专家。分析PPG（心率、HRV、SpO2）和EDA（SCL、SCR）数据，评估交感/副交感平衡、昼夜节律、自主神经退化。输出JSON评估。",
        tools=[
            "mcp__ad-sensor-tools__read_sensor_features",
            "mcp__ad-sensor-tools__read_patient_profile",
        ],
    ),
    "emotion-behavior-agent": AgentDefinition(
        description="情绪行为专家：多模态融合检测BPSD",
        prompt="你是老年精神科专家。融合EDA+PPG+IMU+Audio数据，检测BPSD（激越、日落综合征、焦虑、淡漠等），预测1-2小时内激越风险。输出JSON评估。",
        tools=[
            "mcp__ad-sensor-tools__read_sensor_features",
            "mcp__ad-sensor-tools__read_patient_profile",
            "mcp__ad-sensor-tools__read_assessment_history",
        ],
    ),
    "clinical-diagnosis-agent": AgentDefinition(
        description="临床诊断专家：AD分期与认知轨迹评估",
        prompt="你是神经内科AD专家。综合所有传感器数据，参考GDS分期标准和Jack 2024 AT(N)框架，评估AD分期、CCI轨迹、6个月转化风险。输出JSON评估。",
        tools=[
            "mcp__ad-sensor-tools__read_sensor_features",
            "mcp__ad-sensor-tools__read_patient_profile",
            "mcp__ad-sensor-tools__read_baseline",
            "mcp__ad-sensor-tools__read_assessment_history",
        ],
    ),
    "intervention-agent": AgentDefinition(
        description="干预专家：推荐非药物干预方案",
        prompt="你是非药物干预专家。根据患者当前情绪状态、AD分期、个人偏好，推荐最合适的干预方式（音乐/呼吸引导/认知训练/怀旧疗法等）。输出JSON建议。",
        tools=[
            "mcp__ad-sensor-tools__read_patient_profile",
            "mcp__ad-sensor-tools__read_sensor_features",
        ],
    ),
    "care-management-agent": AgentDefinition(
        description="护理管理专家：生成报告和预警通知",
        prompt="你是老年护理管理专家。整合所有评估结果，生成分层报告（医生版/家属版），判断是否需要发送预警。输出JSON报告。",
        tools=[
            "mcp__ad-sensor-tools__read_patient_profile",
            "mcp__ad-sensor-tools__read_assessment_history",
            "mcp__ad-sensor-tools__save_assessment",
            "mcp__ad-sensor-tools__send_alert",
        ],
    ),
}


async def run_multi_agent_evaluation(patient_id: str):
    """多Agent协同评估"""
    prompt = f"""请对患者 {patient_id} 执行多专科协同评估：
1. 依次调用 7 个子Agent 获取各专科评估
2. 综合所有评估，应用情境消歧推理
3. 输出最终决策并保存"""

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="claude-sonnet-4-20250514",
            system_prompt=COORDINATOR_PROMPT,
            mcp_servers={"ad-sensor-tools": sensor_mcp_server},
            allowed_tools=[
                "Agent",  # 允许调用子Agent
                "mcp__ad-sensor-tools__save_assessment",
                "mcp__ad-sensor-tools__send_alert",
                "mcp__ad-sensor-tools__read_sensor_features",
                "mcp__ad-sensor-tools__read_patient_profile",
            ],
            agents=SUB_AGENTS,
            max_turns=30,
        )
    ):
        if hasattr(message, "content"):
            print(message.content)
```

---

## 6. 完整数据流（端到端）

```
时间线：每5分钟一个循环

00:00  手机 App 采集 5 分钟数据
       ├─ IMU 50Hz × 300s = 15,000 个采样点 → 提取步态特征（1行）
       ├─ PPG 64Hz × 300s = 19,200 个采样点 → 提取 HRV 特征（1行）
       ├─ EDA 4Hz × 300s = 1,200 个采样点 → 提取 EDA 特征（1行）
       └─ Audio（如有语音段）→ 提取语音特征（1行）

00:01  HTTP POST → FastAPI /api/upload
       → 追加写入 CSV 文件（4个传感器CSV + 1个融合CSV）

每小时  Scheduler 触发 Agent 评估
       → Claude Agent SDK 读取 CSV
       → 7 个专科视角分析
       → 综合推理
       → 保存评估结果到 JSONL
       → 如有异常 → send_alert
```

---

## 7. 患者档案格式

```json
// data/patients/patient_001.json
{
  "patient_id": "patient_001",
  "name": "张XX",
  "age": 75,
  "gender": "female",
  "education_years": 12,
  "diagnosed_stage": "mci",
  "medications": ["多奈哌齐 5mg/日"],
  "music_preferences": ["邓丽君", "京剧"],
  "dialect": "mandarin",
  "caregiver_contact": "家属手机号",
  "known_triggers": ["独处时间过长", "环境噪音"],
  "baseline_established": true
}
```

---

## 8. 启动命令汇总

```bash
# 1. 安装依赖
pip install fastapi uvicorn pandas claude-agent-sdk schedule

# 2. 设置 API Key
export ANTHROPIC_API_KEY=sk-ant-xxxxx

# 3. 创建数据目录
mkdir -p data/{raw,features,assessments,patients,baselines,alerts}

# 4. 创建患者档案
echo '{"patient_id":"patient_001","name":"张XX","age":75,...}' > data/patients/patient_001.json

# 5. 启动 FastAPI 数据接收服务
uvicorn src.server:app --host 0.0.0.0 --port 8000 &

# 6. 启动 Agent 定时评估
python -m src.scheduler
```

---



## 9. 什么时候该升级

当以下任一情况出现时，再考虑从 CSV 升级：

| 信号 | 升级到 |
|------|--------|
| 患者数 > 50，CSV 文件管理混乱 | SQLite（单文件数据库） |
| 需要复杂 SQL 查询（JOIN、聚合） | SQLite 或 PostgreSQL |
| 原始 50Hz 数据也要存（非特征） | Parquet（列式压缩存大文件） |
| 多台服务器需要同时读写 | PostgreSQL / TimescaleDB |
| 需要毫秒级实时告警（跌倒检测等） | MQTT + 流处理 |

---

## 10. 依赖清单（精简版）

```txt
# 必需
fastapi           # 数据接收 API
uvicorn           # ASGI 服务器
pandas            # CSV 读写
claude-agent-sdk  # Agent 后端
schedule          # 定时调度

# 数据处理（特征提取时需要，手机端或服务端）
numpy
scipy             # 信号处理
neurokit2         # 生理信号（PPG HRV、EDA 分解）
librosa           # 音频特征

# 可选
requests          # 手机端上传用
```
