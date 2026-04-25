---
title: kb optimization report
type: synthesis
last_updated: 2026-04-25
status: settled
---

**AD患者多智能体系统**

**专家知识库优化方案报告**

*Knowledge Base Optimization for Multi-Agent AD Monitoring System*

、

# **目录**

# **一、当前知识库架构分析**

## **1.1 现有架构概览**

当前系统采用基于Claude API的7个专科Agent +
1个Master协调器的MDT多学科团队架构。知识库主要通过3种方式存储和注入：

-   主知识库文件: ad_staging_criteria.py (389行 Python字典)

-   各Agent的system_prompt属性 (每个50-150行医学知识)

-   Skill的推理prompt中动态注入知识库内容

## **1.2 知识库内容清单**

  ------------------------------------------------------------------------------------------------------------------
  **知识模块**          **变量名**              **内容概述**                                              **行数**
  --------------------- ----------------------- --------------------------------------------------------- ----------
  GDS 7阶段分期         GDS_STAGES              从正常到重度AD的7个阶段的临床特征/传感器标志物/治疗方案   \~117

  AT(N)生物标志物框架   AT_N_FRAMEWORK          Jack 2024修订标准，Core 1/Core 2生物标志物分类            \~35

  传感器-分期映射规则   SENSOR_STAGING_RULES    IMU/Audio/PPG/EDA四模态与AD分期对应关系                   \~90

  MCR诊断标准           MCR_CRITERIA            Verghese 2013/2014运动认知衰退综合征                      \~18

  BPSD检测矩阵          BPSD_DETECTION_MATRIX   7种行为症状的传感器特征和干预方案                         \~55

  药物知识库            MEDICATIONS             胆碱酯抑制剂/美金刚/抗淀粉样蛋白药物                      \~44

  步态常模              GAIT_NORMATIVE_DATA     Bohannon 2011老年人步态速度参考值                         \~10
  ------------------------------------------------------------------------------------------------------------------

**1.3 发现的核心问题 ：**

**Prompt-Embedded** **Knowledge（提示词嵌入知识）**

![](media/image1.png){width="5.322916666666667in" height="2.1875in"}

### **问题1: 知识三重冗余**

同一条医学知识存在于3个位置，且互不同步：

  ------------------------------------------------------------------------------------------------
  **位置**                 **示例**                                 **风险**
  ------------------------ ---------------------------------------- ------------------------------
  ad_staging_criteria.py   GDS分期、BPSD矩阵、药物知识              源文件，但修改需改Python代码

  Agent system_prompt      临床诊断Agent有90行重复的GDS/AT(N)知识   更新源文件后此处不会同步

  Skill prompt注入         ad_staging.py把整个字典json.dumps塞入    每次API调用都发送全量知识
  ------------------------------------------------------------------------------------------------

### **问题2: Token消耗过高**

每次评估的全量token消耗分析：

  -----------------------------------------------------------------------
  **环节**                   **计算**                  **Token数**
  -------------------------- ------------------------- ------------------
  7个Agent调用               7 × \~1,700 tokens        \~12,000

  Master协调器               1 × \~3,350 tokens        \~3,350

  7个Agent输出               7 × \~500 tokens          \~3,500

  Master输出                 1 × \~800 tokens          \~800

  单次评估总计                                         \~19,650

  日均消耗(5分钟/次)         19,650 × 288次            \~566万
  -----------------------------------------------------------------------

按Sonnet 4价格(\$3/M input tokens)，日均成本约 **\$17/天**。优化后可降至
**\$5/天**，节省约70%。

### **问题3: 缺乏结构化元数据**

当前知识条目缺少：

-   证据等级（RCT? 观察性研究? 专家共识?）

-   文献来源（只在注释里提了，没绑定到具体数据条目）

-   更新时间和审核周期

-   适用人群（中国 vs 西方数据）

### **问题4: 知识与角色指令混合**

以AutonomicAgent为例，system_prompt混合了角色定义和医学知识，导致：

-   更新知识需要改Agent代码

-   无法动态调整注入内容

-   非程序员（临床医生）无法参与知识维护

# **二、学术参考与理论依据**

## **2.1 核心参考论文**

  ---------------------------------------------------------------------------------------------------------------------------------
  **论文**            **年份/会议**   **核心方法**                                                 **与AD系统的关联**
  ------------------- --------------- ------------------------------------------------------------ --------------------------------
  KG4Diagnosis (Zuo,  2024, arXiv     知识图谱增强的分层多Agent诊断系统，全科+专科Agent协作        直接参考:
  Jiang等)                                                                                         分层Agent架构、KG构建方法

  MedRAG              2025, WWW       KG引导的RAG架构，从患者输入提取临床特征→KG匹配→检索相关EHR   鉴别诊断场景的KG-RAG架构

  MAC Framework       2025, npj DM    受MDT启发的多Agent对话框架，4医生+1主管最优                  验证了MDT多Agent架构的有效性

  KG-RAG              2024, Oxford    嵌入式上下文剪枝，token消耗减少\>50%                         关键参考: token效率优化
  (Bioinformatics)                                                                                 

  Cognitive Agent Lab 2025, Alz & Dem 6个Agent协作认知筛查，专门面向痴呆                           最直接相关: AD筛查Agent架构

  PHIA                2026, Nat Comm  可穿戴数据+LLM Agent，ReAct多步推理                          传感器数据解析模块模板
  (Google/Stanford)                                                                                

  i-MedRAG            2024, PSB       迭代式RAG，LLM基于前轮检索生成后续查询                       渐进式AD评估流程的参考

  LumiCare            2024,           可穿戴传感器+LLM的混合架构，专为AD患者日常监测               直接展示可穿戴+LLM的AD监测架构
                      Electronics                                                                  
  ---------------------------------------------------------------------------------------------------------------------------------

## **2.2 方法论对比**

  ------------------------------------------------------------------------------
  **方法**         **代表**        **Token效率**   **知识更新**   **适用场景**
  ---------------- --------------- --------------- -------------- --------------
  Prompt Stuffing  早期LLM应用     低 (全量发送)   手动改代码     小规模原型
  (当前)                                                          

  KG-enhanced RAG  MedRAG,         高 (按需检索)   更新KG即可     生产系统
                   KG4Diagnosis                                   

  Context Pruning  KG-RAG          最高            较复杂         实时监测
                                   (\>50%节省)                    

  Agentic RAG      i-MedRAG        中 (多轮检索)   动态           复杂诊断
  ------------------------------------------------------------------------------

## **2.3 推荐方案: KG-enhanced Agentic RAG**

结合文献调研，最适合AD监测系统的方案是 KG-enhanced Agentic RAG 架构：

-   用结构化JSON知识库组织AD领域知识

-   用KnowledgeStore动态检索相关知识片段注入Agent推理

-   用多Agent分工处理不同数据模态

-   未来可升级为向量检索RAG

# **三、优化方案详细设计**

## **3.1 P0: 知识外部化JSON + 元数据**

### **3.1.1 新的知识库目录结构**

> knowledge/
>
> schema/
>
> knowledge_entry.schema.json \# JSON Schema定义
>
> staging/
>
> gds_stages.json \# GDS 7阶段分期
>
> atn_framework.json \# AT(N)生物标志物框架
>
> sensors/
>
> imu_markers.json \# IMU传感器标志物
>
> audio_markers.json \# 语音标志物
>
> ppg_markers.json \# PPG/HRV标志物
>
> eda_markers.json \# EDA标志物
>
> clinical/
>
> bpsd/ \# BPSD分类子目录
>
> agitation.json
>
> sundowning.json
>
> \...
>
> mcr_criteria.json \# MCR标准
>
> gait_norms.json \# 步态常模
>
> loader.py \# 统一加载器
>
> knowledge_store.py \# 检索引擎

### **3.1.2 知识条目元数据结构**

每个JSON知识条目包含以下元数据字段：

  --------------------------------------------------------------------------------
  **字段**                 **类型**   **说明**                **示例**
  ------------------------ ---------- ----------------------- --------------------
  id                       string     唯一标识符              BPSD_AGITATION_001

  category                 string     知识类别                bpsd / staging /
                                                              sensor

  applicable_stages        array      适用的AD分期            \[\"mci\",
                                                              \"mild_ad\"\]

  modality                 array      相关传感器模态          \[\"eda\", \"ppg\"\]

  evidence.level           string     证据等级(A/B/C/D)       B

  evidence.sources         array      文献来源列表            \[{citation, doi,
                                                              \...}\]

  evidence.population      string     研究人群                西方老年人群

  evidence.last_reviewed   date       上次审核日期            2026-03-13

  search_query             string     PubMed自动检索关键词    Alzheimer agitation
                                                              EDA
  --------------------------------------------------------------------------------

### **3.1.3 BPSD激越条目JSON示例**

> {
>
> \"id\": \"BPSD_AGITATION_001\",
>
> \"category\": \"bpsd\",
>
> \"name\": \"激越/攻击性\",
>
> \"applicable_stages\": \[\"mci\", \"mild_ad\", \"moderate_ad\"\],
>
> \"modality\": \[\"eda\", \"ppg\", \"imu\"\],
>
> \"detection\": {
>
> \"sensor_signature\": \"EDA↑ + HR↑ + ACC活动增强\",
>
> \"sensor_auc\": 0.87,
>
> \"thresholds\": {
>
> \"eda_scl_increase\": \"\>30% above baseline\",
>
> \"hr_increase\": \"\>15bpm above resting\"
>
> }
>
> },
>
> \"evidence\": {
>
> \"level\": \"B\",
>
> \"sources\": \[{
>
> \"citation\": \"Iaboni et al., 2022\",
>
> \"study_type\": \"cohort\",
>
> \"finding\": \"AUC 0.80-0.95\"
>
> }\],
>
> \"last_reviewed\": \"2026-03-13\"
>
> }
>
> }

## **3.2 P0: Agent System Prompt瘦身 + 知识按需注入**

### **3.2.1 优化前后对比**

  -------------------------------------------------------------------------
  **维度**            **优化前**                 **优化后**
  ------------------- -------------------------- --------------------------
  system_prompt内容   角色定义 + 医学知识 +      仅角色定义和输出格式
                      阈值规则                   

  system_prompt长度   50-150行 / 500-1200 tokens 10-20行 / 150-250 tokens

  知识注入方式        全量硬编码                 按需检索相关片段

  每次知识量          所有知识 \~800 tokens      相关知识 \~200-400 tokens

  知识更新            需改Agent Python代码       编辑JSON文件即可
  -------------------------------------------------------------------------

### **3.2.2 AutonomicAgent优化示例**

优化前的system_prompt (32行, \~700 tokens):

> 你是自主神经功能专家Agent\...
>
> \## 专业能力
>
> 1\. HRV时域/频域分析
>
> \- SDNN: NN间期标准差\...
>
> \- RMSSD: 相邻间期差均方根\...
>
> \[\...全量知识\...\]
>
> \## 关键阈值
>
> \- SDNN\<50ms → \...
>
> \- LF/HF\>3.0 → \...

优化后的role_prompt (5行, \~150 tokens) + 按需知识:

> 你是自主神经功能专家Agent，担任神经内科医生。
>
> 基于PPG(HR/HRV/SpO2)和EDA(SCL/SCR)评估自主神经功能。
>
> 以JSON格式输出。

按需检索逻辑 (只在指标异常时注入相关知识):

> if features.ppg.sdnn \< 60:
>
> knowledge += store.get(\"ppg_markers.hrv_decline\")
>
> if context.is_sundowning_window:
>
> knowledge += store.get(\"ppg_markers.circadian_disruption\")
>
> if features.ppg.sdnn \< 30: \# 严重异常
>
> knowledge += store.get(\"differential.dlb_vs_ad_hrv\")

### **3.2.3 Token节省量化分析**

  -----------------------------------------------------------------------
  **场景**           **优化前**       **优化后**       **节省**
  ------------------ ---------------- ---------------- ------------------
  正常患者日常监测   \~1,700          \~600 tok/Agent  65%
                     tok/Agent                         

  MCI患者BPSD预警    \~1,700          \~1,000          41%
                     tok/Agent        tok/Agent        

  全量评估(少见)     \~1,700          \~1,500          12%
                     tok/Agent        tok/Agent        

  日均总消耗(正常)   \~566万 tokens   \~170万 tokens   70%

  日均成本           \~\$17/天        \~\$5/天         \~\$12/天
  -----------------------------------------------------------------------

## **3.3 P1: KnowledgeStore统一检索引擎**

### **3.3.1 检索接口设计**

KnowledgeStore提供统一的知识检索接口，支持多维度过滤：

> class KnowledgeStore:
>
> def query(self,
>
> stage: str = None, \# 患者当前分期
>
> modalities: list = None, \# 可用传感器模态
>
> category: str = None, \# 知识类别
>
> min_evidence: str = \"C\", \# 最低证据等级
>
> max_entries: int = 10 \# 最多返回条目
>
> ) -\> str:
>
> \"\"\"返回格式化知识文本，直接可注入prompt\"\"\"

### **3.3.2 检索流程图**

优化后的知识获取流程：

> 传感器数据 → 特征提取 → 异常检测
>
> │
>
> ▼
>
> KnowledgeStore.query(
>
> stage=患者当前分期,
>
> modalities=异常模态,
>
> min_evidence=\"B\"
>
> )
>
> │
>
> ▼ 只返回相关片段 (\~300 tokens)
>
> Agent role_prompt (\~150 tok) + 知识 + 数据
>
> │
>
> ▼
>
> Claude API 调用 (\~600-1000 tok total)

### **3.3.3 检索示例**

MCI患者，下午5点，EDA和HR异常：

> knowledge = store.query(
>
> stage=\"mci\",
>
> modalities=\[\"eda\", \"ppg\"\],
>
> category=\"bpsd\",
>
> min_evidence=\"B\",
>
> max_entries=5
>
> )
>
> \# 只返回 \~300 tokens:
>
> \# - 激越: EDA↑+HR↑+ACC增强, AUC 0.87
>
> \# - 日落综合征: 16:00-18:00 EDA+HR渐进性升高

## **3.4 P1: 集成PubMed文献检索**

通过Biopython的Entrez模块让Agent可以主动查询PubMed最新文献：

> from Bio import Entrez
>
> class PubMedTool:
>
> def search(self, query, max_results=5):
>
> handle = Entrez.esearch(
>
> db=\"pubmed\", term=query,
>
> retmax=max_results, sort=\"date\"
>
> )
>
> \# 返回最新文献摘要

通过Claude的tool_use功能让Agent按需调用：

> tools = \[{
>
> \"name\": \"search_pubmed\",
>
> \"description\": \"搜索PubMed获取AD领域最新文献\",
>
> \"input_schema\": {\"type\": \"object\", \...}
>
> }\]

## **3.5 P2: 知识过期检测与更新**

每条知识条目的evidence.last_reviewed和review_due字段支持自动过期检测：

> class KnowledgeUpdater:
>
> def check_stale(self, store, max_age_days=180):
>
> \"\"\"返回超过6个月未审核的知识条目\"\"\"
>
> async def suggest_updates(self, stale_entry, pubmed):
>
> \"\"\"对过时条目自动检索新文献并建议更新\"\"\"

# **四、实施路线图**

## **4.1 实施优先级**

  -------------------------------------------------------------------------------
  **优先级**   **任务**                          **工作量**   **收益**
  ------------ --------------------------------- ------------ -------------------
  P0           知识外部化JSON + 元数据           2-3天        可维护性大幅提升

  P0           Agent                             1-2天        Token节省\~70%
               system_prompt瘦身，知识按需注入                

  P1           KnowledgeStore统一加载/检索       1天          统一知识访问接口

  P1           集成Biopython PubMed搜索          0.5天        Agent可查最新文献

  P2           知识过期检测 + 更新建议           1天          长期维护

  P3           完整RAG（向量检索）               3-5天        知识库扩大后必要
  -------------------------------------------------------------------------------

## **4.2 知识库文件清单**

本次优化将在 /knowledge/ 目录下创建以下文件：

  -------------------------------------------------------------------------------------------
  **文件路径**                         **内容**                **来源**
  ------------------------------------ ----------------------- ------------------------------
  schema/knowledge_entry.schema.json   JSON Schema定义         新建

  staging/gds_stages.json              GDS 7阶段分期知识       从ad_staging_criteria.py迁移

  staging/atn_framework.json           AT(N)生物标志物框架     从ad_staging_criteria.py迁移

  sensors/imu_markers.json             IMU传感器标志物和阈值   从ad_staging_criteria.py迁移

  sensors/audio_markers.json           语音标志物和阈值        从ad_staging_criteria.py迁移

  sensors/ppg_markers.json             PPG/HRV标志物和阈值     从ad_staging_criteria.py迁移

  sensors/eda_markers.json             EDA标志物和阈值         从ad_staging_criteria.py迁移

  clinical/bpsd/\*.json                7种BPSD检测知识         从BPSD_DETECTION_MATRIX迁移

  clinical/mcr_criteria.json           MCR诊断标准             从MCR_CRITERIA迁移

  clinical/medications.json            药物知识库              从MEDICATIONS迁移

  clinical/gait_norms.json             步态常模数据            从GAIT_NORMATIVE_DATA迁移

  knowledge_store.py                   统一检索引擎            新建

  loader.py                            JSON文件加载器          新建
  -------------------------------------------------------------------------------------------

## **4.3 开源工具集成建议**

  ---------------------------------------------------------------------------------
  **工具**        **用途**                   **安装命令**             **优先级**
  --------------- -------------------------- ------------------------ -------------
  NeuroKit2       传感器信号处理             pip install neurokit2    P0 (已在用)

  tsfresh         自动时序特征提取           pip install tsfresh      P0

  Biopython       PubMed文献检索             pip install biopython    P1

  scispaCy        生物医学NLP                pip install scispacy     P1

  medspaCy        临床文本处理               pip install medspacy     P2

  OpenClaw Skills 医学AI技能库(869个skill)   git sparse-checkout      P2
  ---------------------------------------------------------------------------------

# **五、附录**

## **5.1 参考文献完整列表**

1.  KG4Diagnosis (Zuo, Jiang et al., 2024) - arXiv:2412.16833

2.  MedRAG (SNOW team, 2025) - WWW 2025 / IJCAI 2025

3.  MAC Framework (2025) - npj Digital Medicine

4.  KG-RAG (2024) - Bioinformatics, Oxford Academic

5.  Cognitive Agent Lab (Mekulu et al., 2025) - Alzheimer\'s & Dementia

6.  PHIA (Google/Stanford, 2026) - Nature Communications

7.  i-MedRAG (Xiong, Jin et al., 2024) - Pacific Symposium on
    Biocomputing

8.  Health-LLM (MIT/Google, 2024) - arXiv

9.  LumiCare (2024) - Electronics, MDPI

10. openCHA (UC Irvine, 2024/2025) - JAMIA Open

11. Omni-RAG (Chen, Liao et al., 2025) - ACL 2025

12. DR.KNOWS (Wu et al., 2025) - JMIR AI

13. Jack CR Jr. et al. (2024) - Revised criteria for AD diagnosis and
    staging

14. Buracchio T et al. (2010) - Rate of gait speed decline as predictor
    of MCI

15. Collins O et al. (2012) - HRV and AD risk

16. Iaboni A et al. (2022) - Wearable EDA/HR for BPSD detection

17. Verghese J et al. (2013/2014) - Motoric Cognitive Risk Syndrome

## **5.2 术语表**

  ------------------------------------------------------------------------------
  **术语**   **全称**                        **说明**
  ---------- ------------------------------- -----------------------------------
  RAG        Retrieval-Augmented Generation  检索增强生成，LLM结合外部知识检索

  KG         Knowledge Graph                 知识图谱，结构化知识表示

  MDT        Multi-Disciplinary Team         多学科团队，临床会诊模式

  GDS        Global Deterioration Scale      全球衰退量表，AD 7阶段分期

  AT(N)      Amyloid/Tau/Neurodegeneration   AD生物标志物分类框架

  BPSD       Behavioral & Psychological      痴呆行为和心理症状
             Symptoms of Dementia            

  MCR        Motoric Cognitive Risk          运动认知衰退综合征

  CCI        Composite Cognitive Index       综合认知指数

  HRV        Heart Rate Variability          心率变异性

  EDA        Electrodermal Activity          皮肤电活动
  ------------------------------------------------------------------------------
