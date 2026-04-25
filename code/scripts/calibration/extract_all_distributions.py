"""提取所有 OpenNeuro 数据集的真实分布到 distributions.json
用于校准 AD 项目的合成数据生成器
"""

import pandas as pd
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "output" / "distributions_master.json"
OUT.parent.mkdir(exist_ok=True)


def safe_stats(series):
    """安全的描述统计 (忽略 NaN)"""
    s = series.dropna()
    if len(s) == 0:
        return None
    return {
        "n": int(len(s)),
        "mean": float(s.mean()),
        "sd": float(s.std()),
        "min": float(s.min()),
        "max": float(s.max()),
        "q25": float(s.quantile(0.25)),
        "q50": float(s.quantile(0.50)),
        "q75": float(s.quantile(0.75)),
    }


def gender_breakdown(series):
    return series.value_counts().to_dict() if not series.empty else {}


# ── 容器 ──
master = {
    "_meta": {
        "purpose": "校准 AD 项目合成数据生成器, 使合成患者分布像真实患者",
        "created": "2026-04-25",
    },
    "datasets": {}
}


# ============================================================
# ds004504 — EEG AD/FTD/Healthy 88 人
# ============================================================
print("\n[1/5] ds004504...")
try:
    df = pd.read_csv(DATA / "ds004504" / "participants.tsv", sep="\t")
    GROUP_MAP = {"A": "ad", "F": "ftd", "C": "ctrl"}
    df["stage"] = df["Group"].map(GROUP_MAP)

    ds = {"source_paper": "Miltiadous et al. 2023, MDPI Data 8(6):95",
          "doi": "10.18112/openneuro.ds004504",
          "modality": "EEG (19ch, 500Hz, eyes-closed)",
          "n_total": int(len(df)),
          "groups": {}}

    for stage, gdf in df.groupby("stage"):
        ds["groups"][stage] = {
            "n": int(len(gdf)),
            "age": safe_stats(gdf["Age"]),
            "mmse": safe_stats(gdf["MMSE"]),
            "gender": gender_breakdown(gdf["Gender"]),
        }
    master["datasets"]["ds004504"] = ds
    print(f"  ✓ {ds['n_total']} 人, 组: {list(ds['groups'].keys())}")
except Exception as e:
    print(f"  ✗ {e}")


# ============================================================
# ds007427 — AD/MCI/Control + MMSE (Colombia 团队)
# ============================================================
print("\n[2/5] ds007427 (Lopera 团队 AD/MCI/CTR)...")
try:
    df = pd.read_csv(DATA / "ds007427" / "participants.tsv", sep="\t")

    # 从 ID 前缀提取分组
    def parse_group(pid):
        m = re.match(r"sub-([A-Z]+)\d+", pid)
        if m:
            return m.group(1)
        return "?"
    df["group_code"] = df["participant_id"].apply(parse_group)

    GROUP_MAP_ES = {
        "CTR": "ctrl",
        "DCL": "mci",       # Deterioro Cognitivo Leve = MCI
        "DTA": "ad",        # Demencia Tipo Alzheimer = AD
        "G":   "at_risk",   # 基因风险组 (PSEN1 携带者?)
    }
    df["stage"] = df["group_code"].map(GROUP_MAP_ES)

    ds = {"source_paper": "Henao Isaza et al. 2026, PLOS ONE",
          "doi": "10.18112/openneuro.ds007427",
          "modality": "EEG",
          "note": "Colombia paisa 队列, 含 E280A PSEN1 家族性 AD 携带者",
          "n_total": int(len(df)),
          "groups": {}}

    for stage, gdf in df.groupby("stage"):
        if stage is None:
            continue
        gstats = {
            "n": int(len(gdf)),
            "age": safe_stats(gdf["age"]),
            "education": safe_stats(gdf["education"]),
            "gender": gender_breakdown(gdf["sex"]),
        }
        # MMSE 总分
        if "MM_total" in gdf.columns:
            gstats["mmse_total"] = safe_stats(gdf["MM_total"])
        # MMSE 子项
        for sub in ["MM_Tiempo", "MM_espac", "MM_fijac", "MM_atenc", "MM_evoc", "MM_leng"]:
            if sub in gdf.columns:
                gstats[sub] = safe_stats(gdf[sub])
        # 命名测试
        if "Denom_total" in gdf.columns:
            gstats["naming_total"] = safe_stats(gdf["Denom_total"])
        ds["groups"][stage] = gstats

    master["datasets"]["ds007427"] = ds
    print(f"  ✓ {ds['n_total']} 人, 组: {list(ds['groups'].keys())}")
except Exception as e:
    print(f"  ✗ {e}")


# ============================================================
# ds006095 — 老年人 EEG+IMU+认知 (★ 关键数据集)
# ============================================================
print("\n[3/5] ds006095 (老年人 EEG+EMG+IMU+步行+MOCA)...")
try:
    df = pd.read_csv(DATA / "ds006095" / "participants.tsv", sep="\t")

    ds = {"source": "Mind in Motion Older Adults Walking Over Uneven Terrain",
          "doi": "10.18112/openneuro.ds006095",
          "modality": "高密度 EEG + 颈 EMG + IMU + 地面反力 + 不平地形步行任务",
          "note": "★ 对项目最直接相关 — 含 IMU + MOCA, 用于校准老年 IMU 步态 baseline",
          "n_total": int(len(df)),
          "all_subjects_aggregated": {
              "age": safe_stats(df["age"]),
              "moca": safe_stats(df["MOCA"]),
              "sppb": safe_stats(df["SPPB"]),  # 简短身体表现成套测试
              "time_400m_seconds": safe_stats(df["time_400m_seconds"]),
              "treadmill_speed": safe_stats(df["treadmill_speed"]),
              "gender": gender_breakdown(df["sex"]),
          },
          "moca_distribution": {
              "normal_>=26": int((df["MOCA"] >= 26).sum()),
              "mild_22to25": int(((df["MOCA"] >= 22) & (df["MOCA"] < 26)).sum()),
              "moderate_<22": int((df["MOCA"] < 22).sum()),
          },
          }
    master["datasets"]["ds006095"] = ds
    print(f"  ✓ {ds['n_total']} 老年人, MOCA μ={ds['all_subjects_aggregated']['moca']['mean']:.1f}")
except Exception as e:
    print(f"  ✗ {e}")


# ============================================================
# ds004796 — PEARL-Neuro 中年痴呆风险 (Polish, 完整 phenotyping)
# ============================================================
print("\n[4/5] ds004796 (PEARL-Neuro 中年痴呆风险队列)...")
try:
    df = pd.read_csv(DATA / "ds004796" / "participants.tsv", sep="\t")

    ds = {"source": "Dzianok & Kublik 2024, Sci Data 11:276",
          "doi": "10.18112/openneuro.ds004796",
          "modality": "EEG + fMRI + 完整生活方式问卷 + 血液生化 + APOE 基因",
          "note": "中年 50-60 岁, 痴呆风险但未发病. 用于 SCD/早期建模",
          "n_total": int(len(df)),
          "phenotypes_available": list(df.columns),
          "key_distributions": {
              "age": safe_stats(df["age"]),
              "education": safe_stats(df["education"]),
              "BMI": safe_stats(df["BMI"]),
              "BDI_depression": safe_stats(df["BDI"]),
              "NEO_NEU": safe_stats(df["NEO_NEU"]),
              "NEO_EXT": safe_stats(df["NEO_EXT"]),
              "RPM_raven_matrices": safe_stats(df["RPM"]),
              "AUDIT_alcohol": safe_stats(df["AUDIT"]),
              "CVLT_1": safe_stats(df["CVLT_1"]),  # 言语学习首次回忆
              "CVLT_5": safe_stats(df["CVLT_5"]),  # 第 5 次学习
          },
          "apoe_haplotype_distribution": gender_breakdown(df["APOE_haplotype"]),
          }
    master["datasets"]["ds004796"] = ds
    print(f"  ✓ {ds['n_total']} 中年人, age μ={ds['key_distributions']['age']['mean']:.1f}")
except Exception as e:
    print(f"  ✗ {e}")


# ============================================================
# ds002778 — UC San Diego PD vs Healthy (差异诊断)
# ============================================================
print("\n[5/5] ds002778 (PD vs Healthy 差异诊断)...")
try:
    df = pd.read_csv(DATA / "ds002778" / "participants.tsv", sep="\t")

    # 从 ID 提取分组 (hc/pd)
    df["stage"] = df["participant_id"].apply(
        lambda x: "pd" if "pd" in x else "ctrl" if "hc" in x else "?"
    )

    ds = {"source": "UC San Diego, Rockhill et al.",
          "doi": "10.18112/openneuro.ds002778",
          "modality": "Resting state EEG",
          "note": "★ 用于 AD 与 PD 差异诊断 EEG 标志物对照",
          "n_total": int(len(df)),
          "groups": {}}

    # MMSE 列名空格不一致, 找出来
    mmse_col = next((c for c in df.columns if "MMSE" in c.upper()), None)

    for stage, gdf in df.groupby("stage"):
        gstats = {
            "n": int(len(gdf)),
            "age": safe_stats(gdf["age"]),
            "gender": gender_breakdown(gdf["gender"]),
        }
        if mmse_col:
            gstats["mmse"] = safe_stats(pd.to_numeric(gdf[mmse_col], errors="coerce"))
        ds["groups"][stage] = gstats

    master["datasets"]["ds002778"] = ds
    print(f"  ✓ {ds['n_total']} 人, 组: {list(ds['groups'].keys())}")
except Exception as e:
    print(f"  ✗ {e}")


# ============================================================
# 汇总: 综合 MMSE 分期映射 (跨 ds004504 + ds007427)
# ============================================================
print("\n[Summary] 跨数据集综合 MMSE 分期映射...")

ad_combined_n = 0; ad_combined_mmse_sum = 0; ad_combined_mmse_sumsq = 0
mci_combined_n = 0; mci_combined_mmse_sum = 0; mci_combined_mmse_sumsq = 0
ctrl_combined_n = 0; ctrl_combined_mmse_sum = 0; ctrl_combined_mmse_sumsq = 0

for ds_id in ["ds004504", "ds007427"]:
    ds = master["datasets"].get(ds_id, {})
    grps = ds.get("groups", {})
    for stage_label in ["ad", "mci", "ftd", "ctrl"]:
        g = grps.get(stage_label, {})
        mmse_field = "mmse" if "mmse" in g else "mmse_total" if "mmse_total" in g else None
        if not mmse_field or g.get(mmse_field) is None:
            continue
        m = g[mmse_field]
        n, mu, sd = m["n"], m["mean"], m["sd"]
        if stage_label == "ad":
            ad_combined_n += n
            ad_combined_mmse_sum += mu * n
            ad_combined_mmse_sumsq += (sd**2 + mu**2) * n
        elif stage_label in ("mci", "ftd"):  # FTD 当 MCI 代理
            mci_combined_n += n
            mci_combined_mmse_sum += mu * n
            mci_combined_mmse_sumsq += (sd**2 + mu**2) * n
        elif stage_label == "ctrl":
            ctrl_combined_n += n
            ctrl_combined_mmse_sum += mu * n
            ctrl_combined_mmse_sumsq += (sd**2 + mu**2) * n


def combine(n, sum_, sumsq):
    if n == 0:
        return None
    mean = sum_ / n
    var = sumsq / n - mean**2
    sd = max(var, 0) ** 0.5
    return {"n": n, "mean": round(mean, 2), "sd": round(sd, 2)}


master["combined_mmse_distribution"] = {
    "ad":   combine(ad_combined_n,   ad_combined_mmse_sum,   ad_combined_mmse_sumsq),
    "mci":  combine(mci_combined_n,  mci_combined_mmse_sum,  mci_combined_mmse_sumsq),
    "ctrl": combine(ctrl_combined_n, ctrl_combined_mmse_sum, ctrl_combined_mmse_sumsq),
    "note": "FTD 并入 MCI 桶作为'中度认知障碍'代理 (因 FTD 在量表上常处中间区)",
    "sources": ["ds004504", "ds007427"],
}

# 写出
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print(f"\n✓ 主分布文件: {OUT}")
print(f"   写入 {len(master['datasets'])} 个数据集")

print("\n" + "=" * 60)
print("综合 MMSE 分布 (跨 ds004504 + ds007427)")
print("=" * 60)
for stage in ["ctrl", "mci", "ad"]:
    s = master["combined_mmse_distribution"][stage]
    if s:
        print(f"  {stage:5s}: n={s['n']:3d}, MMSE μ={s['mean']:.2f}, σ={s['sd']:.2f}")

print("\n" + "=" * 60)
print("生成器 v2 用法")
print("=" * 60)
ad = master["combined_mmse_distribution"]["ad"]
mci = master["combined_mmse_distribution"]["mci"]
ctrl = master["combined_mmse_distribution"]["ctrl"]
print(f'''
# data/baseline 4.8/generate_synthetic_temporal.py 内
def progression_to_mmse(p, age, edu):
    """progression ∈ [0,1] → MMSE 分数
    基于 ds004504 + ds007427 联合 (n={ad['n']+mci['n']+ctrl['n'] if (ad and mci and ctrl) else 'N/A'} 真实患者)
    """
    if p < 0.3:    target_mu, target_sd = {ctrl['mean']:.2f}, {ctrl['sd']:.2f}  # ctrl
    elif p < 0.7:  target_mu, target_sd = {mci['mean']:.2f}, {mci['sd']:.2f}    # mci
    else:          target_mu, target_sd = {ad['mean']:.2f}, {ad['sd']:.2f}     # ad

    score = np.random.normal(target_mu, target_sd)
    score += 0.05 * (edu - 12)
    return np.clip(score, 0, 30)
''')
