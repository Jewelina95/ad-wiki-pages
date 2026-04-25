---
title: 5 个 OpenNeuro 数据集对应的论文
type: dataset
last_updated: 2026-04-25
status: settled
sources:
  - wiki/datasets/external/_external_datasets_registry.md
---

# 5 个 OpenNeuro 数据集对应的论文

合成数据 v1 校准用的 5 个外部数据集，每个对应的原始 paper 和数据描述论文。

---

## 1. ds004504 — AD/FTD/Healthy EEG (n=88)

**Paper**：
> Miltiadous A, Tzimourta KD, Afrantou T, Ioannidis P, Grigoriadis N, Tsalikakis DG, Angelidis P, Tsipouras MG, Glavas E, Giannakeas N, Tzallas AT.
> **A Dataset of Scalp EEG Recordings of Alzheimer's Disease, Frontotemporal Dementia and Healthy Subjects from Routine EEG**.
> *Data*. 2023; 8(6):95.
> doi: [10.3390/data8060095](https://doi.org/10.3390/data8060095)

**OpenNeuro**: https://openneuro.org/datasets/ds004504  
**Paper PDF**: https://www.mdpi.com/2306-5729/8/6/95

**数据**: 88 名受试者 — 36 AD + 23 FTD + 29 健康对照 · 19 通道 EEG (Nihon Kohden, 10-20 系统) · 500 Hz · 闭眼 resting state · MMSE 三组分布 (AD μ=17.75, FTD μ=22.17, CN=30)

**我们怎么用它**: MMSE 分布主校准源（已写进 `code/data/distributions_master.json`）

---

## 2. ds007427 — AD/MCI EEG · 哥伦比亚 PSEN1 E280A 队列 (n=138)

**Paper**：
> Henao Isaza V, Tobón Quintero CA, Ochoa Gómez JF (with Aguillon, Lopera).
> **Comprehensive methodology for sample enrichment in EEG biomarker studies for Alzheimer's risk classification**.
> *PLOS ONE*. 2026.
> doi: [10.1371/journal.pone.0343722](https://doi.org/10.1371/journal.pone.0343722)

**OpenNeuro**: https://openneuro.org/datasets/ds007427  
**Funder**: Universidad de Antioquia, Colombia

**数据**: PSEN1 E280A 携带者（哥伦比亚 paisa 队列, Lopera 实验室）—— 这是**世界最大的家族性 AD 队列**之一，PSEN1 E280A 携带者大概 40 多岁就发病，相当于自然加速版的 MCI 进展曲线 · 多 cohort（UdeA1 + UdeA2 等）合并后 n=138 · MMSE μ=24.0, σ=3.84

**相关论文（背景引用）**：
- Ochoa JF et al. 2017 *J Alzheimer's Dis* — Precuneus failures detected with quantitative EEG ([链接](https://journals.sagepub.com/doi/10.3233/JAD-161291))
- García-Pretelt FJ et al. 2022 *J Alzheimer's Dis* — Automatic classification using ML + resting-state EEG ([链接](https://journals.sagepub.com/doi/abs/10.3233/JAD-210148))
- Lopera lab Lancet Neurology / Alzheimer's & Dementia 多篇基础队列论文

**我们怎么用它**: MCI / at-risk 中度区间 MMSE 校准 · 加速进展型 persona 模板

---

## 3. ds006095 — Mind in Motion · 老年人不平地形步行 (n=71)

**Paper**：
> Liu C, Pliner EM, Salminen JS et al. (Daniel P. Ferris, lead PI).
> **Mind in Motion: Older Adults Walking Over Uneven Terrain** (OpenNeuro dataset).
> doi: [10.18112/openneuro.ds006095.v1.0.0](https://doi.org/10.18112/openneuro.ds006095.v1.0.0)
> 
> **Funding**: NIH U01AG061389 (Human Neuromechanics Lab, U Florida)

**OpenNeuro**: https://openneuro.org/datasets/ds006095

**关联已发表 paper**（项目组同一队列）：
> Pliner EM, Liu C, Ferris DP.
> **Uneven terrain treadmill walking in younger and older adults**.
> *PLOS ONE*. 2022.
> doi: [10.1371/journal.pone.0278646](https://doi.org/10.1371/journal.pone.0278646)
> 
> Liu C, Salminen JS, Ferris DP et al.
> **Mobile electroencephalography captures differences of walking over even and uneven terrain**.
> *Frontiers in Sports and Active Living*. 2022.
> doi: [10.3389/fspor.2022.945341](https://doi.org/10.3389/fspor.2022.945341)

**数据**: 71 名老年人 · 高密度 dual-layer EEG + 颈 EMG + IMU + 地面反力 + 不平地形步行 · 任务：每个条件 2 trial × 3 min + 3 min 静坐基线

**我们怎么用它**: ⭐ **最关键** —— 老年人 IMU + MoCA baseline。**71 例老年健康人 IMU + 认知评估**，这个直接给我们"老年健康人步态/手部运动 + 认知基线"——和手套项目最对得上。**用它替换我们 N=4 年轻人 baseline，是当前最高 ROI 的一步**。

---

## 4. ds004796 — PEARL-Neuro · 波兰中年痴呆风险队列 (n=192)

**Paper**：
> Dzianok P, Kublik E.
> **PEARL-Neuro Database: EEG, fMRI, health and lifestyle data of middle-aged people at risk of dementia**.
> *Scientific Data*. 2024; 11:276.
> doi: [10.1038/s41597-024-03106-5](https://doi.org/10.1038/s41597-024-03106-5)

**OpenNeuro**: https://openneuro.org/datasets/ds004796 (DOI: 10.18112/openneuro.ds004796.v1.0.4)  
**Paper 全文**: https://www.nature.com/articles/s41597-024-03106-5  
**项目主页**: https://github.com/PTDZ/PEARL-Neuro

**数据**: 192 名中年人 (50-63 岁) · APOE + PICALM 基因型 · 7 项神经心理测试 · 79 人子集有 EEG + fMRI · 基础血检 · 健康量表 + 生活方式 (运动/饮食/睡眠) · BIDS 标准格式

**相关后续论文**：
> Dzianok P et al.
> **Alzheimer's disease-like features in resting state EEG/fMRI of cognitively intact and healthy middle-aged APOE/PICALM risk carriers**.
> *PMC12231819*. 2025.
> https://pmc.ncbi.nlm.nih.gov/articles/PMC12231819/

**我们怎么用它**: SCD / 早期风险阶段建模参考 · APOE + 生活方式 → 风险型 persona 模板（填补我们 SCD 阶段空白，因为我们大部分数据都是已发病患者）

---

## 5. ds002778 — UC San Diego Resting State EEG · PD vs Healthy (n=31)

**Paper**：
> George JS, Strunk J, Mak-McCully R, Houser M, Poizner H, Aron AR.
> **Dopaminergic therapy in Parkinson's disease decreases cortical beta band coherence in the resting state and increases cortical beta band power during executive control**.
> *NeuroImage: Clinical*. 2013; 3:261-270.
> doi: [10.1016/j.nicl.2013.07.013](https://doi.org/10.1016/j.nicl.2013.07.013)

**OpenNeuro**: https://openneuro.org/datasets/ds002778  
**数据集策展**: Alex Rockhill (U Oregon) — `arockhil@uoregon.edu`（论文发表前请联系策展人）

**数据**: 15 名 PD 患者（8 女, μ=62.6 岁）+ 16 名匹配健康对照（9 女, μ=63.5 岁）· 32 通道 Biosemi Active Two EEG · 512 Hz · 静息 ≥3 分钟 · PD 患者 ON/OFF 用药两次访问（顺序均衡）· 受试者均来自 Scripps Clinic, La Jolla, CA

**我们怎么用它**: PD 对照桶 / **AD vs PD 鉴别诊断** —— 这条专门支撑 ClinicalAgent 写鉴别诊断时的依据
- AD: 后部 alpha 减低 + theta 增加
- PD: 用药 ON 状态降低 cortical beta band coherence

---

## 引用合集（BibTeX）

```bibtex
@article{miltiadous2023eegdataset,
  author = {Miltiadous, A. and Tzimourta, K.D. and Afrantou, T. and Ioannidis, P. and Grigoriadis, N. and Tsalikakis, D.G. and Angelidis, P. and Tsipouras, M.G. and Glavas, E. and Giannakeas, N. and Tzallas, A.T.},
  title = {A Dataset of Scalp {EEG} Recordings of {A}lzheimer's Disease, Frontotemporal Dementia and Healthy Subjects from Routine {EEG}},
  journal = {Data},
  volume = {8},
  number = {6},
  pages = {95},
  year = {2023},
  doi = {10.3390/data8060095}
}

@article{henaoisaza2026enrichment,
  author = {Henao Isaza, V. and Tobón Quintero, C.A. and Ochoa Gómez, J.F.},
  title = {Comprehensive methodology for sample enrichment in {EEG} biomarker studies for {A}lzheimer's risk classification},
  journal = {PLOS ONE},
  year = {2026},
  doi = {10.1371/journal.pone.0343722}
}

@misc{ferris2024mindinmotion,
  author = {Liu, C. and Pliner, E.M. and Salminen, J.S. and Ferris, D.P. and others},
  title = {Mind in Motion Older Adults Walking Over Uneven Terrain},
  year = {2024},
  publisher = {OpenNeuro},
  doi = {10.18112/openneuro.ds006095.v1.0.0}
}

@article{pliner2022uneven,
  author = {Pliner, E.M. and Liu, C. and Ferris, D.P.},
  title = {Uneven terrain treadmill walking in younger and older adults},
  journal = {PLOS ONE},
  year = {2022},
  doi = {10.1371/journal.pone.0278646}
}

@article{dzianok2024pearl,
  author = {Dzianok, P. and Kublik, E.},
  title = {{PEARL}-{N}euro Database: {EEG}, f{MRI}, health and lifestyle data of middle-aged people at risk of dementia},
  journal = {Scientific Data},
  volume = {11},
  pages = {276},
  year = {2024},
  doi = {10.1038/s41597-024-03106-5}
}

@article{george2013dopaminergic,
  author = {George, J.S. and Strunk, J. and Mak-McCully, R. and Houser, M. and Poizner, H. and Aron, A.R.},
  title = {Dopaminergic therapy in {P}arkinson's disease decreases cortical beta band coherence in the resting state and increases cortical beta band power during executive control},
  journal = {NeuroImage: Clinical},
  volume = {3},
  pages = {261--270},
  year = {2013},
  doi = {10.1016/j.nicl.2013.07.013}
}
```

---

## Method 章节模板（论文 draft 阶段直接抄）

```latex
\subsection{External Datasets for Distribution Calibration}

To ensure synthetic patient trajectories reflect real-world AD phenotypes
across the cognitive spectrum (healthy → SCD → MCI → AD; with PD as
differential reference), we calibrated generator parameters against
five publicly available cohorts on OpenNeuro (total n=520):

\begin{itemize}
\item \textbf{ds004504}~\cite{miltiadous2023eegdataset} (n=88, 36 AD / 23 FTD / 29 CN):
clinical 19-channel EEG with MMSE — primary anchor for the
\emph{stage → MMSE} joint distribution.

\item \textbf{ds007427}~\cite{henaoisaza2026enrichment} (n=138, PSEN1 E280A
Colombian paisa carriers): familial AD with accelerated progression curve;
calibrates the MCI / at-risk middle stratum.

\item \textbf{ds006095}~\cite{ferris2024mindinmotion} (n=71, older adults):
high-density EEG + EMG + IMU during uneven-terrain locomotion —
\textbf{primary IMU baseline source for elderly healthy subjects}.

\item \textbf{ds004796}~\cite{dzianok2024pearl} (n=192, PEARL-Neuro middle-aged
Polish cohort): EEG + fMRI + APOE + lifestyle — used to model SCD-stage
risk persona (filling the early-stage gap absent in symptomatic cohorts).

\item \textbf{ds002778}~\cite{george2013dopaminergic} (n=31, 15 PD / 16 HC):
resting-state EEG with ON/OFF medication — used as differential-diagnosis
reference for AD vs PD.
\end{itemize}

We extracted age, sex, MMSE/MoCA, and EEG power-band distributions from each
cohort and integrated them into \texttt{distributions\_master.json}, which
parameterizes our synthetic patient generator. Synthetic distributions were
validated against real distributions using two-sample Kolmogorov-Smirnov
tests (Section~\ref{sec:calibration_validation}).
```

---

## Sources

- [Miltiadous et al. 2023 — ds004504 paper (MDPI)](https://www.mdpi.com/2306-5729/8/6/95)
- [Henao Isaza et al. 2026 — ds007427 paper (PLOS ONE)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0343722)
- [ds006095 — Mind in Motion (OpenNeuro)](https://openneuro.org/datasets/ds006095)
- [Pliner et al. 2022 — Uneven terrain (PLOS ONE)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0278646)
- [Dzianok & Kublik 2024 — PEARL-Neuro (Scientific Data)](https://www.nature.com/articles/s41597-024-03106-5)
- [George et al. 2013 — ds002778 (NeuroImage Clinical)](https://www.sciencedirect.com/science/article/pii/S2213158213000867)
- [ds002778 OpenNeuro page](https://openneuro.org/datasets/ds002778)
