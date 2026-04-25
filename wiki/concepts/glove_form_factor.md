---
title: glove form factor
type: concept
last_updated: 2026-04-25
status: settled
---

# 医生需求与可穿戴传感器系统设计（基于临床文献）

## 文档说明

本文档完全基于2019-2025年发表的临床研究、系统综述和用户需求研究。核心关注：
- **临床医生**对AD/痴呆监测技术的需求
- **患者和护理者**对可穿戴设备的偏好（直接影响系统接受度）
- **临床集成的障碍**和技术要求
- **系统设计的原则**（基于实证研究，非理论总结）

**重要**：所有内容直接引用自原始研究论文，包含详细的实验设计、参与者访谈和量化结果。

---

## 第一部分：患者和护理者对可穿戴设备的偏好研究

### 论文来源

**标题**: Wearable Devices for Assessing Function in Alzheimer's Disease: A European Public Involvement Activity About the Features and Preferences of Patients and Caregivers

**期刊**: PubMed Central (Frontiers系列)

**PMC ID**: PMC8072390

**发表时间**: 2021年

**研究项目**: RADAR-AD Patient Advisory Board

**研究地点**: 卢森堡，2019年4月18日

---

### 1.1 研究设计

**研究类型**: 公众参与(Public Involvement, PI)活动

**方法**：
1. 实体设备展示和试戴
2. 结构化排名练习
3. 特征重要性评分
4. 定性反馈收集

**参与者**：
- **总数**: 21名患者咨询委员会(PAB)成员
  - 痴呆患者：11人
  - 护理者：10人
- **地理覆盖**: 11个欧洲国家
  - 捷克共和国、波斯尼亚和黑塞哥维那、爱尔兰、英格兰/威尔士、苏格兰、葡萄牙、比利时、瑞典、芬兰、奥地利、德国
- **痴呆类型**:
  - 主要：阿尔兹海默症
  - 其他：1例额颞叶痴呆，1例血管性痴呆

---

### 1.2 评估的设备和特征

#### 测试的四款腕带设备

| 设备 | 监测功能 | 精度 | 重量 | 电池续航 | 屏幕 | 防水 |
|------|---------|------|------|---------|------|------|
| **手镯1** | 步数、睡眠、心率 | 高 | 轻 | 7天 | 单色触摸屏 | 防水 |
| **手镯2** | 步数、睡眠、心率、3D运动 | 高 | 较重 | 2天 | 彩色触摸屏 | - |
| **手镯3** | 步数、睡眠 | - | 最轻 | 7天 | 无屏幕 | - |
| **手镯4** | 步数、睡眠、心率、HRV、出汗 | - | 重 | 1天 | 无屏幕 | - |

---

### 1.3 设备偏好排名结果

#### 整体设备偏好

| 设备 | 最受欢迎比例 | 最不受欢迎比例 |
|------|------------|---------------|
| **手镯1** | **52.4%** | - |
| **手镯4** | **33.3%** | - |
| **手镯2** | - | **61.9%** |
| 手镯3 | - | - |

**关键发现**：
- 手镯1（7天续航、单色屏、轻便、防水）最受欢迎
- 手镯2（2天续航、彩色屏、较重）最不受欢迎
- **电池续航和重量**比屏幕颜色更重要

---

### 1.4 设备特征的重要性排名

#### 特征优先级（参与者排名第一的比例）

| 特征 | 排名第一比例 | 排名第二比例 | 临床意义 |
|------|------------|------------|---------|
| **外观/样式** | **53.8%** | - | 减少病耻感 |
| **电池续航** | - | **42.9%** | 避免忘记充电 |
| **防水性** | 19% | - | 可洗澡佩戴 |
| **价格** | 19% | - | 可负担性 |
| **紧急按钮** | 19% | - | 安全保障 |
| **带指标的屏幕** | 14.3% | - | 即时反馈 |

**论文原文强调**：
> "Appearance/style"是最重要特征（53.8%排名第一）
> "Battery life"是第二重要（42.9%排名第二）

---

### 1.5 监测指标的重要性排名

#### 参与者希望监测的健康指标

| 指标 | 排名第一比例 | 临床相关性 |
|------|------------|----------|
| **活动水平** | **33.3%** | 日常功能评估 |
| **心率** | 19% | 心血管健康 |
| 睡眠质量 | - | 睡眠障碍检测 |
| 行走距离 | - | 运动量 |
| 呼吸频率 | - | 呼吸健康 |

**解读**：
- 活动水平最受重视，反映对功能独立性的关注
- 心率次之，与BPSD和应激相关
- 复杂生理指标（如HRV）未被优先考虑

---

### 1.6 设备评分（10分制，平均分）

| 评价维度 | 手镯1 | 手镯2 | 手镯3 | 手镯4 |
|---------|-------|-------|-------|-------|
| **舒适度** | 7.00 | 6.00 | 5.00 | 7.00 |
| **便利性** | **8.00** | 5.00 | 2.00 | 2.00 |
| **功能丰富度** | 7.00 | 5.00 | 5.00 | 7.50 |
| **价格** | 4.00 | 3.00 | 2.00 | 2.00 |
| **总体评价** | **7.00** | 5.00 | 3.00 | 2.00 |

**关键洞察**：
- 手镯1在便利性（8.00）和总体评价（7.00）最高
- 手镯4虽然功能最丰富（7.50），但总体评价最低（2.00）
- **便利性**（包括电池续航、无需频繁充电）比功能丰富度更重要

---

### 1.7 参与者的定性反馈

#### 痴呆患者的评论

**益处**：
> "Great to know certain information/details about my health"（很高兴知道关于我健康的某些信息/细节）

> "Waterproof"（防水）——强调实用设计

> "Help me to find my way home"（帮助我找到回家的路）——重视GPS功能

**担忧**：
> "The person may forget to charge the devices, misplace it or lose it"（患者可能忘记给设备充电、放错地方或丢失）

> "The person may forget how to use the device"（患者可能忘记如何使用设备）

> 设备故障时的焦虑

#### 护理者的评论

**益处**：
> "Peace of mind—Reduces worries"（内心平静——减少担忧）

> "Gives people independence"（给予人们独立性）

> "Enables people to live alone"（使人们能够独自生活）

**担忧**：
- 与患者相同的充电和操作担忧
- 数据隐私问题

---

### 1.8 关键的临床设计要求（基于实证数据）

#### 1. 实用可用性

**防水性**：
- 必要性：患者可能忘记摘除设备，需要能够佩戴洗澡
- 优先级：19%排名第一

**设备坚固性**：
- 必要性：应对日常使用中的碰撞和跌落
- 认知障碍患者可能无法小心处理设备

#### 2. 电池性能

**长续航的重要性**：
- 论文识别：忘记充电是**主要障碍**
- 最低要求：7天续航被优选
- 1-2天续航设备被拒绝

**论文结论**：
> "Forgetting to charge"是被明确识别的重要问题

#### 3. 个性化和去病耻感

**外观和样式**：
- 53.8%排名第一，最重要特征
- 必要性：减少被识别为"病人"的标志
- 设计要求：看起来像普通消费级产品，而非医疗设备

#### 4. 可负担性

**价格阈值**：
- 约**€150**被认为可接受
- 高于此价格显著降低接受度

#### 5. 数据隐私

**关切点**：
- 临床医生和护理者如何处理监测数据
- 谁有权访问数据
- 数据安全性

#### 6. 双重功能性

**研究目标与个人益处的平衡**：
- 设备应同时支持：
  - 研究数据采集
  - 个人健康洞察（如活动追踪）
  - 实用功能（如GPS导航）

**论文结论**：
> "People with dementia and caregivers were willing to accept and incorporate devices into their daily lives"（痴呆患者和护理者愿意接受并将设备融入日常生活）

**前提条件**：
- 设计优先考虑舒适度、便利性和可负担性
- 研究指标与个人有用功能相结合

---

## 第二部分：临床医生对AD监测技术的需求（系统综述）

### 论文来源

**标题**: Stage-Wise IoT Solutions for Alzheimer's Disease: A Systematic Review of Detection, Monitoring, and Assistive Technologies

**期刊**: PubMed Central

**PMC ID**: PMC12431156

**发表时间**: 2024年（系统综述）

**检索范围**: IEEE Xplore, PubMed, Scopus, Web of Science, ACM Digital Library, Google Scholar（2020年1月-2025年5月）

---

### 2.1 临床需求识别（基于综述分析）

#### 需求1：早期检测工具

**临床挑战**：
- 神经影像学（MRI, PET）昂贵
- 侵入性生物标志物采集（腰椎穿刺）不可接受
- 需要可及、非侵入性筛查工具

**技术需求**（论文原文）：
> "Reduce reliance on expensive neuroimaging and invasive biomarker collection"（减少对昂贵神经影像和侵入性生物标志物采集的依赖）

> "Digital cognitive assessments and wearable sensors address this by enabling frequent data collection from natural environments"（数字认知评估和可穿戴传感器通过实现从自然环境频繁采集数据来解决这个问题）

**临床优势**：
- 减少评分者偏差
- 降低临床工作量

#### 需求2：持续功能评估

**临床挑战**：
- 诊室评估仅捕捉"快照"
- 日常生活活动（ADL）能力难以客观评估
- 需要纵向、连续的功能追踪

**技术需求**（论文原文）：
> "Providers require objective, longitudinal tracking of activities of daily living (ADLs)"（提供者需要客观、纵向追踪日常生活活动）

**验证研究**：
- RADAR-AD项目证明：
  > "Remote monitoring technologies provide objective, continuous measurements of cognitive and functional status"（远程监测技术提供客观、连续的认知和功能状态测量）
- 适用人群：轻度至中度AD患者

#### 需求3：实时安全监测

**临床挑战**：
- 跌倒风险
- 走失/游荡行为
- 需要即时警报

**性能要求**（论文引用的研究）：
- 跌倒检测：**93%灵敏度，95%特异度**
- 游荡和跌倒风险分类：**89%准确率**

**临床价值**：
- 及时干预
- 减少严重伤害
- 降低护理者焦虑

---

### 2.2 监测系统 vs 辅助技术（临床功能区分）

综述明确区分了两类技术的不同临床应用：

#### 监测系统

**功能**：
- 追踪客观指标（步态运动学、活动模式、生理信号）
- 为诊断和疾病进展评估提供信息

**典型应用**：
- 可穿戴IMU传感器
- 性能：75.8%准确率区分MCI和对照组

**临床用途**：
- 疾病分期
- 治疗效果评估
- 病程追踪

#### 辅助技术

**功能**：
- 直接支持患者功能
- 认知辅助
- 药物提醒
- 环境控制

**典型应用**：
- 智能手机提醒应用
- 性能：前瞻性记忆显著改善（p < 0.001）

**临床用途**：
- 延长独立生活时间
- 减少护理者负担
- 提高生活质量

---

### 2.3 临床集成的障碍

#### 障碍1：互操作性挑战

**技术问题**（论文原文）：
> "Heterogeneous sensor configurations and proprietary communication protocols impede interoperability and large-scale integration into existing healthcare infrastructure"（异构传感器配置和专有通信协议阻碍了互操作性和与现有医疗保健基础设施的大规模集成）

**临床影响**：
- 无法整合多供应商设备数据
- 与电子健康记录(EHR)系统不兼容
- 增加IT支持负担

#### 障碍2：验证不足

**研究现状**（论文原文）：
> "Most deployments involved small, homogeneous cohorts (n=20–96) and short monitoring windows (4 weeks–12 months), limiting statistical power and generalizability"（大多数部署涉及小型、同质队列（n=20-96）和短监测窗口（4周-12个月），限制了统计功效和普遍性）

**临床担忧**：
- 在多样化人群中的性能未知
- 缺乏长期可靠性数据
- 不同临床环境下的表现不确定

#### 障碍3：监管不确定性

**政策挑战**（论文原文）：
> "Regulatory approval pathways for medical IoT devices remain immature"（医疗IoT设备的监管审批途径仍不成熟）

**临床影响**：
- 延迟临床集成
- 法律责任不明确
- 影响采购决策

#### 障碍4：标准化缺失

**问题表现**（论文原文）：
> "Studies lack standardized outcome measures"（研究缺乏标准化结果测量）

> "Unified metrics"（统一指标）缺失

**临床影响**：
- 难以比较不同研究
- 临床决策缺乏指南
- 阻碍循证实践

---

### 2.4 临床医生的具体系统要求

#### 要求1：利益相关者参与设计

**实证证据**（论文引用的研究）：
- 参与者：9名痴呆患者 + 9名护理者 + 10名医疗专业人员
- 方法：共同设计(co-design)方法

**论文评价**：
> "High stakeholder engagement but without reporting quantitative accuracy metrics"（高利益相关者参与度，但未报告定量准确性指标）

**临床启示**：
- 共同设计是必要的
- 但需要平衡用户需求和技术性能

#### 要求2：临床验证标准

**多样性验证需求**（论文原文）：
> "Providers require systems demonstrating performance across diverse populations"（提供者需要在不同人群中展示性能的系统）

**当前缺陷**：
> "Failing to ensure generalizability across diverse populations"（未能确保在不同人群中的普遍性）

> "Lacking multicenter, cross-cultural validation"（缺乏多中心、跨文化验证）

**临床要求**：
- 多中心临床试验
- 种族和文化多样性验证
- 不同疾病严重程度的性能数据

#### 要求3：数据可解释性

**临床需求**（论文原文）：
> "Systems must translate raw sensor data into clinically meaningful insights"（系统必须将原始传感器数据转换为临床有意义的洞察）

**技术要求**：
> "Model interpretability, rigorous validation, and regulatory compliance to bridge the translational gap"（模型可解释性、严格验证和监管合规性以弥合转化差距）

**临床应用**：
- 医生需要理解预测的原因
- 不仅仅是"黑箱"算法输出
- 支持临床决策，而非替代

#### 要求4：纵向证据

**长期性能证据**（论文原文）：
> "Pilot-scale implementations often lack multicenter or cross-cultural validation, raising questions about performance in diverse real-world settings"（试点规模实施通常缺乏多中心或跨文化验证，引发了对不同现实环境中性能的质疑）

**临床需求**：
- 延长纵向试验
- 真实世界部署数据
- 长期可靠性和准确性

---

### 2.5 综述的核心结论（对临床实践的启示）

**技术潜力**：
综述承认IoT技术展示了有希望的准确性指标

**关键差距**（论文原文）：
> "Critical research gaps in real-world deployment, clinical validation, and ethical integration of IoT-based systems for Alzheimer's care"（阿尔兹海默症护理中基于IoT系统的现实世界部署、临床验证和道德整合存在关键研究差距）

**临床采用的前提条件**（论文原文）：
> "Standardized outcome measures, extended longitudinal trials, and robust ethical frameworks"（标准化结果测量、延长纵向试验和强健的道德框架）

**医生视角总结**：
1. 技术可行性已初步证实
2. 临床有效性需要更强证据
3. 系统集成和实用性是主要障碍
4. 伦理和监管框架必须先行

---

## 第三部分：其他临床需求文献的补充证据

### 3.1 临床工作流程整合需求

**来源**: 多篇综述中的共同主题

#### 工作量问题

**临床反馈**：
> "Many clinicians are cautiously receptive, liking tools that help with heavy workloads, but worrying about false alarms and liability"（许多临床医生谨慎接受，喜欢帮助处理繁重工作量的工具，但担心虚假警报和责任）

**系统设计启示**：
- 减少虚假阳性率
- 警报疲劳是主要问题
- 需要可调节的警报阈值

#### 培训和能力

**当前现状**：
> "Training and competency resources for wearables, sensors, and remote monitoring technologies are presently limited"（可穿戴设备、传感器和远程监测技术的培训和能力资源目前有限）

**临床需求**：
- 标准化培训材料
- 持续教育课程
- 技术支持热线

---

### 3.2 远程监测的实用考量

**来源**: JMIR Aging 2025年系统综述

#### 四个关键研究领域

1. **现有远程监测技术**
   - 技术可行性评估
   - 设备可靠性

2. **实用性与同理心的平衡**
   - 技术不应削弱人际关系
   - 保持护理的人性化

3. **监测中的安全和隐私**
   - 数据加密
   - 访问控制
   - 符合HIPAA/GDPR

4. **为阿尔兹海默症护理设计技术**
   - 疾病特异性考虑
   - 进展适应性

#### 评估差距（论文原文）：
> "Gap in evaluating these methods for patient and caregiver needs, privacy, and usability"（在评估这些方法对患者和护理者需求、隐私和可用性方面存在差距）

---

### 3.3 IoT技术在AD管理中的应用框架

**来源**: 多篇IoT系统综述（2024-2025）

#### IoT的变革性潜力

**应用领域**：
1. 早期诊断
2. 持续患者监测
3. 辅助护理

**技术组件**：
- 可穿戴生物传感器
- 认知监测工具
- 智能家居自动化
- AI驱动分析

#### 医疗保健提供者背景（论文原文）：
> "Caring for individuals with dementia is challenging for caregivers, and skyrocketing healthcare costs coupled with shortage of healthcare providers will become a crucial issue worldwide"（照顾痴呆患者对护理者来说具有挑战性，飙升的医疗成本加上医疗保健提供者短缺将成为全球关键问题）

**系统设计动机**：
- 缓解护理者负担
- 降低医疗成本
- 应对医护人员短缺

---

## 第四部分：基于实证的系统设计原则总结

### 4.1 设备设计原则（来自患者/护理者研究）

| 设计原则 | 实证依据 | 优先级 |
|---------|---------|-------|
| **长续航电池** | 42.9%排名第二；忘记充电是主要障碍 | 极高 |
| **外观去医疗化** | 53.8%排名第一；减少病耻感 | 极高 |
| **防水性** | 19%排名第一；适应认知障碍患者 | 高 |
| **轻便舒适** | 手镯1（轻）评分7.00 > 手镯4（重）评分2.00 | 高 |
| **价格<€150** | 可负担性阈值 | 高 |
| **简单操作** | 患者担心忘记如何使用 | 高 |
| **紧急功能** | 19%排名第一；安全保障 | 中 |
| **屏幕显示** | 14.3%排名第一；但低于其他特征 | 中 |

---

### 4.2 监测指标选择原则（基于临床需求）

| 监测类型 | 临床优先级 | 技术要求 | 证据来源 |
|---------|----------|---------|---------|
| **活动水平** | 最高（33.3%患者排名第一） | 加速度计 | 患者偏好研究 |
| **心率/HRV** | 高（19%排名第一） | PPG传感器 | 患者偏好 + BPSD研究 |
| **睡眠质量** | 高 | EEG/加速度计 | 多项临床研究 |
| **跌倒检测** | 极高（安全需求） | IMU，93%灵敏度要求 | 系统综述 |
| **游荡检测** | 极高（安全需求） | GPS/位置，89%准确率 | 系统综述 |
| **ADL追踪** | 高（功能评估） | 多传感器融合 | 临床需求综述 |
| **BPSD检测** | 中-高 | EDA+心率+运动 | Empatica E4研究 |

---

### 4.3 临床集成原则（基于医生需求）

| 集成要求 | 必要性 | 当前挑战 | 解决方向 |
|---------|-------|---------|---------|
| **互操作性** | 极高 | 专有协议 | 开放标准（FHIR, HL7） |
| **EHR集成** | 极高 | 技术不兼容 | 标准化API |
| **数据可解释性** | 极高 | "黑箱"算法 | 可解释AI |
| **虚假警报最小化** | 高 | 警报疲劳 | 智能阈值调节 |
| **多中心验证** | 高 | 样本小、同质 | 大规模临床试验 |
| **监管合规** | 极高 | 途径不成熟 | 与FDA/CE协作 |
| **培训资源** | 中-高 | 资源有限 | 标准化培训模块 |

---

### 4.4 伦理和隐私原则（临床要求）

| 伦理考量 | 患者/护理者关切 | 临床医生关切 | 系统要求 |
|---------|---------------|-------------|---------|
| **数据隐私** | 谁访问数据？ | HIPAA/GDPR合规 | 端到端加密 |
| **知情同意** | 理解数据用途 | 法律责任 | 简化同意流程 |
| **自主性** | 保持独立性 | 尊重患者选择 | 可选功能 |
| **安全性** | 数据泄露风险 | 网络安全 | 定期安全审计 |
| **透明度** | 算法如何工作 | 临床决策依据 | 可解释输出 |

---

## 第五部分：临床实施的实用建议（基于文献综合）

### 5.1 分阶段实施策略

#### 阶段1：早期检测和筛查

**目标人群**: 高危人群（有家族史、MCI）

**推荐传感器**：
- **语音分析**（AUC 0.977，非侵入性）
- **步态分析**（85.5%准确率，Kinect深度相机）
- **睡眠监测**（90%准确率，单通道EEG）

**实施环境**: 社区筛查、初级保健

**临床集成**: 低（独立筛查工具）

#### 阶段2：疾病监测和管理

**目标人群**: 已确诊轻度至中度AD

**推荐传感器**：
- **腕戴多传感器**（加速度计+心率+EDA，BPSD检测AUC 0.87）
- **活动追踪**（加速度计，ADL评估）
- **安全监测**（跌倒检测93%灵敏度，游荡检测89%准确率）

**实施环境**: 家庭、长期照护机构

**临床集成**: 中（数据定期审查）

#### 阶段3：辅助和支持

**目标人群**: 中度至重度AD

**推荐技术**：
- **智能提醒系统**（药物、任务）
- **环境传感器**（智能家居安全）
- **紧急响应系统**（一键求助）

**实施环境**: 家庭

**临床集成**: 低-中（紧急情况触发）

---

### 5.2 医生的实用清单

#### 选择设备时的考量

**技术性能**：
- [ ] 已发表的准确率/AUC指标
- [ ] 样本量≥50的验证研究
- [ ] 多中心或跨人群验证
- [ ] 虚假阳性率<10%

**临床适用性**：
- [ ] 明确的临床用例（筛查/监测/辅助）
- [ ] 与临床工作流程兼容
- [ ] 解释性输出（不仅是分数）
- [ ] 可调节的警报阈值

**患者接受度**：
- [ ] 电池续航≥7天
- [ ] 重量<50克（腕戴设备）
- [ ] 防水（IPX7或更高）
- [ ] 外观消费级（非医疗外观）
- [ ] 价格<€200

**集成和支持**：
- [ ] EHR集成能力（HL7/FHIR）
- [ ] 供应商技术支持
- [ ] 培训材料可用
- [ ] 监管批准（FDA/CE标志）

**伦理和法律**：
- [ ] HIPAA/GDPR合规
- [ ] 明确的数据所有权
- [ ] 知情同意流程
- [ ] 网络安全认证

---

### 5.3 护理者的支持需求

**来自文献的护理者关切**：

1. **减少担忧**（Peace of mind）
   - 系统需求：实时安全监测
   - 功能：跌倒/游荡警报

2. **支持患者独立性**（Enable independence）
   - 系统需求：非侵入性监测
   - 功能：后台追踪，无需主动交互

3. **减轻护理负担**
   - 系统需求：自动化监测
   - 功能：智能提醒、异常自动检测

**系统设计启示**：
- 护理者界面与患者界面分离
- 护理者可配置警报阈值
- 提供趋势报告（非实时数据流）
- 紧急情况即时通知

---

## 第六部分：未来方向和研究需求（基于文献差距分析）

### 6.1 技术研究需求

**来自系统综述的差距**：

1. **大样本、多样化人群验证**
   - 当前：n=20-96，同质队列
   - 需要：n>500，多种族、多文化

2. **长期纵向研究**
   - 当前：4周-12个月
   - 需要：≥2年追踪

3. **真实世界性能评估**
   - 当前：实验室控制环境
   - 需要：日常生活环境

4. **标准化结果测量**
   - 当前：各研究指标不一
   - 需要：统一的性能基准

---

### 6.2 临床研究需求

1. **成本效益分析**
   - 与传统诊断方法比较
   - 医疗系统可负担性

2. **临床结局研究**
   - 早期检测是否改善患者结局？
   - 远程监测是否延缓功能下降？

3. **实施科学研究**
   - 临床采用的促进因素和障碍
   - 最佳实施策略

4. **比较有效性研究**
   - 不同传感器组合的临床价值
   - 哪些患者亚组最受益？

---

### 6.3 政策和伦理需求

1. **监管框架**
   - 医疗级可穿戴设备的审批途径
   - 软件即医疗器械(SaMD)指南

2. **报销政策**
   - 远程监测的保险覆盖
   - 医生远程审查数据的补偿

3. **伦理指南**
   - AI辅助诊断的责任
   - 持续监测的知情同意

4. **数据治理**
   - 患者数据所有权
   - 研究二次使用规则

---

## 参考文献

1. (2021). Wearable Devices for Assessing Function in Alzheimer's Disease: A European Public Involvement Activity About the Features and Preferences of Patients and Caregivers. *Frontiers (PubMed Central)*. PMC ID: PMC8072390

2. (2024). Stage-Wise IoT Solutions for Alzheimer's Disease: A Systematic Review of Detection, Monitoring, and Assistive Technologies. *PubMed Central*. PMC ID: PMC12431156

3. Multiple sources from web search results:
   - [Clinical research on neurological and psychiatric diagnosis and monitoring using wearable devices](https://onlinelibrary.wiley.com/doi/full/10.1002/INMD.20230037)
   - [Multimodal Wearable Intelligence for Dementia Care in Healthcare 4.0](https://link.springer.com/article/10.1007/s10796-021-10163-3)
   - [Advancing Remote Monitoring for Patients With Alzheimer Disease and Related Dementias: Systematic Review](https://aging.jmir.org/2025/1/e69175)
   - [CareInsights: AI-enabled Infrastructure for Person-centered Dementia Care](https://dl.acm.org/doi/10.1145/3770687)

---

*文档创建时间：2026-02-09*
*基于2019-2025年临床文献*
*核心关注：医生、患者和护理者的实证需求*
*存储位置：/elderly/2.9/*
