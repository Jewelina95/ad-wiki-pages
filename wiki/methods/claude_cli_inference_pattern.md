---
title: claude cli inference pattern
type: method
last_updated: 2026-04-25
status: settled
---

# AD 传感器数据方案（Claude Pro Max 版）

> **零 API 费用**。用 `claude -p` 命令行调 Claude，走 Pro Max 订阅。CSV 存数据，FastAPI 收数据。



## 2. 整体架构

```
┌──────────────────┐
│  可穿戴设备        │  IMU / PPG / EDA / Mic
└────────┬─────────┘
         │ BLE
         ▼
┌──────────────────┐
│  手机 App          │  边缘预处理 → 特征提取
└────────┬─────────┘
         │ HTTP POST（每1-5分钟）
         ▼
┌──────────────────────────────────────────────┐
│  你的电脑 / 服务器                               │
│                                                │
│  ┌──────────┐    ┌─────────┐    ┌───────────┐ │
│  │ FastAPI   │───▶│ CSV 文件 │───▶│ claude -p │ │
│  │ 收数据    │    │ 追加写入  │    │ 读CSV分析  │ │
│  └──────────┘    └─────────┘    │ 7专科评估  │ │
│                                  └─────┬─────┘ │
│                                        ▼       │
│                                  评估结果.jsonl  │
└──────────────────────────────────────────────┘
```

---

## 3. 数据存储：CSV（和之前一样）

```
data/
├── raw/                          # 手机上传的传感器特征
│   └── patient_001/
│       ├── imu_2026-03-17.csv
│       ├── ppg_2026-03-17.csv
│       ├── eda_2026-03-17.csv
│       └── audio_2026-03-17.csv
├── features/                     # 多模态融合（Agent 读这个）
│   └── patient_001/
│       └── multimodal_2026-03-17.csv
├── assessments/                  # Agent 评估结果
│   └── patient_001/
│       └── 2026-03-17.jsonl
├── patients/                     # 患者档案
│   └── patient_001.json
└── baselines/                    # 个人基线
    └── patient_001_baseline.json
```

CSV 格式和之前文档完全一致，不赘述。

---

## 4. 数据接收：FastAPI（和之前一样）

```python
# src/server.py — 完全复用之前方案，不需要改
# 手机 POST JSON → 追加写入 CSV
# 详见 数据接口与存储方案.md 第4节
```

启动：
```bash
pip install fastapi uvicorn pandas
uvicorn src.server:app --host 0.0.0.0 --port 8000
```

---

## 5. Agent 后端：用 `claude -p` 替代 SDK

### 5.1 核心封装：调用 Claude CLI

```python
# src/claude_cli.py

import subprocess
import json


def claude_query(
    prompt: str,
    system_prompt: str = "",
    model: str = "sonnet",
    output_format: str = "json",
    allowed_tools: list[str] | None = None,
    add_dirs: list[str] | None = None,
    max_turns: int = 10,
) -> dict | str:
    """
    调用 claude -p，走 Pro Max 订阅，零 API 费用。

    参数:
        prompt: 用户 prompt
        system_prompt: 系统 prompt（定义 Agent 角色）
        model: "sonnet" / "opus" / "haiku"
        output_format: "json" 返回结构化结果, "text" 返回纯文本
        allowed_tools: 允许的工具列表，如 ["Read", "Bash", "Grep"]
        add_dirs: 额外允许访问的目录
        max_turns: 最大工具调用轮数
    """
    cmd = [
        "claude",
        "-p", prompt,
        "--model", model,
        "--output-format", output_format,
        "--permission-mode", "bypassPermissions",  # 无人值守模式
        "--no-session-persistence",                 # 不保存会话（省磁盘）
        "--max-turns", str(max_turns),
    ]

    if system_prompt:
        cmd.extend(["--system-prompt", system_prompt])

    if allowed_tools:
        cmd.extend(["--allowed-tools", ",".join(allowed_tools)])

    if add_dirs:
        for d in add_dirs:
            cmd.extend(["--add-dir", d])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,  # 5分钟超时
    )

    if result.returncode != 0:
        raise RuntimeError(f"claude CLI 错误: {result.stderr}")

    if output_format == "json":
        parsed = json.loads(result.stdout)
        # json 模式返回 {"result": "...", "cost_usd": ..., ...}
        return parsed
    return result.stdout
```

### 5.2 单 Agent 评估（简单版，推荐先用这个）

把 7 个专科视角写进一个大 prompt，一次 CLI 调用搞定：

```python
# src/evaluator.py

import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from src.claude_cli import claude_query

DATA_ROOT = Path("data")


def load_context(patient_id: str) -> str:
    """把 CSV 数据 + 患者档案组装成 prompt 文本"""

    today = datetime.now().strftime("%Y-%m-%d")

    # 1. 患者档案
    profile_path = DATA_ROOT / "patients" / f"{patient_id}.json"
    profile = json.loads(profile_path.read_text()) if profile_path.exists() else {}

    # 2. 最新传感器特征（最近 12 条 = 最近 1 小时，每 5 分钟 1 条）
    features_path = DATA_ROOT / "features" / patient_id / f"multimodal_{today}.csv"
    if features_path.exists():
        df = pd.read_csv(features_path)
        recent = df.tail(12).to_csv(index=False)
    else:
        recent = "今日暂无数据"

    # 3. 基线
    baseline_path = DATA_ROOT / "baselines" / f"{patient_id}_baseline.json"
    baseline = json.loads(baseline_path.read_text()) if baseline_path.exists() else {}

    # 4. 近期评估历史
    assess_dir = DATA_ROOT / "assessments" / patient_id
    history_lines = []
    if assess_dir.exists():
        for f in sorted(assess_dir.glob("*.jsonl"), reverse=True)[:3]:
            for line in open(f):
                history_lines.append(line.strip())
            if len(history_lines) >= 5:
                break
    history = history_lines[:5]

    # 组装
    return f"""## 患者档案
```json
{json.dumps(profile, ensure_ascii=False, indent=2)}
```

## 最近传感器数据（CSV，每行=一个5分钟窗口）
```csv
{recent}
```

## 个人基线（28天均值±标准差）
```json
{json.dumps(baseline, ensure_ascii=False, indent=2) if baseline else "尚未建立基线"}
```

## 近期评估历史
{chr(10).join(history) if history else "无历史评估"}
"""


SYSTEM_PROMPT = """你是 AD（阿尔茨海默病）多智能体监测系统。

收到患者数据后，你需要从以下 7 个专科视角逐一分析，最后综合输出。

## 7 个专科视角

### 1. 运动认知（IMU 数据）
- 步态速度、步频、步态变异性 → 是否存在 MCR（运动认知风险综合征）
- 手部震颤评分 → 帕金森鉴别
- 活动量 → 淡漠评估
- 参考：步速 <0.8m/s + 主观认知下降 = MCR 阳性

### 2. 语言认知（Audio 数据）
- 语速下降、停顿增多 → 词汇检索困难
- TTR（类型标记比）下降 → 词汇多样性降低
- 语义连贯性 → 执行功能/语义记忆
- 基频、Jitter、Shimmer → 声带运动控制

### 3. 自主神经（PPG + EDA 数据）
- HRV（SDNN, RMSSD, LF/HF）→ 交感/副交感平衡
- SpO2 → 缺氧状态
- SCL/SCR → 情绪唤醒水平、焦虑
- 昼夜节律（趋势数据）

### 4. 情绪行为（多模态融合）
- EDA↑ + HR↑ + 活动↑ → 激越
- EDA↓ + HR 平稳 + 活动↓ → 淡漠
- 下午4-6点异常 → 日落综合征
- 检测 BPSD：激越、抑郁、焦虑、淡漠、游荡、幻觉、日落综合征

### 5. 临床诊断
- 综合所有传感器 → GDS 分期（1-7）
- 参考 Jack 2024 AT(N) 框架
- CCI（复合认知指数）趋势：稳定/下降/快速下降
- 6 个月转化风险评估

### 6. 干预建议
- 根据情绪状态 + AD 分期 + 患者偏好 → 推荐非药物干预
- 可选：音乐疗法、呼吸引导、认知训练、怀旧疗法、安全提示

### 7. 护理管理
- 预警等级判断（green/yellow/red）
- 如需预警，给出具体通知内容

## 情境消歧规则
- HR↑ + EDA↑ + 步态稳 + 有访客 → 情绪激动（非病理）
- HR↑ + EDA↑ + 步态不稳 + 16:00-18:00 → 日落综合征
- HR↑ + EDA↓ + 活动增加 → 运动性心率升高（正常）
- 安全优先：任何一个维度严重异常 → 预警不低于 yellow

## 输出要求
必须输出以下 JSON（中文推理）：
```json
{
  "agent_analyses": {
    "motor_cognitive": "运动认知分析摘要",
    "language_cognitive": "语言认知分析摘要",
    "autonomic": "自主神经分析摘要",
    "emotion_behavior": "情绪行为分析摘要",
    "clinical_diagnosis": "临床诊断摘要",
    "intervention": "干预建议",
    "care_management": "护理管理摘要"
  },
  "final_stage": "normal/scd/mci/mild_ad/moderate_ad/severe_ad",
  "bpsd_detected": [],
  "alert_level": "green/yellow/red",
  "confidence": 0.0,
  "reasoning_chain": "完整推理过程",
  "recommendations": ["建议1", "建议2"],
  "alert_message": "如需预警，填写通知内容；无预警填 null"
}
```"""


def evaluate_patient(patient_id: str) -> dict:
    """对某患者执行一次完整评估"""

    context = load_context(patient_id)
    prompt = f"请对以下患者执行完整的 7 专科评估：\n\n{context}"

    response = claude_query(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        model="sonnet",         # Pro Max 可用 "opus" 更强
        output_format="json",
        max_turns=3,            # 纯推理不需要多轮工具调用
    )

    # 从 CLI 返回中提取结果
    result_text = response.get("result", "")

    # 解析 JSON
    try:
        if "```json" in result_text:
            json_str = result_text.split("```json")[1].split("```")[0].strip()
        else:
            json_str = result_text.strip()
        assessment = json.loads(json_str)
    except (json.JSONDecodeError, IndexError):
        assessment = {
            "error": "解析失败",
            "raw_response": result_text[:1000],
            "alert_level": "yellow",
        }

    # 保存结果
    assessment["timestamp"] = datetime.now().isoformat()
    assessment["patient_id"] = patient_id

    today = datetime.now().strftime("%Y-%m-%d")
    save_path = DATA_ROOT / "assessments" / patient_id / f"{today}.jsonl"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "a") as f:
        f.write(json.dumps(assessment, ensure_ascii=False) + "\n")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] {patient_id}: "
          f"stage={assessment.get('final_stage')}, "
          f"alert={assessment.get('alert_level')}, "
          f"confidence={assessment.get('confidence')}")

    return assessment
```

### 5.3 高级版：让 Claude 自己读文件

如果你希望 Claude 自己用 Read 工具直接读 CSV（而不是你拼到 prompt 里），也可以：

```python
def evaluate_patient_with_tools(patient_id: str) -> dict:
    """让 Claude 自己读文件，适合数据量大时"""

    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""请对患者 {patient_id} 执行完整的 7 专科评估。

数据位置：
- 患者档案：data/patients/{patient_id}.json
- 今日传感器特征：data/features/{patient_id}/multimodal_{today}.csv
- 个人基线：data/baselines/{patient_id}_baseline.json
- 评估历史：data/assessments/{patient_id}/ 目录下的 .jsonl 文件

请：
1. 用 Read 工具读取上述文件
2. 从 7 个专科视角分析
3. 输出 JSON 格式评估结果
4. 将结果追加写入 data/assessments/{patient_id}/{today}.jsonl"""

    response = claude_query(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        model="sonnet",
        output_format="json",
        allowed_tools=["Read", "Glob", "Write"],  # 只允许读写文件
        add_dirs=["data"],                          # 允许访问 data 目录
        max_turns=15,
    )
    return response
```

先不看 先要从1个agent 开始跑
### 5.4 多 Agent 版：每个专科独立调用

如果你想要 7 个 Agent 各自独立推理（更像真正的多智能体），可以并行调用 7 次 CLI：

```python
# src/multi_agent_evaluator.py

import json
import concurrent.futures
from datetime import datetime
from pathlib import Path
from src.claude_cli import claude_query
from src.evaluator import load_context, DATA_ROOT


# 每个子 Agent 的 system prompt（精简版，完整版自行扩充）
SUB_AGENT_PROMPTS = {
    "motor_cognitive": "你是神经运动学专家。只分析 IMU 相关数据（gait_speed, cadence, stride_variability, hand_tremor_score, activity_level）。评估步态、震颤、MCR风险。输出JSON: {findings, confidence, alert_level, reasoning}",

    "language_cognitive": "你是临床语言学专家。只分析语音相关数据（f0_mean, jitter, shimmer, hnr, speech_rate, pause_rate, ttr, mlu, semantic_coherence）。评估语言认知功能。输出JSON: {findings, confidence, alert_level, reasoning}",

    "autonomic": "你是自主神经功能专家。只分析 PPG+EDA 数据（heart_rate, spo2, sdnn, rmssd, lf_hf_ratio, pnn50, scl, scr_count, scr_amplitude, ns_scr_rate）。评估自主神经功能和昼夜节律。输出JSON: {findings, confidence, alert_level, reasoning}",

    "emotion_behavior": "你是老年精神科专家。融合所有传感器数据，检测 BPSD（激越、日落综合征、焦虑、淡漠等）。预测1-2小时内激越风险。输出JSON: {findings, bpsd_detected, confidence, alert_level, reasoning}",

    "clinical_diagnosis": "你是神经内科AD专家。综合所有传感器数据，参考GDS分期和Jack 2024 AT(N)框架，评估AD分期和CCI轨迹。输出JSON: {stage, gds_score, cci_trend, conversion_risk_6m, confidence, reasoning}",

    "intervention": "你是非药物干预专家。根据患者情绪状态和AD分期，推荐干预方案（音乐/呼吸/认知训练/怀旧疗法）。输出JSON: {intervention_type, specific_plan, reasoning}",

    "care_management": "你是老年护理管理专家。综合所有信息，判断预警等级，决定是否需要通知护理人员。输出JSON: {alert_level, alert_message, report_summary}",
}


def run_sub_agent(agent_name: str, system_prompt: str, context: str) -> dict:
    """运行单个子 Agent"""
    prompt = f"请从你的专科视角分析以下患者数据：\n\n{context}"

    response = claude_query(
        prompt=prompt,
        system_prompt=system_prompt,
        model="sonnet",
        output_format="json",
        max_turns=3,
    )

    result_text = response.get("result", "")
    try:
        if "```json" in result_text:
            json_str = result_text.split("```json")[1].split("```")[0].strip()
        else:
            json_str = result_text.strip()
        return {"agent": agent_name, "assessment": json.loads(json_str)}
    except (json.JSONDecodeError, IndexError):
        return {"agent": agent_name, "assessment": {"error": result_text[:500]}}


def evaluate_patient_multi_agent(patient_id: str) -> dict:
    """7 个子 Agent 并行评估，然后协调器综合"""

    context = load_context(patient_id)

    # ── Step 1: 并行跑 7 个子 Agent ────────────
    agent_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        futures = {
            executor.submit(run_sub_agent, name, prompt, context): name
            for name, prompt in SUB_AGENT_PROMPTS.items()
        }
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                result = future.result(timeout=120)
                agent_results[name] = result["assessment"]
            except Exception as e:
                agent_results[name] = {"error": str(e)}

    # ── Step 2: 协调器综合推理 ────────────
    coordinator_prompt = f"""以下是 7 个专科 Agent 对患者 {patient_id} 的独立评估结果：

```json
{json.dumps(agent_results, ensure_ascii=False, indent=2)}
```

患者原始数据：
{context}

请综合所有评估，解决冲突，输出最终决策 JSON：
{{
  "final_stage": "...",
  "bpsd_detected": [],
  "alert_level": "green/yellow/red",
  "confidence": 0.0-1.0,
  "reasoning_chain": "综合推理过程",
  "recommendations": [],
  "agent_analyses": {{各Agent摘要}}
}}"""

    coordinator_system = """你是多智能体系统的总协调器。
冲突仲裁规则：
- 安全优先：任何 Agent 发出红色预警 → 整体不低于 yellow
- 优先信任与当前情境最相关的 Agent
- 不确定时降低置信度，建议增加监测频率"""

    response = claude_query(
        prompt=coordinator_prompt,
        system_prompt=coordinator_system,
        model="opus",  # 协调器用更强的模型
        output_format="json",
        max_turns=3,
    )

    result_text = response.get("result", "")
    try:
        if "```json" in result_text:
            json_str = result_text.split("```json")[1].split("```")[0].strip()
        else:
            json_str = result_text.strip()
        final = json.loads(json_str)
    except (json.JSONDecodeError, IndexError):
        final = {"error": "协调器解析失败", "raw": result_text[:1000]}

    # 保存
    final["timestamp"] = datetime.now().isoformat()
    final["patient_id"] = patient_id
    final["sub_agent_results"] = agent_results

    today = datetime.now().strftime("%Y-%m-%d")
    save_path = DATA_ROOT / "assessments" / patient_id / f"{today}.jsonl"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "a") as f:
        f.write(json.dumps(final, ensure_ascii=False) + "\n")

    return final
```

---

## 6. 定时调度

```python
# src/scheduler.py

import schedule
import time
from src.evaluator import evaluate_patient
# 或者用多Agent版：
# from src.multi_agent_evaluator import evaluate_patient_multi_agent as evaluate_patient

PATIENTS = ["patient_001"]
INTERVAL_MINUTES = 60


def run_all():
    for pid in PATIENTS:
        try:
            evaluate_patient(pid)
        except Exception as e:
            print(f"评估 {pid} 失败: {e}")


if __name__ == "__main__":
    run_all()  # 启动时跑一次
    schedule.every(INTERVAL_MINUTES).minutes.do(run_all)

    print(f"已启动，每 {INTERVAL_MINUTES} 分钟评估一次")
    print(f"监测患者: {PATIENTS}")
    while True:
        schedule.run_pending()
        time.sleep(1)
```

---

## 7. 完整启动流程

```bash
# 1. 确保 claude CLI 已登录 Pro Max
claude --version
# 如果没登录: claude 然后按提示登录

# 2. 安装 Python 依赖
pip install fastapi uvicorn pandas schedule

# 3. 创建数据目录 + 示例患者
mkdir -p data/{raw/patient_001,features/patient_001,assessments/patient_001,patients,baselines,alerts}

cat > data/patients/patient_001.json << 'EOF'
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
  "known_triggers": ["独处时间过长"]
}
EOF

# 4. 启动 FastAPI（收手机数据）
uvicorn src.server:app --host 0.0.0.0 --port 8000 &

# 5. 模拟上传一条测试数据
curl -X POST http://localhost:8000/api/upload \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient_001",
    "timestamp": "2026-03-17T08:00:00",
    "imu": {"gait_speed": 1.15, "cadence": 108, "stride_variability": 3.2,
            "hand_tremor_score": 1.5, "activity_level": 0.65},
    "ppg": {"heart_rate": 72.5, "spo2": 98.1, "sdnn": 45.2,
            "rmssd": 38.7, "lf_hf_ratio": 1.8, "pnn50": 22.3},
    "eda": {"scl": 2.5, "scr_count": 3, "scr_amplitude": 0.45,
            "ns_scr_rate": 0.12}
  }'

# 6. 手动测试一次评估
python -c "from src.evaluator import evaluate_patient; evaluate_patient('patient_001')"

# 7. 启动定时调度
python -m src.scheduler
```

---

## 8. 两种评估模式对比

| | 单次调用（推荐起步） | 多Agent并行 |
|--|-------------------|------------|
| CLI 调用次数 | **1 次** | 7（子Agent）+ 1（协调器）= **8 次** |
| 耗时 | ~30-60秒 | ~30-60秒（并行）+ ~30秒（协调）|
| Pro Max 消耗 | 较少 | 较多（8倍 token） |
| 推理深度 | 单次推理，7个视角写在一起 | 各专科独立深度分析 |
| 推荐场景 | 日常监测、研究开发 | 需要详细分专科报告时 |

**建议**：先用单次调用版跑通流程，确认数据链路没问题后，再切换到多 Agent 版。

---

## 9. 注意事项

### Pro Max 限流
- Pro Max 有每日使用限额（不是无限的），大量评估可能触发限流
- 如果每小时评估 1 个患者，每天 24 次 CLI 调用，一般不会触发
- 如果多 Agent 模式（每次 8 调用），每天 192 次，可能接近限额
- 遇到限流时 `claude -p` 会返回错误，代码中已有异常处理

### `--permission-mode bypassPermissions`
- 这个标志让 Claude 跳过所有权限确认（读文件、写文件）
- **只在你信任的目录下使用**，不要在 home 目录根下跑
- 替代方案：用 `--allowed-tools "Read,Grep"` 限制只允许读操作

### 模型选择
- `--model sonnet`：快、便宜（Pro Max 额度消耗少），日常监测够用
- `--model opus`：更强推理能力，用于协调器综合判断或复杂案例
- `--model haiku`：最快最省，用于简单的异常检测预筛

---

## 10. 依赖清单

```txt
# Python 包
fastapi
uvicorn
pandas
schedule

# 系统要求
claude          # Claude Code CLI，已登录 Pro Max
python >= 3.10
```

和 API Key 方案相比，**不需要** `claude-agent-sdk` 和 `anthropic` 包。
