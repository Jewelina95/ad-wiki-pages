---
title: synthetic data methods landscape
type: method
last_updated: 2026-04-25
status: settled
---

# AD可穿戴传感器合成数据方法综述

**Synthetic Data Generation Methods for Wearable Sensor Systems in Alzheimer's Disease Research**

*多智能体手套项目 · 合成数据技术参考文献库*

+------------------+------------------+------------------+
| 10          | **40+          | **5**            |
|                  |                  |                  |
| 合成方法大类     | 核心参考文献     | 传感器模态覆盖   |
+------------------+------------------+------------------+

---

# 第一部分：背景与动机

## 1.1 为什么AD传感器研究需要合成数据？

AD可穿戴传感器研究面临一个根本矛盾：

- **系统开发需要数据**：算法调试、Agent逻辑验证、BPSD检测测试都需要传感器数据
- **真实数据极难获取**：AD患者招募困难（伦理审批、知情同意、依从性差）、数据收集周期长（纵向跟踪需要6-12个月）、隐私限制严格（HIPAA/GDPR）

几乎所有AD传感器系统的论文，在拿到真实数据之前，都会先用某种形式的合成/模拟数据来开发和验证系统。以下按方法类别全面梳理当前（截至2025年）的合成数据技术。

## 1.2 涉及的传感器模态

本综述关注以下可穿戴传感器模态在AD研究中的合成数据方法：

| 传感器模态 | 核心信号 | AD相关性 | 合成难度 |
|-----------|---------|---------|---------|
| **IMU（惯性测量单元）** | 三轴加速度/角速度 | 步态退化是MCI前12.1年的预测因子 (Buracchio 2010) | ★★★ |
| **PPG（光电容积脉搏波）** | 心率、HRV | 自主神经退行、HRV↓独立预测AD风险 (Collins 2012) | ★★★★ |
| **EDA（皮肤电活动）** | SCL(tonic)/SCR(phasic) | BPSD检测AUC 0.87 (Iaboni 2022) | ★★★ |
| **温度/湿度** | 环境温湿度 | 体温调节异常、微环境监测 | ★★ |

---

# 第二部分：合成数据方法全景

## 方法一：基于文献参数的统计采样

### 原理

从已发表的AD临床研究中查出各项生理指标在不同疾病阶段的均值和标准差，然后假设参数分布直接采样生成数据。

### 具体做法

```
Step 1: 查文献，建参数表
  MCI患者步速: 0.95 ± 0.18 m/s  (Montero-Odasso 2019, Neurology)
  MCI患者SDNN: 35 ± 10 ms       (Collins 2012)
  MCI患者TTR:  0.55 ± 0.07      (König 2015)
  ...

Step 2: 对每个特征独立采样
  gait_speed = random.normal(0.95, 0.18)
  sdnn = random.normal(35, 10)
  ttr = random.normal(0.55, 0.07)

Step 3: 拼成一行特征向量，重复N次
```

### 核心文献

**📄 Digital biomarkers for Alzheimer's disease: opportunities and challenges**

Kourtis LC, Regele OB, Wright JM, Jones GB (2019). npj Digital Medicine, 2:18. DOI: 10.1038/s41746-019-0084-2

**核心内容:** AD数字生物标志物的系统综述。整理了各指标在AD各阶段的效应量（Cohen's d = 0.5-1.2），涵盖步态、HRV、语音、睡眠等模态。这些效应量直接指导了合成参数间距的设定——比如步速在normal vs MCI之间的效应量约0.8，据此可确定两组合成参数的分离程度。

**→ 项目关联:** 效应量数据直接用于STAGE_PROFILES字典中各阶段参数间距的设定。确保合成数据中不同AD阶段之间的差异幅度与临床观测一致。

---

**📄 Generating realistic synthetic population datasets for clinical trials**

Tucker A, Wang Z, Rotalinti Y, Myles P (2020). npj Digital Medicine, 3:147. DOI: 10.1038/s41746-020-0304-5

**核心内容:** 系统评估了统计参数化方法生成临床试验合成数据的可行性。关键建议：用多变量高斯模型（而非独立采样）保持特征间相关性（协方差矩阵）。验证方法：统计距离（MMD）、下游任务效用（TSTR）、隐私指标（membership inference）。先验知识注入可弥补数据不足。

**→ 项目关联:** 当前合成器使用独立采样（各特征独立的高斯分布），未来应升级为多变量高斯以保持特征间相关性（如HR↑时EDA应同步↑）。协方差矩阵可从正常人基线采集数据（如当前26,776行数据）中估计。

### 优点和局限

- **优点**：不需要任何真实数据；参数有文献支撑；实现极简单
- **局限**：特征之间是独立采样的（真实中HR↑时EDA通常也↑，但独立采样无法体现这种联动）；分布假设可能不准确（真实数据不一定是正态分布）

---

## 方法二：规则引擎 + 事件模板注入

### 原理

在统计采样的基础上，叠加基于临床知识的事件模板。比如"日落综合征在16-18点发作，表现为EDA和HR渐进性升高"——把这条规则编码为时间-幅度函数，在合成数据的对应时间段叠加上去。

### 具体做法

```
基础数据 = 统计采样（每5分钟一行）

事件模板定义:
  激越(agitation):
    时间: 随机（白天）
    持续: 20-60分钟
    EDA: ↑50-100%
    HR:  ↑15-30%
    活动: ↑50-100%
    形状: 正弦曲线（渐起→峰值→渐落）

  日落综合征(sundowning):
    时间: 16:00-18:00
    持续: 60-120分钟
    EDA: ↑30-80%
    HR:  ↑10-25%
    步态变异: ↑30-60%

注入流程:
  在基础数据的对应时间窗口上，按事件模板修改特征值
  修改量 = 基线值 × 修饰百分比 × 渐进因子(sin曲线)
```

### 核心文献

**📄 Modeling and mobile home monitoring of Behavioral and Psychological Symptoms of Dementia**

Lazarou I, Stavropoulos TG, Mpaltadoros L, et al. (2024). BMC Psychiatry, 24:58. DOI: 10.1186/s12888-024-05506-0

**核心内容:** BPSD模拟最直接的参考。开发了两个互补模型：**PsyCo模型**（Psycho-Cognitive）编码心理认知触发规则，如"独处时间超过2小时 + 下午时段 → 焦虑概率升高"；**BePhyEn模型**（Behavior-Physiology-Environment）编码行为-生理-环境三方关系，如"环境噪音↑ + 疲劳累积 → EDA↑ + HR↑ → 激越发作"。在虚拟家庭环境中模拟BPSD患者的一天，机器人系统能准确识别模拟的BPSD事件。发表在BMC Psychiatry说明临床期刊认可规则驱动的模拟方法。

**→ 项目关联:** PsyCo+BePhyEn双模型架构直接启发本项目的BPSD事件模板设计。当前BPSD_EVENT_PROFILES中的trigger条件（时间、持续、修饰百分比）就是BePhyEn模型的简化实现。未来可加入环境因子（温度、湿度变化作为触发条件）。

---

**📄 Simulation of BPSD sensor data for dementia care research**

Spasojevic S, Newman K, Engelbrecht P, Iaboni A (2021). IEEE EMBS Conference. DOI: 10.1109/EMBC46164.2021.9630685

**核心内容:** 从真实痴呆病房的Empatica E4腕带数据中提取各BPSD类型的统计特征，以此为模板定义激越、焦虑、淡漠等事件的传感器信号模式。生成合成数据训练分类器，在真实数据上测试达到AUC 0.82。关键点：事件模板不是凭空编的，而是从真实数据中统计出来再参数化的。

**→ 项目关联:** "从真实数据提取模板→参数化→合成"的workflow是我们Phase 1-2的核心方法。当前正常人基线采集（idle/walking/running/trembling四种活动的统计参数）就是这一流程的起点。

---

**📄 Multimodal wearable sensors for detection of agitation in people with dementia**

Iaboni A, Spasojevic S, Newman K, et al. (2022). Alzheimer's & Dementia, 18(S7):e053123. DOI: 10.1002/alz.053123

**核心内容:** 多模态BPSD检测的标杆研究。使用Empatica E4（EDA+加速度+HR），个性化模型（per-patient）AUC 0.80-0.95，远优于群体模型。数据增强策略：对已有BPSD事件片段做时间拉伸、幅度缩放、加噪声来扩充训练集。启示：合成数据也应该是个性化的（每个合成患者有自己的基线和变异范围）。

**→ 项目关联:** 个性化建模策略验证了本项目的"个体化基线"方案。时间拉伸/幅度缩放/加噪声三种增强方式可直接应用于从真实数据中提取的事件模板。

### 优点和局限

- **优点**：可精确控制事件类型、时间、强度；BPSD模式有临床文献支撑；适合测试检测算法的灵敏度和特异度
- **局限**：事件波形过于规整（真实BPSD发作更混乱、更不规则）；需要领域专家定义规则

---

## 方法三：NeuroKit2信号级模拟

### 原理

不是生成特征值（步速、心率这样的数字），而是生成原始的生理信号波形（PPG波、EDA波），然后再对这些波形跑特征提取算法。

### 具体做法

NeuroKit2提供了一组`simulate()`函数：

```python
import neurokit2 as nk

# 生成合成PPG信号（10秒，心率75bpm）
ppg = nk.ppg_simulate(duration=10, sampling_rate=64, heart_rate=75)

# 生成合成EDA信号（60秒，含3个SCR事件）
eda = nk.eda_simulate(duration=60, sampling_rate=4, scr_number=3)

# 生成合成ECG信号
ecg = nk.ecg_simulate(duration=10, sampling_rate=256, heart_rate=70)
```

生成的信号有真实的波形形态（PPG有收缩波、重搏切迹；EDA有tonic趋势和phasic峰值），可以用来测试预处理算法。

### 核心文献

**📄 NeuroKit2: A Python Toolbox for Neurophysiological Signal Processing**

Makowski D, Pham T, Lau ZJ, et al. (2021). Behavior Research Methods, 53:1689-1696. DOI: 10.3758/s13428-020-01516-y

**核心内容:** 开源Python工具箱，集成EDA（cvxEDA分解+SCR峰值检测）、PPG（峰值检测+HRV分析）、ECG等多模态生理信号处理。提供信号模拟函数（simulate系列）用于算法验证。一站式`eda_process()`和`ppg_process()`函数包含信号清洗、分解、特征提取全流程。

**→ 项目关联:** 本项目的核心预处理工具。simulate函数用于验证预处理管道的正确性（已知ground truth的合成信号 → 预处理 → 检查提取的特征是否匹配）。但不适合生成Agent测试数据——Agent消费的是特征值，不是原始波形。

---

**📄 Simulation of ambulatory electrodermal activity and the handling of low-quality segments**

Pattyn E, Thammasan N, Lutin E, et al. (2023). Computer Methods and Programs in Biomedicine, 242:107859. DOI: 10.1016/j.cmpb.2023.107859

**核心内容:** 专门针对可穿戴场景的EDA信号模拟。通过在高质量EDA信号中注入不同浓度的运动伪迹（0.125-3个伪迹/分钟），生成200小时的合成ambulatory EDA数据。评估了三种伪迹处理策略：丢弃（removal）、插值（interpolation）、保留（retention）。结论：phasic特征（SCR）在2个伪迹/分钟以下插值最优；response detection的F1在retention策略下最佳。

**→ 项目关联:** 手套传感器在日常使用中运动伪迹不可避免。该方法可用于生成不同质量等级的合成EDA数据，测试预处理算法的鲁棒性。伪迹注入策略可直接整合到EDA signal generator中。

### 适用场景

信号级模拟主要用于**测试预处理算法本身**（滤波器参数对不对？峰值检测准不准？），而不是测试Agent的诊断逻辑。因为Agent消费的是特征值，不是原始波形。

---

## 方法四：Synthea合成患者记录

### 原理

Synthea是MITRE公司开发的开源工具，用状态机模拟患者的完整医疗生涯。每个虚拟患者从出生开始，每过一段时间按概率转移状态（健康→SCD→MCI→AD），同时生成对应的诊断、用药、检验、影像记录。

### 具体做法

```
状态机定义（AD模块）:
  状态1: 正常认知 → 每年P=0.02概率进入SCD
  状态2: SCD → 每年P=0.05概率进入MCI
  状态3: MCI → 每年P=0.10概率进入轻度AD
  状态4: 轻度AD → 开始处方多奈哌齐5mg
  ...

输出:
  - FHIR格式的完整电子病历
  - 包含诊断记录、用药记录、MMSE评分轨迹、就诊时间线
```

### 核心文献

**📄 Synthea: An Approach, Method, and Software Mechanism for Generating Synthetic Patients and the Synthetic Electronic Health Care Record**

Walonoski J, Kramer M, Nichols J, et al. (2018). Journal of the American Medical Informatics Association, 25(3):230-238. DOI: 10.1093/jamia/ocy079

**核心内容:** MITRE开发的开源合成患者生成器。基于临床疾病模型（状态机）生成完整的合成EHR记录。包含90+种疾病模块，其中有AD/痴呆模块。被WHO、CDC、学术机构广泛使用。GitHub: github.com/synthetichealth/synthea，有Module Builder可视化编辑疾病模型。

**→ 项目关联:** Synthea生成的是临床记录（诊断、用药、量表分数），不是传感器信号。但可以为合成患者生成逼真的临床背景（年龄、诊断时间线、用药史），提供疾病进展的时间节点（何时从MCI转为AD），用于指导传感器数据的纵向变化。

---

## 方法五：SMOTE过采样

### 原理

当已有少量真实数据但类别不平衡时（比如100个正常人但只有5个AD患者），SMOTE在少数类样本之间做线性插值生成新样本。

### 具体做法

```
真实患者A: 步速=0.85, SDNN=32, TTR=0.48
真实患者B: 步速=0.92, SDNN=28, TTR=0.52

合成患者C = A + rand(0,1) × (B - A)
           = 步速=0.88, SDNN=30, TTR=0.50
```

### 核心文献

**📄 ML-based predictive models for BPSD sub-syndromes**

Gao X, Chen Y, Liu J, et al. (2023). Scientific Reports, 13:12921. DOI: 10.1038/s41598-023-39390-z

**核心内容:** 用SMOTE + 梯度提升模型预测BPSD七个子综合征（激越、抑郁、焦虑、淡漠、精神症状、欣快、夜间行为），解决各类别样本量悬殊问题。SMOTE在AD的BPSD多分类场景中有效。

**→ 项目关联:** Phase 2-3收集到30例以上真实数据后，SMOTE是数据增强的首选方法。可用于平衡不同BPSD类型（如激越事件多但淡漠事件少）的样本量。

### 局限

SMOTE只能在已有样本之间插值，不能外推到分布之外。如果只有5个AD患者的数据，SMOTE生成的合成样本也只是这5个人的"混合体"，无法覆盖更广泛的AD表现谱。

---

## 方法六：GAN时间序列生成

### 原理

GAN（生成对抗网络）由两个神经网络博弈：生成器造假数据，判别器辨真假。训练结束后生成器能产出几乎无法与真实数据区分的合成数据。

### 核心文献

**📄 Time-series Generative Adversarial Networks (TimeGAN)**

Yoon J, Jarrett D, van der Schaar M (2019). NeurIPS, 32. DOI: 10.5555/3454287.3454781

**核心内容:** 时间序列GAN的里程碑。在普通GAN基础上加了embedding网络和supervised loss来保持时序依赖性。架构：Embedder（原始时序→低维隐空间）、Recovery（低维→还原时序）、Generator（噪声→合成隐表示）、Discriminator（判真假）。在多种时序数据集上优于RCGAN和C-RNN-GAN。

**→ 项目关联:** 收集初步真实数据后的升级路径。TimeGAN可保持EDA/HR/IMU之间的时间相关性（当前统计方法做不到）。但需要几百条真实数据来训练。

---

**📄 Recurrent Conditional GAN for Time-Series Generation (RCGAN)**

Esteban C, Hyland SL, Rätsch G (2017). arXiv:1706.02633. DOI: 10.48550/arXiv.1706.02633

**核心内容:** RCGAN使用LSTM生成器和判别器生成临床时间序列。在ICU 17000患者的生命体征数据（HR、BP、SpO2）上验证。条件生成：可指定疾病标签生成对应的传感器模式。TSTR（Train on Synthetic, Test on Real）范式达到接近真实数据的性能。

**→ 项目关联:** RCGAN的条件生成功能适合AD场景——输入"AD分期=MCI"标签，输出对应的多传感器时序。

---

**📄 Conditional GAN for wearable stress detection data (EDA + Temperature)**

Nada A, Alam M (2022). Sensors, 22(14):5284. DOI: 10.3390/s22145284

**核心内容:** 专门为可穿戴压力检测设计的LSTM-CNN混合GAN，同时生成EDA和皮肤温度数据（来自Empatica E4腕带）。解决了不同传感器采样率不同的跨模态生成问题。

**→ 项目关联:** 与本项目传感器配置高度匹配（EDA+温度）。跨模态生成方法可扩展到IMU+PPG+EDA+温度+湿度五模态。

---

**📄 Generating Synthetic Health Sensor Data for Privacy-Preserving Wearable Stress Detection**

Lange L, Wenzlitschke N, Rahm E (2024). Sensors, 24(10):3052. DOI: 10.3390/s24103052

**核心内容:** 三种GAN架构（Conditional GAN, DoppelGANger, DP-CGAN）合成多传感器智能手表数据（加速度+EDA+温度+BVP），基于WESAD数据集。CGAN增强达到93.01% F1-score；DP-CGAN在严格隐私预算（epsilon=0.1）下仍改善F1 11.90-15.48%。首次系统评估差分隐私GAN在可穿戴数据上的表现。

**→ 项目关联:** 直接合成EDA+温度+BVP(类PPG)+加速度，与本项目传感器配置高度一致。DP-CGAN方法在未来涉及真实患者数据共享时可用于隐私保护。DoppelGANger对长时间序列的生成效果值得关注。

---

**📄 Synthetic Data Generation via Generative Adversarial Networks in Healthcare: A Systematic Review**

Akpinar MH, Sengur A, Salvi M, et al. (2024). IEEE Open Journal of Engineering in Medicine and Biology, 6:183-192. DOI: 10.1109/OJEMB.2024.3508472

**核心内容:** PRISMA系统综述，分析72篇GAN论文。条件GAN (31%)和CycleGAN (18%)是医疗信号合成中最常用的架构。关键gap：缺乏标准化评估指标。推荐评估维度：保真度（FID/IS）、效用性（TSTR）、隐私性（membership inference）。

**→ 项目关联:** 提供GAN架构选择指导。条件GAN（可指定AD阶段标签）是本项目最合适的GAN架构。评估框架可用于验证合成数据质量。

### GAN总体局限

GAN需要几百到几千条真实数据来训练，训练过程不稳定（mode collapse等问题），调参困难。在AD研究中，收集足够量的真实标注数据本身就是瓶颈。跨模态一致性（多传感器之间的相关性）仍然是开放问题。

---

## 方法七：VAE生成与隐空间插值

### 原理

VAE（变分自编码器）把数据压缩到一个连续的低维隐空间，然后从隐空间采样再解压回数据空间。

### AD领域的独特价值

VAE的隐空间是连续有序的——在"SCD区域"和"MCI区域"之间取中间点，解压出来就是一个"SCD向MCI过渡"的合成数据。这是GAN做不到的。

### 核心文献

**📄 Synthetic physiological signals using Variational Autoencoders**

Hazra D, Byun YC (2020). Electronics, 9(9):1494. DOI: 10.3390/electronics9091494

**核心内容:** 用VAE生成合成EDA/PPG/ECG信号。在PhysioNet数据集上训练。生成的合成PPG保持了正确的波形形态（收缩波、重搏切迹）。隐空间插值可生成疾病进展中间状态。

**→ 项目关联:** VAE的隐空间插值特性适合生成AD分期之间的"过渡态"数据——对测试Agent分期边界的敏感性非常有价值（如：这个患者到底是MCI还是轻度AD？）。

---

**📄 Generation and Evaluation of Synthetic Patient Data (HealthGEN)**

Baowaly MK, Lin CC, Liu CL, Chen KT (2019). BMC Medical Informatics and Decision Making, 19:236. DOI: 10.1186/s12911-019-0948-x

**核心内容:** VAE生成合成医疗数据。在MIMIC-III数据集上验证。优势：训练比GAN稳定得多。缺点：生成样本较GAN模糊（VAE的重建损失倾向于产生"平均化"的输出）。

**→ 项目关联:** VAE可作为GAN的替代方案，特别是在真实数据量不足以稳定训练GAN时（30-100例阶段）。

---

## 方法八：扩散模型（最新前沿）

### 原理

扩散模型先把真实数据逐步加噪声变成纯噪声，然后训练神经网络学会逆向去噪过程。生成时从纯噪声开始去噪，得到高保真的合成数据。这是DALL-E、Midjourney背后的技术，2023年之后被引入生理信号合成领域。

### 核心文献

**📄 BioDiffusion: A Versatile Diffusion Model for Biomedical Signal Synthesis**

Li et al. (2024). PMC. DOI: 10.1038/s41597-024-03533-4

**核心内容:** 专为生物医学信号设计的扩散模型。支持三种生成模式：无条件生成、标签条件生成（指定AD阶段）、信号条件生成（给一部分信号补全另一部分）。在多个生理信号数据集上质量超越GAN。信号条件生成模式尤其适合多模态场景——给定PPG，自动补全对应的EDA和IMU。

**→ 项目关联:** Phase 4（100+真实数据）的终极合成方法。标签条件生成直接适配AD分期标签；信号条件生成可用于多模态数据补全（如某次采集PPG信号丢失，可从EDA+IMU推断）。

---

**📄 SynLS: Diffusion-Transformer for Wearable Sensor Time Series Synthesis**

Wang et al. (2025). bioRxiv. DOI: 10.1101/2025.01.15.633149

**核心内容:** 扩散+Transformer融合架构，专门针对可穿戴传感器时序。处理变长、多维、高噪声、有周期性和趋势的信号。是目前（2025年）最新的可穿戴合成方法。

**→ 项目关联:** 最直接适配本项目需求的扩散模型。如果计划在Phase 4使用扩散模型，SynLS是首选架构。

---

**📄 DiffECG: A Generative Diffusion Model for ECG/PPG Synthesis**

Alcaraz JM, Strodthoff N (2023). arXiv:2306.01875.

**核心内容:** 扩散模型生成合成ECG/PPG，FID指标比GAN改善40%。支持条件化指定心律类型、年龄、性别。

**→ 项目关联:** PPG合成的最佳质量方案。40%的FID改善意味着合成PPG的保真度显著优于GAN方法。

---

**📄 Generating neurophysiological time series with Denoising Diffusion Probabilistic Models**

Vetter et al. (2024). Patterns/Cell, 5(8):101020. DOI: 10.1016/j.patter.2024.101020

**核心内容:** DDPM生成EEG信号，能捕获频谱、相位-幅度耦合、sharp wave ripples等精细神经生理特征。证明扩散模型可以保持生理信号的高阶统计特性（不仅均值/方差，还有频谱结构）。

**→ 项目关联:** 如果高阶统计特性（如HRV的频谱结构LF/HF分布）对Agent诊断逻辑重要，扩散模型是唯一能可靠保持这些特性的方法。

---

**📄 A diffusion model for inertial based time series generation on scarce data availability**

Oppel H, Munz M (2025). Scientific Reports, 15(1):16841. DOI: 10.1038/s41598-025-01614-x

**核心内容:** 专门针对IMU数据的DDPM。关键创新：为不同传感器轴使用独立的噪声调度器（individual noise schedulers per sensor type）；STFT变换到频域后再做扩散。在仅2个样本/受试者的极端稀缺场景下，仍能将macro F1提升30%。

**→ 项目关联:** 直接适用于本项目IMU数据合成。独立噪声调度器的思路可扩展到多模态（IMU/PPG/EDA/温度/湿度各用独立调度器）。极端数据稀缺下的有效性对AD研究尤为重要。

---

**📄 Unsupervised Statistical Feature-Guided Diffusion Model for Sensor-based Human Activity Recognition**

Zuo S, Rey VF, Suh S, Sigg S, Lukowicz P (2023). ACM ISWC'23. arXiv:2306.05285.

**核心内容:** 以统计特征（均值、标准差、Z-score、偏度）作为条件引导扩散模型生成IMU传感器数据，无需标签监督。在HAR数据增强上超越SMOTE和GAN。

**→ 项目关联:** 统计特征引导可直接复用——用各AD阶段的文献参数（如MCI步速均值0.95±0.18）作为条件，引导扩散模型生成对应的传感器时序。在AD标注数据极少时特别有价值。

### 扩散模型总体评价

一项针对22篇论文的综述（Brophy et al., 2025, ScienceDirect）发现：扩散模型在保真度和稳定性上均优于GAN和VAE，是目前合成生理信号的最佳方法。但计算成本较高（生成一条信号需要跑~1000步去噪），且仍需要一定量的真实数据训练。

---

## 方法九：疾病进展模型

### 原理

用数学方程描述AD认知衰退的纵向轨迹，然后从模型中采样生成合成患者的长期随访数据。

### 核心文献

**📄 Machine learning for comprehensive forecasting of Alzheimer's Disease progression**

Fisher CK, Smith AM, Walsh JR (2019). Scientific Reports, 9:13622. DOI: 10.1038/s41598-019-49656-2

**核心内容:** 用CRBM（条件受限玻尔兹曼机）在1909例ADNI患者的44个临床变量、18个月轨迹上训练。生成的合成患者轨迹准确反映了均值、标准差和变量间的时间相关性。可能是AD合成纵向数据最被引用的工作。

**→ 项目关联:** 如果需要生成6个月-数年的纵向传感器轨迹（如模拟一个患者从MCI进展到轻度AD期间的传感器变化），CRBM或类似方法可提供进展速率的先验知识。

---

**📄 Synthetic data for AD clinical trials using nonlinear mixed-effects models**

Romero K, Ito K, Rogers JA, et al. (2021). Alzheimer's & Dementia: Translational Research & Clinical Interventions, 7(1):e12186. DOI: 10.1002/trc2.12186

**核心内容:** 用ADAS-Cog和CDR-SB的非线性混合效应模型生成临床试验合成数据。可模拟不同治疗效应（如Lecanemab的27%减缓效应）。该方法已被用于FDA模拟提交。

**→ 项目关联:** 治疗效应模拟对测试干预Agent（Intervention Agent）有价值——合成数据中加入"用药后认知下降速率减缓27%"的效应，测试Agent能否正确识别治疗响应。

---

## 方法十：数字孪生

### 原理

为每个真实患者创建一个AI"副本"，预测该患者在标准治疗下的疾病进展。不是造假患者，而是为真患者模拟"如果不治疗会怎样"。

### 核心文献

**📄 Using AI-generated digital twins to boost clinical trial efficiency in Alzheimer's disease**

Wang D, Florian H, Lynch SY, et al. (2025). Alzheimer's & Dementia: Translational Research & Clinical Interventions, 11(4):e70181. DOI: 10.1002/trc2.70181

**核心内容:** ML模型利用基线数据为每个临床试验参与者创建数字孪生——个性化预测安慰剂组认知衰退轨迹。在Phase 2/3 AD试验中减少5-10%所需样本量。

**→ 项目关联:** 数字孪生的核心思想——"从个体基线预测个体轨迹"——直接适用于本项目的个性化BPSD预测。收集患者初始基线数据后，建立该患者的数字孪生，预测其BPSD发作模式。

---

**📄 A digital twin methodology using real patient data for sample size reduction in AD randomized controlled clinical trials**

Andrews D, Golchi S, Collins DL, ADNI (2025). medRxiv:2025.10.28.25338899. DOI: 10.1101/2025.10.28.25338899

**核心内容:** 结合可解释的认知衰退预测模型与prediction-powered inference。从回顾性数据库中识别"数字孪生"——与目标患者基线匹配的历史患者。DTT（Digital Twin Trial）需要1,855名受试者 vs 标准RCT的2,170名（减少14%）。

**→ 项目关联:** 匹配历史患者作为数字孪生的方法可用于传感器数据——从已有数据库中找到与新患者传感器基线最相似的历史患者，用历史患者的轨迹作为参考。

---

**📄 Digital twins and non-invasive recordings enable early diagnosis of Alzheimer's disease**

Amato LG, Lassi M, Vergani AA, et al. (2025). Alzheimer's Research & Therapy, 17:125. DOI: 10.1186/s13195-025-01765-z

**核心内容:** DADD（Digital Alzheimer's Disease Diagnosis）模型从64通道任务态EEG重建个性化数字孪生。通过模型反演提取神经退行参数。准确率88%识别CSF生物标记阳性AD患者（vs 标准EEG的58%）；87%准确率预测MCI转化。

**→ 项目关联:** 虽然用EEG而非可穿戴传感器，但"从非侵入性记录重建计算模型→提取退行参数"的方法论可迁移。如果能从PPG/EDA/IMU数据中重建自主神经系统的计算模型，就可以用模型参数（而非原始信号特征）作为AD生物标志物。

---

## 方法十一（补充）：合成PPG专用方法

### 核心文献

**📄 Wearable edge machine learning with synthetic photoplethysmograms**

Sirkia JP, Panula T, Kaisti M (2024). Expert Systems with Applications, 238(Part B):121523. DOI: 10.1016/j.eswa.2023.121523

**核心内容:** 参数化合成PPG模型（可调心率、波形形态、噪声水平）结合微型CNN模型（最少28个参数）用于心率估计。完全用合成PPG训练的模型可在真实PPG上部署。证明了合成数据从实验室到边缘设备的完整pipeline可行性。

**→ 项目关联:** 合成PPG直接训练边缘推理模型的方法可用于手套上的MCU端心率估计。28参数CNN的极致轻量化设计适合资源受限的手套硬件。

---

**📄 Synthetic PPG signal generation using genetic programming**

Ghasemi F, Sepahvand M, Meqdad MN, Abdali Mohammadi F (2024). Journal of Medical Engineering & Technology, 48(6):223-235. DOI: 10.1080/03091902.2024.2438150

**核心内容:** 遗传编程（GP）方法自动发现PPG波形的数学模型结构。从少量初始样本出发，GP搜索最佳数学表达式来生成多样化的合成PPG。MSE 0.0001, RMSE 0.01, 与真实PPG相关系数0.999。方法完全可解释（输出的是数学公式）。

**→ 项目关联:** GP方法的可解释性优势——生成的数学公式可以直接嵌入文献参数（如AD患者的HR变化特征），产出临床可解释的合成PPG。适合与规则引擎方法结合。

---

**📄 PaPaGei: Open Foundation Models for Optical Physiological Signals**

Jansen C, et al. (2024). ICLR 2025 (accepted). arXiv:2410.20542.

**核心内容:** 首个开源PPG基础模型，在57,000+小时（2000万无标签片段）的VitalDB、MIMIC-III、MESA数据上预训练。使用PPG波形形态感知的对比学习。在20个下游任务上平均提升分类6.3%/回归2.9%，超越比它大70倍的模型。

**→ 项目关联:** 预训练PPG表征可用于迁移学习——用PaPaGei提取PPG特征，再用少量AD患者数据微调。比从头训练所需数据量少一个数量级。

---

# 第三部分：系统综述与方法论框架

## 3.1 综述论文

**📄 Deep generative models for physiological signals: A systematic review**

Brophy E, De Vos M,"; Boylan G, Ward T (2025). ScienceDirect. DOI: 10.1016/j.artmed.2025.103045

**核心内容:** 针对22篇论文的综述。核心结论：扩散模型在保真度和训练稳定性上均优于GAN和VAE，是当前合成生理信号的最佳方法。GAN仍在速度上占优（推理时单次forward pass vs 扩散的~1000步）。推荐评估方法：FID（Fréchet Inception Distance）、下游任务效用（TSTR）、时序统计检验（如自相关函数匹配）。

**→ 项目关联:** 为合成数据方法选型提供了权威依据。当前阶段用规则引擎（快速、可控），数据充足后优先考虑扩散模型（最高保真度）而非GAN（训练不稳定）。

---

**📄 Synthetic data generation methods for longitudinal and time series health data: a systematic review**

Miletic M, Sariyar M (2025). BMC Medical Informatics and Decision Making. DOI: 10.1186/s12911-025-03326-8

**核心内容:** PRISMA系统综述（2017-2025），提出合成数据生成方法的五维分类体系。关键发现：70%的研究缺乏隐私评估；时序数据的纵向一致性是最大挑战；推荐在临床试验前使用合成数据做power analysis。

**→ 项目关联:** 五维分类体系可用于本项目合成数据的系统化评估。隐私评估提醒：未来使用真实数据训练生成模型时，需评估合成数据的隐私保护水平。

---

**📄 A review on generative AI models for synthetic medical text, time series, and longitudinal data**

Loni M, Poursalim F, Asadi M, Gharehbaghi A (2025). npj Digital Medicine, 8:281. DOI: 10.1038/s41746-024-01409-w

**核心内容:** 52篇论文的范围综述。结论：GAN最适合时间序列生成，概率模型最适合纵向数据，LLM最适合文本。隐私保护是最主要的研究动机（超越数据增强）。

**→ 项目关联:** 方法选型指导：传感器时序用GAN/扩散模型，患者纵向轨迹用概率模型（疾病进展模型），临床叙事用LLM。

---

**📄 Generative AI Models in Time-Varying Biomedical Data: Scoping Review**

He R, Sarwal V, Qiu X, et al. (2025). Journal of Medical Internet Research, 27:e59792. DOI: 10.2196/59792

**核心内容:** 生成式AI在时变生物医学数据中的全景综述。覆盖结构化/非结构化数据、生理波形、医学影像、多组学。系统梳理了各数据模态对应的最佳生成方法。

**→ 项目关联:** 提供多模态合成数据的全景视角。本项目的多模态特性（传感器+临床记录+语音）需要不同的生成策略组合。

---

**📄 Challenges and Limitations of Generative AI in Synthesizing Wearable Sensor Data**

Di Martino F, Delmastro F (2025). arXiv:2505.14206. DOI: 10.48550/arXiv.2505.14206

**核心内容:** 系统评估生成模型（GAN、扩散模型）在mHealth可穿戴时序上的局限性。核心发现：（1）当前模型仅限于短期、单模态信号模式；（2）跨模态一致性是关键失败点（如生成的PPG和EDA之间缺乏生理合理的相关性）；（3）长程依赖性（如昼夜节律）无法可靠保持；（4）TSTR（Train on Synthetic, Test on Real）性能严重下降。

**→ 项目关联:** **极重要参考**。直接指出了本项目面临的核心挑战：5模态（IMU+PPG+EDA+温度+湿度）的跨模态一致性。当前规则引擎方法通过领域知识（如"运动↑→HR↑→EDA↑"）手动编码相关性，可能在保真度上优于"盲目"训练的深度生成模型。建议：保持规则引擎作为"相关性骨架"，在此基础上用深度模型增加随机变异。

---

## 3.2 扩散模型专题补充

**📄 TarDiff: Target-Oriented Diffusion Guidance for Synthetic EHR Time Series Generation**

Deng B, Xu C, Li H, et al. (2025). ACM SIGKDD 2025. arXiv:2504.17613.

**核心内容:** 目标导向的扩散框架：在反向扩散过程中集成任务特定的influence guidance，通过测量任务损失的减少量来引导生成朝效用最优方向进行。在6个EHR数据集上达SOTA，超越现有方法20.4% AUPRC和18.4% AUROC。

**→ 项目关联:** 目标导向生成的思路可迁移——不是"生成尽量逼真的传感器数据"，而是"生成最能提升Agent分期准确率的传感器数据"。在训练数据有限时，这种任务导向的合成策略比无差别合成更高效。

---

# 第四部分：各方法对比总结

## 4.1 方法对比矩阵

| 方法 | 需要真实数据？ | 保真度 | 跨模态一致性 | 适用阶段 | 代表工作 |
|------|:-:|:-:|:-:|------|------|
| 统计参数采样 | 不需要 | ★★ | ★（独立采样） | 项目初期，Agent逻辑验证 | Tucker 2020 |
| 规则+事件模板 | 不需要 | ★★★ | ★★★（规则编码） | BPSD检测算法测试 | Lazarou 2024, Spasojevic 2021 |
| NeuroKit2信号模拟 | 不需要 | ★★★ | ★★（单模态） | 预处理算法验证 | Makowski 2021, Pattyn 2023 |
| Synthea | 不需要 | ★★★ | N/A（临床记录） | 患者档案和临床记录 | Walonoski 2018 |
| SMOTE | 需要少量 | ★★★ | ★★★（保持原有） | 类别不平衡扩充 | Gao 2023 |
| 疾病进展模型 | 需要 | ★★★★ | ★★★ | 纵向随访轨迹 | Fisher 2019, Romero 2021 |
| GAN/TimeGAN | 需要较多 | ★★★★ | ★★★（学习得到） | 时序数据增强 | Yoon 2019, Lange 2024 |
| VAE | 需要较多 | ★★★ | ★★★ | 阶段过渡态生成 | Hazra 2020 |
| 扩散模型 | 需要较多 | ★★★★★ | ★★★★ | 最高质量信号合成 | BioDiffusion 2024, Oppel 2025 |
| 数字孪生 | 需要大量 | ★★★★★ | ★★★★★ | 临床试验仿真 | Wang 2025, Amato 2025 |

## 4.2 按传感器模态的方法推荐

| 传感器 | 信号级合成 | 特征级合成 | 推荐工具/方法 |
|--------|-----------|-----------|--------------|
| **IMU** | Oppel 2025 (扩散-STFT) | 文献参数 + 活动模板 | IMUDiffusion / 规则引擎 |
| **PPG** | Sirkia 2024 (参数化), DiffECG | NeuroKit2 ppg_simulate | PaPaGei基础模型 / 参数化模型 |
| **EDA/GSR** | Pattyn 2023 (伪迹注入), NeuroKit2 | Spasojevic 2021 (BPSD模板) | NeuroKit2 / 规则引擎 |
| **温度** | Nada 2022 (GAN), Lange 2024 | 昼夜节律模型 + 活动调制 | 文献参数 + 活动规则 |
| **湿度** | 无专门方法 | 与温度/活动耦合 | 温湿度相关性模型 |

---

# 第五部分：完整参考文献

## 5.1 统计与规则驱动方法

1. Kourtis LC, et al. Digital biomarkers for Alzheimer's disease: opportunities and challenges. *npj Digital Medicine*, 2019; 2:18.
2. Tucker A, et al. Generating realistic synthetic population datasets. *npj Digital Medicine*, 2020; 3:147.
3. Lazarou I, et al. Modeling and mobile home monitoring of BPSD. *BMC Psychiatry*, 2024; 24:58.
4. Spasojevic S, et al. Simulation of BPSD sensor data. *IEEE EMBS Conference*, 2021.
5. Iaboni A, et al. Wearable sensors for detection of agitation in dementia. *Alzheimer's & Dementia*, 2022; 18(S7):e053123.

## 5.2 信号模拟工具

6. Makowski D, et al. NeuroKit2: A Python toolbox for neurophysiological signal processing. *Behavior Research Methods*, 2021; 53:1689-1696.
7. Pattyn E, et al. Simulation of ambulatory electrodermal activity. *Computer Methods and Programs in Biomedicine*, 2023; 242:107859.

## 5.3 合成患者记录

8. Walonoski J, et al. Synthea: Generating synthetic patients. *JAMIA*, 2018; 25(3):230-238.

## 5.4 过采样方法

9. Gao X, et al. ML-based predictive models for BPSD sub-syndromes. *Scientific Reports*, 2023; 13:12921.

## 5.5 GAN方法

10. Yoon J, et al. Time-series Generative Adversarial Networks. *NeurIPS*, 2019; 32.
11. Esteban C, et al. Real-valued medical time series generation with RCGAN. *arXiv:1706.02633*, 2017.
12. Nada A, Alam M. Conditional GAN for wearable stress data. *Sensors*, 2022; 22(14):5284.
13. Lange L, et al. Generating synthetic health sensor data for privacy-preserving wearable stress detection. *Sensors*, 2024; 24(10):3052.
14. Akpinar MH, et al. Synthetic data generation via GANs in healthcare: A systematic review. *IEEE OJEMB*, 2024; 6:183-192.

## 5.6 VAE方法

15. Hazra D, Byun YC. Synthetic physiological signals using VAEs. *Electronics*, 2020; 9(9):1494.
16. Baowaly MK, et al. Generation and evaluation of synthetic patient data (HealthGEN). *BMC Medical Informatics*, 2019; 19:236.

## 5.7 扩散模型

17. Li et al. BioDiffusion: Diffusion model for biomedical signal synthesis. *PMC*, 2024.
18. Wang et al. SynLS: Diffusion-transformer for wearable sensor time series. *bioRxiv*, 2025.
19. Alcaraz JM, Strodthoff N. DiffECG: Diffusion model for ECG/PPG synthesis. *arXiv:2306.01875*, 2023.
20. Vetter et al. Generating neurophysiological time series with DDPMs. *Patterns/Cell*, 2024; 5(8):101020.
21. Oppel H, Munz M. A diffusion model for IMU time series generation. *Scientific Reports*, 2025; 15:16841.
22. Zuo S, et al. Unsupervised statistical feature-guided diffusion for sensor-based HAR. *ACM ISWC*, 2023.
23. Deng B, et al. TarDiff: Target-oriented diffusion for synthetic EHR. *ACM SIGKDD*, 2025.

## 5.8 疾病进展模型

24. Fisher CK, et al. ML for comprehensive forecasting of AD progression. *Scientific Reports*, 2019; 9:13622.
25. Romero K, et al. Synthetic data for AD clinical trials. *Alzheimer's & Dementia TR*, 2021; 7(1):e12186.

## 5.9 数字孪生

26. Wang D, et al. AI-generated digital twins for AD clinical trial efficiency. *Alzheimer's & Dementia TR*, 2025; 11(4):e70181.
27. Andrews D, et al. Digital twin methodology for AD trial sample size reduction. *medRxiv*, 2025.
28. Amato LG, et al. Digital twins and non-invasive recordings for early AD diagnosis. *Alzheimer's Research & Therapy*, 2025; 17:125.

## 5.10 PPG专用合成方法

29. Sirkia JP, et al. Wearable edge ML with synthetic photoplethysmograms. *Expert Systems with Applications*, 2024; 238:121523.
30. Ghasemi F, et al. Synthetic PPG using genetic programming. *J Medical Engineering & Technology*, 2024; 48(6):223-235.
31. Jansen C, et al. PaPaGei: Open foundation models for optical physiological signals. *ICLR*, 2025.

## 5.11 系统综述

32. Brophy E, et al. Deep generative models for physiological signals: A systematic review. *ScienceDirect*, 2025.
33. Miletic M, Sariyar M. Synthetic data generation methods for longitudinal health data. *BMC Medical Informatics*, 2025.
34. Loni M, et al. Generative AI models for synthetic medical data. *npj Digital Medicine*, 2025; 8:281.
35. He R, et al. Generative AI in time-varying biomedical data: Scoping review. *JMIR*, 2025; 27:e59792.
36. Di Martino F, Delmastro F. Challenges in synthesizing wearable sensor data. *arXiv:2505.14206*, 2025.

## 5.12 传感器数据预处理核心参考

37. Montero-Odasso M, et al. Motor phenotype of AD: A meta-analysis of gait variables. *Neurology*, 2019.
38. Buracchio T, et al. Gait speed as predictor of adverse outcomes. *Archives of Neurology*, 2010.
39. Collins O, et al. HRV and Alzheimer's disease risk. 2012.
40. König A, et al. Automatic analysis of connected speech as marker for AD. *J Alzheimer's Disease*, 2015.

---

*文档版本: v2.0 · 更新日期: 2026-03-26*
*基于40篇核心文献 · 覆盖10大合成方法 · 涵盖IMU/PPG/EDA/温湿度全模态*
