---
title: related work positioning
type: synthesis
last_updated: 2026-04-25
status: settled
---

**CHI 2026 论文调研报告**

*主题：可穿戴健康感知 × 专家知识增强 LLM × AD（阿尔茨海默）项目借鉴*

生成日期：2026-04-22 \| 会议时间：2026年4月13--17日 @ Barcelona CCIB

**一、报告说明与检索策略**

本报告基于 CHI 2026 官方完整程序数据（2780 条内容，含 Papers / Posters /
Workshops / Demos / SRC / Panels / Meet-Ups），针对你 AD
项目的三条主线系统检索：

-   **(A)** 可穿戴 / 传感器健康监测，尤其面向老年、认知相关人群（ESP32
    音频采集、多模态传感融合）

-   **(B)** LLM + 专家 / 临床 / 领域知识（RAG、知识图谱、临床
    agent、clinician-in-the-loop）

-   **(C)** 多模态 LLM × 健康，尤其 speech / voice
    biomarker、conversational care agent

共命中 363 条候选；本报告精选出最能直接服务你 AD 项目（专家知识库 +
传感器 Agent + 早期筛查）的约 26 篇 + 6 个
Workshop/Meetup。每条均标注「与 AD 项目关联」，便于直接对接 docs/
下已有的 SensorDataFactory 与 AD 专家知识库两套设计方案。

**二、痴呆 / 认知障碍 / 老龄直接相关（AD 最核心）**

*这组论文与 AD 病程、筛查、照护、干预直接同域。对你「早期筛查 +
居家传感 + 专家知识增强」的路线具有最高复用价值。*

**\[Paper\] Challenges in Automatic Speech Recognition for Adults with
Cognitive Impairment**

*作者: Michelle Cohn, Alyssa Lanzi, Yui Ishihara et al.*

*会场: （时间/会场待官方公布）*

*DOI: https://doi.org/10.1145/3772318.3791581*

**摘要:** 系统评估 ADRD（阿尔茨海默及相关痴呆）患者的 ASR 性能：在 83
位不同认知水平老年人上测量语音识别错误率，分离出导致 ASR
降级的具体声学因素。证实语音助手在 ADRD 用户上仍显著劣化。

**与AD项目关联:** 直接对应你 ESP32 音频采集 + 语音分析路线。AD 人群 ASR
失效模式（发音速率、停顿、模糊辅音）正是 SensorDataFactory
的「真实传感器数据分析」需要建模的偏差源；可作为 AD 语音预处理管道的
baseline 与 error-mode 参考。

**\[Paper\] Tracking Together: Robot-and-App-Based Speech Analysis
System for Dementia Care Partners**

*作者: 8 PLWD + 9 care partners 参与式研究*

*会场: Time & Personhood \| Fri Apr 17 11:00*

*DOI: https://doi.org/10.1145/3772318.3790450*

**摘要:** 为痴呆患者（PLWD）与照护伙伴设计的语音分析系统：robot + app
持续记录与分析会话，让 care partner 共同参与 meaning-making。

**与AD项目关联:** 与你 AD 项目「专家知识 +
真实对话分析」最接近。完整「语音 → 症状维度 → 照护决策」链路，可直接对标
SensorDataFactory 的 Agent 接口与 clinical knowledge 层。

**\[Paper\] Rememo: AI-in-the-loop Therapist Tool for Dementia
Reminiscence**

*作者: Research-through-Design 团队*

*会场: Bodies, Care & More Than Human Places \| Wed Apr 15 13:15*

*DOI: https://doi.org/10.1145/3772318.3790461*

**摘要:** 回忆疗法（RT）的 AI-in-the-loop
工具：不替代人类治疗师，而是强化其 facilitation
能力，保留关系性临床价值。

**与AD项目关联:** 直接呼应你「AD 专家知识库」定位------augment
而非替代临床专家。其「人类专家 + GenAI 支架」模式可作为
expert-knowledge-in-the-loop LLM 的交互蓝本。

**\[Paper\] Calls of Care: Materializing Posthuman Personhood with
Conversational Agents in Dementia Care**

*作者: 4 位 PLWD，6 个月参与式设计*

*会场: Time & Personhood \| Fri Apr 17 11:00*

*DOI: https://doi.org/10.1145/3772318.3790306*

**摘要:** 在痴呆照护中部署对话 agent，将「以人为本」扩展到「后人类
personhood」------强调非人类对象在照护 assemblage 中的角色。

**与AD项目关联:** 当 LLM Agent 进入 AD 居家环境时，本文提供了伦理 / 人格
/ 关系层面的设计语言，可嵌入 ethical approvel 文件夹的叙事。

**\[Paper\] Shared Stories, Shared Bonds: People with Dementia Exploring
Generative AI Together**

*作者: 17 PwD × 6 workshops*

*会场: Memory and Interaction \| Fri Apr 17 13:15*

*DOI: https://doi.org/10.1145/3772318.3791055*

**摘要:** 17 位痴呆患者共同体验 Copilot / Midjourney / Suno 三种
GenAI，研究社会连结感。GenAI 可作为 reminiscence
催化剂，但需管理幻觉与情绪波动。

**与AD项目关联:** 提示 AD-LLM Agent 须配置「幻觉 +
情绪」风险护栏，尤其知识库缺失时的 fallback 策略。

**\[Paper\] Temporal Snapshots: Probing and Designing for Subjective
Time in Dementia**

*作者: 12 位 design probe 参与者*

*会场: Time & Personhood \| Fri Apr 17 11:00*

*DOI: https://doi.org/10.1145/3772318.3790347*

**摘要:**
痴呆患者的时间体验异于常人，设计仍沿用规范化时钟/日程是限制。用 Temporal
Snapshots probe 探索主观时间，挑战规范化时间设计。

**与AD项目关联:** 你 AD 早期筛查若涉及时间感知任务（MMSE
定向题），这篇提供非规范化时间交互设计空间，指导 Agent 响应节律。

**\[Paper\] Defining Reality in Dementia VR: Stakeholder Perspectives on
Ecological Validity**

*作者: PwD + caregivers + therapists 访谈*

*会场: Aging and Later Life \| Wed Apr 15 11:00*

*DOI: https://doi.org/10.1145/3772318.3791489*

**摘要:** VR 在痴呆照护中多用于娱乐，少用于日常活动训练。三方访谈提炼
ecological validity 定义。

**与AD项目关联:**
若扩展到沉浸式任务训练，本文给出「真实感」评估维度表，可写进专家知识库的「任务保真度」规约。

**\[Paper\] Looking Beyond the Screen: Technology Use of Older People
Experiencing Cognitive Concerns**

*作者: 10 位有认知担忧的老年人*

*会场: Care and Lived Practices \| Wed Apr 15 11:00*

*DOI: https://doi.org/10.1145/3772318.3790526*

**摘要:**
一周视频会议使用调查：软硬件之外的物件（便签、旁人协助）对认知关注老年人的技术使用至关重要。

**与AD项目关联:** 提示 AD
居家部署必须把「非数字协作资源」建模进传感数据语义------只看屏幕信号会严重欠拟合。

**\[Poster\] Measuring Propensity for Dementia-Related Stigma in Large
Language Models**

*作者: GPT-5 / GPT-5 mini / GPT-5 nano*

*会场: Posters (Monday) \| Mon Apr 13 20:00*

*DOI: https://doi.org/10.1145/3772363.3798383*

**摘要:** 系统评估三个 LLM 在痴呆 stigma
维度上的倾向，与人类基准对比；测试 identity 设定是否放大/缓解 stigma。

**与AD项目关联:** 直接提示：AD 专家知识库注入 LLM 前必做 stigma
评测。可作为知识库上线前的标准化审查环节。

**\[Poster\] Collaborative AI Scaffolding for Structured Drawing in
Dementia Care**

*作者: Hui-Lien Huang, I-Ping Chen*

*会场: Posters (Wednesday) \| Wed Apr 15 18:30*

*DOI: https://doi.org/10.1145/3772363.3798912*

**摘要:** 平板绘画工具 + 视觉-语言模型（VLM）+ 本地
TTS，为痴呆老人提供结构化创作的微提示支架（HITL facilitator）。

**与AD项目关联:** VLM + 本地 TTS + 微提示技术栈与 esp32-audio-ai-main
边缘语音生成可直接对接，是非药物干预原型的最小可行参考。

**\[Poster\] Talking to Heirlooms: Conversational Agents Embodied in
Familiar Objects for Dementia**

*作者: heirloom table 对话 agent*

*会场: Posters (Thursday) \| Thu Apr 16 18:30*

*DOI: https://doi.org/10.1145/3772363.3798993*

**摘要:** 将对话 agent 嵌入熟悉的非人形家居物件（传家桌），降低
self-disclosure 阻力，支持深度回忆与生命回顾。

**与AD项目关联:** 与 ESP32 分散式音频节点思路天然契合------把 LLM Agent
藏进日常物件而非显眼设备，降低 AD 用户抗拒。

**\[Poster\] Finding MeBo: LLM-Based Voice User Interfaces for
Reminiscence Therapy**

*作者: Manasi Vaidya, Ryan Bruggeman, Jessie Chin et al.*

*会场: Posters (Thursday) \| Thu Apr 16 16:15*

*DOI: https://doi.org/10.1145/3772363.3798825*

**摘要:** 与 11 位老年人参与式共创 LLM 语音系统 Memory
Box。老年人将其视为「有情感存在的关系体」而非工具，强调 attentiveness /
emotional safety。

**与AD项目关联:** 给出 LLM 语音 agent
在老年用户上的「关系性」评估维度------AD 用户访谈与 ethical approval
章节可直接借鉴。

**\[SRC\] Homy: A Wayfinding Device That Supports Environmental
Connection for People With Dementia**

*作者: Student Research Competition*

*会场: SRC Posters \| Tue Apr 14 18:30*

*DOI: https://doi.org/10.1145/3772363.3799181*

**摘要:** 语音引导的户外寻路设备，兼顾 wayfinding
与将注意力引向周围自然环境，激发反思与情绪。

**与AD项目关联:** 若扩展到「户外 AD 辅助」，Homy 是形态参考；也可启发把
ESP32 音频节点挂到便携设备。

**三、可穿戴 / 多模态传感器健康监测（对接 SensorDataFactory）**

*这组覆盖 hearable 心音、smartwatch
行为、多模态被动感知等最新技术，直接对应 SensorDataFactory
的「真实传感数据分析 + 数据接口」章节。*

**\[Poster\] SAGE: Sensor-Augmented Grounding Engine for LLM-Powered
Sleep Care Agent**

*作者: Hansoo Lee, Yoonjae Cho, Sonya Kwak et al.*

*会场: Posters (Thursday) \| Thu Apr 16 16:15*

*DOI: https://doi.org/10.1145/3772363.3798959*

**摘要:** 指出「可穿戴 + LLM agent」存在 Data-Action
Gap：静态仪表板缺上下文，规则 agent 僵硬，纯 LLM agent 缺个人数据
grounding。SAGE 提出 sensor-augmented grounding engine，把传感数据注入
LLM agent，给出可执行建议。

**与AD项目关联:** ⭐⭐⭐ 与你 AD
项目架构最同构：把专家知识库塞进「grounding
engine」就是你的设计。技术对标核心，现场重点交流。

**\[Paper\] LubDubDecoder: Bringing Micro-Mechanical Cardiac Monitoring
to Hearables**

*作者: Siqi Zhang, Xiyuxing Zhang, Duc Vu et al.*

*会场: AI-Assisted Clinical Diagnosis and Reasoning \| Thu Apr 16 13:15
@ Auditorium*

*DOI: https://doi.org/10.1145/3772318.3790445*

**摘要:** 把 hearable 内置扬声器复用为声学传感器，捕获 lub-dub
心音，跨多款 hearable 解码心脏瓣膜微振动。

**与AD项目关联:** 与 ESP32 音频生态一脉相承------展示「现有硬件复用 +
声学信号 → 生理指标」可行性。AD 项目可尝试把 ESP32
麦克风复用为生理信号采集器。

**\[Paper\] MIND: Empowering Mental Health Clinicians with Multimodal
Data Insights (Narrative Dashboard)**

*作者: Ruishi Zou, Shiyu Xu, Margaret Morris et al.*

*会场: AI Explanations and Decision Support in Healthcare \| Mon Apr 13
13:15 @ Auditorium*

*DOI: https://doi.org/10.1145/3772318.3790529*

**摘要:** 融合被动感知（wearable + 手机）与主动自报（EMA /
问卷），用叙事化 dashboard 呈现给临床医生，缩短「数据 → 决策」距离。

**与AD项目关联:** AD
专家知识库向医生端暴露时，叙事化呈现（非纯图表）是高回报方向。可借 MIND
的 data storytelling 维度表。

**\[Paper\] Stress Mindset Matters: Rethinking Mental Stress Detection
with Multimodal Wearable Sensors**

*作者: Lakmal Meegahapola, Marios Constantinides, Zoran Radivojevic et
al.*

*会场: Mindfulness, Breathing, and Biofeedback Technologies \| Fri Apr
17 11:00*

*DOI: https://doi.org/10.1145/3772318.3791340*

**摘要:** 把 stress mindset 纳入可穿戴应激检测特征空间，发现 mindset
显著改变生理-心理应激响应。

**与AD项目关联:** AD 同理：患者与照护者的认知 mindset
影响传感信号可解释性。合成数据生成时要把此类心理变量作为条件。

**\[Paper\] From Sleep Scores to Self-Knowledge: Older Adults
Experiences with Oura Ring**

*作者: Aneesha Singh, Minsi Song, Stella L. Woestman et al.*

*会场: AI Literacy, Ethics, and Critical AI Understanding \| Wed Apr 15
11:00 @ Auditorium*

*DOI: https://doi.org/10.1145/3772318.3791510*

**摘要:** 研究老年人如何解读 Oura Ring
睡眠数据：从单纯评分到自我认知的转化。

**与AD项目关联:** AD
早期筛查中睡眠模式是重要信号。给出「老年人对可穿戴输出的理解模型」，帮助
Agent 端调整解释风格。

**\[Paper\] MUST: Smartwatch-based Multimodal Framework for Driver State
& Takeover Performance**

*作者: Seokyong Sheem, Yujin Cho, In Kyung Lee et al.*

*会场: Novel Mobile and Tangible Interactions \| Fri Apr 17 13:15*

*DOI: https://doi.org/10.1145/3772318.3791703*

**摘要:** 仅用 smartwatch 多模态（生理 +
IMU）预测驾驶员状态与接管性能，避开摄像头方案的侵入性。

**与AD项目关联:** 启示：smartwatch
非侵入多模态足以替代大量摄像头场景，符合 AD 老年用户对隐私的期待。

**\[Paper\] Uncertainty and Risk at Point of Care: Patient-Generated
ECGs and Algorithmic Interpretations**

*作者: Rachel Keys, Aisling Ann O Kane, Paul Marshall et al.*

*会场: AI-Assisted Clinical Diagnosis and Reasoning \| Thu Apr 16 13:15
@ Auditorium*

*DOI: https://doi.org/10.1145/3772318.3790692*

**摘要:** 基层医生如何看待「用户可穿戴 ECG +
算法解读」------不确定性的沟通是临床采纳关键。

**与AD项目关联:** AD 传感器 + AI 输出进入临床路径会遇到相同的
uncertainty communication 难题。其 vignette 研究方法可复制到 AD 语境。

**\[Paper\] Exploring Data-Driven Approaches to Stress Management: A
Systematic Review**

*作者: Youngji Koh, Jeonghyun Kim, Kwangyoung Lee et al.*

*会场: Stress Management and Emotional Regulation \| Thu Apr 16 13:15*

*DOI: https://doi.org/10.1145/3772318.3791194*

**摘要:** 可穿戴应激监测 + 干预 + 评估方法的系统综述。

**与AD项目关联:** AD
合成数据与干预闭环若涉及应激维度，这是最新方法汇总。

**四、LLM × 专家 / 临床 / 领域知识（对接 AD 专家知识库）**

*这组直接映射到 knowledge/ 下的 AD
专家知识库优化方案------知识图谱增强、clinical reasoning、RAG 工程化。*

**\[Paper\] DiagLink: Dual-User Diagnostic Assistance by Synergizing
Experts with LLMs and Knowledge Graphs**

*作者: Zihan Zhou, Yinan Liu, Yuyang Xie et al.*

*会场: AI-Assisted Clinical Diagnosis and Reasoning \| Thu Apr 16 13:15
@ Auditorium*

*DOI: https://doi.org/10.1145/3772318.3791724*

**摘要:** 面向医生 + 患者双用户的诊断辅助系统，把专家推理与 LLM +
知识图谱动态知识集成结合，针对医疗资源分布不均场景。

**与AD项目关联:** ⭐⭐⭐ 与你 AD 专家知识库思路最对齐：AD
临床专家规则/图谱 × LLM agent ×
家属/医生双端接口。强烈建议现场深度交流。

**\[Paper\] MAP-X: Medically Aligned, Patient-Centered AI Explanation
System**

*作者: Yuyoung Kim, Minjung Kim, Saebyeol Kim et al.*

*会场: AI Explanations and Decision Support in Healthcare \| Mon Apr 13
13:15 @ Auditorium*

*DOI: https://doi.org/10.1145/3772318.3790971*

**摘要:** 在高风险、数据稀缺的临床场景下，提出「医学对齐 + 患者中心」AI
解释评估蓝图，多层级验证。

**与AD项目关联:** AD 属典型「高风险 +
样本稀缺」。专家知识库对外解释必须经医生 + 患者两层验证。MAP-X
多层评估表可直接套进实验设计。

**\[Paper\] AICare: Augmenting Clinical Decision-Making with Interactive
and Interpretable AI Copilot**

*作者: AICare 团队（肾内 + 产科）*

*会场: AI Explanations and Decision Support in Healthcare \| Mon Apr 13
13:15 @ Auditorium*

*DOI: https://doi.org/10.1145/3772318.3791458*

**摘要:** 交互式可解释临床 AI copilot，基于纵向 EHR
做风险预测，用可审查可视化 + LLM 推荐 ground 输出。

**与AD项目关联:** AD 专家知识库接入 LLM 后输出侧同样需要「可解释 +
可审查」。AICare 的 UI 设计与 within-subjects 方法可复用。

**\[Paper\] Do I Trust the AI? User Perception in LLM-Supported Clinical
Reasoning**

*作者: clinical reasoning + LLM trust 研究*

*会场: People and Data \| Fri Apr 17 11:00*

*DOI: https://doi.org/10.1145/3772318.3790835*

**摘要:** 揭示医生对 LLM
诊断能力「信任校准失衡」的成因：现有评估靠标准化
benchmark，难以支持临床医生形成合理信任。

**与AD项目关联:** AD 知识库增强后的 LLM
面对神经内科医生会遇到相同的信任校准问题。本篇提供评估工具与量表。

**\[Paper\] Prompting, Oversight, and Adoption: Physicians Use of LLMs
for Diagnostic Reasoning (LMIC)**

*作者: Ushna Malik, Laiba Intizar Ahmad, Amna Hassan et al.*

*会场: AI-Assisted Clinical Diagnosis and Reasoning \| Thu Apr 16 13:15
@ Auditorium*

*DOI: https://doi.org/10.1145/3772318.3791761*

**摘要:** 混合方法研究医生在临床推理中使用 LLM 的 prompting / oversight
/ adoption 模式------prompt 日志 + 访谈。

**与AD项目关联:** 为 AD 专家知识库的「医生端交互层」提供真实 prompt
使用范式。可迁移其日志编码表到用户研究。

**\[Paper\] RAG Without the Lag: What-If Analysis for
Retrieval-Augmented Generation Pipelines**

*作者: Quentin Romero Lauro, Shreya Shankar, Sepanta Zeighami et al.*

*会场: Conversational AI \| Tue Apr 14 11:00*

*DOI: https://doi.org/10.1145/3772318.3790874*

**摘要:** 针对 RAG 管道变更代价高的痛点，提出 what-if 分析工具，快速探索
retrieval 变体。

**与AD项目关联:** AD 专家知识库上线前必然要做 RAG
选型，此工具可直接并入工程链路。

**\[Paper\] Forage: Understanding LLM-facilitated Sensemaking of
Conversation Data**

*作者: Hope Schroeder, Doug Beeferman, Maya Detwiller et al.*

*会场: Sensemaking \| Tue Apr 14 13:15*

*DOI: https://doi.org/10.1145/3772318.3791640*

**摘要:** RAG 工具 Forage，支持对非结构化会话数据做探索式
sensemaking，N=27 用户研究。

**与AD项目关联:** AD 项目访谈/家属访谈转录数据规模只会更大，Forage 提供
LLM 辅助分析的工作流模板。

**\[Paper\] Designing Around Stigma: Human-Centered LLMs for Menstrual
Health**

*作者: Amna Shahnawaz, Ayesha Shafique, Ding Wang et al.*

*会场: Sexual and Reproductive Health Technologies \| Fri Apr 17 11:00*

*DOI: https://doi.org/10.1145/3772318.3791318*

**摘要:** 在文化禁忌强的健康教育场景，用 LLM + RAG 构建 WhatsApp
chatbot，N=30 共创。

**与AD项目关联:** AD 同样伴随 stigma，其 stigma-aware prompt 工程 + RAG
安全栏可直接迁移到 AD 家属侧对话。

**\[Paper\] Aligning Multimodal LLMs with Human Experts: Focus on
Parent--Child Interaction**

*作者: Weiyan Shi, Kenny Tsu Wei Choo*

*会场: AI Systems for Human Goals \| Tue Apr 14 11:00*

*DOI: https://doi.org/10.1145/3772318.3791267*

**摘要:** 探索性研究：把多模态 LLM
与言语病理学家（SLP）对齐，用于分析亲子互动的 joint attention。

**与AD项目关联:** 与 AD 项目「语音 + 视觉 + 行为 →
认知指标」的专家对齐任务范式相同，可作为方法学模板。

**\[Paper\] LLM-Based AI Assistant for Mindfulness Practice With Older
Adults**

*作者: Lucy McCarren, Ulrika Eriksson, Laura Ortiz Mengual et al.*

*会场: Care and Lived Practices \| Wed Apr 15 11:00*

*DOI: https://doi.org/10.1145/3772318.3790734*

**摘要:** 16 位老年人参与式工作坊，探讨 LLM 正念助手的适老设计。

**与AD项目关联:** 为 AD 侧 Agent
的适老语言风格、响应节奏提供一手设计指引。

**\[Poster\] Dr.Ei: Multi-Agent, Multimodal, Human-in-the-Loop Clinical
Decision Support System**

*作者: multi-agent + multimodal CDSS*

*会场: Posters*

*DOI: https://doi.org/10.1145/3772363.3798870*

**摘要:** 两阶段多 agent、多模态 CDSS，跨学科临床医生参与真实病例评测。

**与AD项目关联:** 为 AD 专家知识库接入多 agent 架构给出具体分工参考。

**\[Poster\] Ask, Verify, Refine: Question-Aware Multimodal XUI for
Clinical Verification**

*作者: 临床验证 XUI 研究*

*会场: Posters (Tuesday) \| Tue Apr 14 18:30*

*DOI: https://doi.org/10.1145/3772363.3798745*

**摘要:** 让医生以 intent-driven question 验证 AI
医学影像输出：确认诊断、定位证据、比较替代、评估不确定性。

**与AD项目关联:** AD 多模态融合输出也需要「问题驱动验证层」，这套 XUI
范式可直接套用。

**五、强相关 Workshop / Meet-Up（建议报名）**

*以下五个 workshop + 一个 meetup 与你项目三条主线全部命中，现场 +
后续协作价值最高。*

**\[Workshop\] Everyday Wearable for Personalized Health and
Well-Being**

*作者: Chankyu Han, Hongyu Mao, Qiuyue Xue et al.*

*会场: Tue Apr 14 16:15 @ P1 - Room 120*

*DOI: https://doi.org/10.1145/3772363.3778742*

**摘要:**
聚焦日用可穿戴------把健康监测从诊所搬到手表/饰品/绷带，讨论个性化、规模化与包容性。

**与AD项目关联:** 与 AD 居家传感场景完全同域，建议带 SensorDataFactory
设计方案去交流。

**\[Workshop\] The Future of Cognitive Personal Informatics**

*作者: cognitive tracking + genAI*

*会场: Thu Apr 16 16:15*

*DOI: https://doi.org/10.1145/3772363.3778687*

**摘要:** 可穿戴认知追踪的未来：应激、专注、认知因素测量，结合 GenAI
做数据分析/可视化/解读。

**与AD项目关联:** ⭐⭐ AD 早期认知筛查 + 个人信息学最直接的
workshop，值得投 position paper。

**\[Workshop\] Speech AI for All: The What, How, and Who of
Measurement**

*作者: speech AI 多样性测量*

*会场: Thu Apr 16 18:30*

*DOI: https://doi.org/10.1145/3772363.3778768*

**摘要:** 面向非典型语音的 speech AI 测量------ASR
在非典型语音上性能差甚至造成伤害。

**与AD项目关联:** AD 患者语音即典型的「非典型」，这是 ESP32
音频侧最需要的测量共同体。

**\[Workshop\] Toward Relationship-Centered Care with AI: Designing for
Human Connections in Healthcare**

*作者: RCC + AI*

*会场: Thu Apr 16 16:15*

*DOI: https://doi.org/10.1145/3772363.3778753*

**摘要:** 关系中心照护（RCC）遇上 AI：强调信任、尊重与有意义的关系。

**与AD项目关联:** 补强专家知识库的伦理框架，照护者 / 患者 /
临床医生三方关系建模。

**\[Workshop\] Engagement in Digital Health Interventions: Open
Questions for Research and Design**

*作者: DHI engagement*

*会场: Thu Apr 16 18:30*

*DOI: https://doi.org/10.1145/3772363.3778762*

**摘要:** 数字健康干预的 engagement 概念框架讨论，跨 psych / IS / HCI。

**与AD项目关联:** AD 干预长期依从是最大挑战，这是 HCI 侧最聚焦的
engagement workshop。

**\[Meet-Up\] AI and the Self: Exploring Identity, Agency, and
Relational Personhood**

*作者: AI + 中风/丧亲/痴呆背景*

*会场: Tue Apr 14 18:30*

*DOI: https://doi.org/10.1145/3772363.3778792*

**摘要:** HCI 关于痴呆/中风/丧亲场景中 AI 对身份与关系性人格的
mediation。

**与AD项目关联:** 直接讨论 AD 患者 personhood 与 AI
的关系，适合带伦理审查问题去交流。

**六、对你 AD 项目的启示与可操作对接**

**6.1 架构层面**

-   **要点：**SAGE（Sensor-Augmented Grounding Engine）与
    DiagLink（Experts × LLM × KG）两篇是你整体架构的最近邻。建议把 SAGE
    的 grounding engine 层与 DiagLink 的 dual-user + KG 融合，作为 AD
    专家知识库 v2 参考蓝图。

-   **要点：**AICare 与 MAP-X 给出可解释 + 多层评估的临床 UI /
    评估模板，可直接套进 docs/项目总体规划.md 的评估章节。

**6.2 数据与合成**

-   **要点：**ADRD 语音研究（Cohn 2026）明确了 AD 人群 ASR
    失效的声学因素------写入 AD
    传感器合成数据方法综述，作为负样本生成条件。

-   **要点：**Stress Mindset 研究提示：合成数据要引入心理 mindset
    条件，避免生理特征过于干净。

-   **要点：**LubDubDecoder
    展示了「扬声器复用为声学传感器」的硬件复用范式，ESP32 v2 可试。

**6.3 Agent / 交互**

-   **要点：**Talking to Heirlooms + Collaborative AI Scaffolding：把
    Agent 藏进日常物件、用 VLM + 本地 TTS
    做微提示------比智能音箱形态更契合 AD 人群。

-   **要点：**Finding MeBo 给出老年人对 LLM 语音 agent
    的关系性评估维度------作为用户访谈量表。

**6.4 风险 / 伦理**

-   **要点：**LLM Dementia Stigma Poster：AD 知识库注入 LLM 前做 stigma
    审查（可借用该 poster 的评估脚本）。

-   **要点：**ECG Point of Care 研究：可穿戴 + 算法输出进入基层时的
    uncertainty communication 难题------在 AD 项目 ethical approval
    中专章说明。

**6.5 现场行动建议**

-   **推荐：**周一 13:15 Auditorium 全程 ------AI Explanations and
    Decision Support in Healthcare（MIND / AICare / MAP-X 同场）

-   **推荐：**周四 13:15 Auditorium 全程 ------AI-Assisted Clinical
    Diagnosis and Reasoning（DiagLink / LubDubDecoder / ECG
    等同场，强度最高）

-   **推荐：**周四 16:15 投稿或参会 The Future of Cognitive Personal
    Informatics workshop

-   **推荐：**周二 18:30 Meet-Up「AI and the
    Self」（身份/人格/痴呆主题）

**附录 A：检索方法与数据来源**

数据来源：CHI 2026 官方程序 JSON（本地 chi26 skill，2780 条记录）。

检索方式：Python 脚本对 title + abstract 做三主题加权关键词打分。主题
A（可穿戴-认知）：dementia / alzheimer / MCI / older adult / wearable /
smartwatch / hearable / passive sensing。主题
B（LLM-专家知识）：retrieval-augmented / knowledge graph / clinical LLM
/ expert / physician。主题 C（多模态 LLM-健康）：multimodal llm / speech
biomarker / conversational agent for health。

候选池 363 条 → 精选 \~26 篇 + 6 workshop/meetup，覆盖 Papers / Posters
/ SRC / Workshops / Meet-Ups。

报告生成器：python-docx 1.2.0。
