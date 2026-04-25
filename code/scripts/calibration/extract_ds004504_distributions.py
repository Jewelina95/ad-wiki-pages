"""从 ds004504 提取真实分布到 distributions.json
- 来源: OpenNeuro ds004504 (88 人: 36 AD + 23 FTD + 29 Healthy)
- 输出: 分组的 (年龄, MMSE) 联合分布
"""

import pandas as pd
import json
from pathlib import Path

# 路径
ROOT = Path(__file__).resolve().parent.parent
PARTICIPANTS_TSV = ROOT / "data" / "ds004504" / "participants.tsv"
OUT = ROOT / "output" / "distributions_ds004504.json"

# 读取
df = pd.read_csv(PARTICIPANTS_TSV, sep="\t")

# 分组映射 (按 Data Descriptor: A=AD, F=FTD, C=Control)
GROUP_MAP = {"A": "ad", "F": "ftd", "C": "ctrl"}
df["stage"] = df["Group"].map(GROUP_MAP)

# 计算每组的 (Age, MMSE) 统计
stats = {}
for stage_label, group_df in df.groupby("stage"):
    stats[stage_label] = {
        "n": int(len(group_df)),
        "age": {
            "mean": float(group_df["Age"].mean()),
            "sd":   float(group_df["Age"].std()),
            "min":  float(group_df["Age"].min()),
            "max":  float(group_df["Age"].max()),
        },
        "mmse": {
            "mean": float(group_df["MMSE"].mean()),
            "sd":   float(group_df["MMSE"].std()),
            "min":  float(group_df["MMSE"].min()),
            "max":  float(group_df["MMSE"].max()),
            "q25":  float(group_df["MMSE"].quantile(0.25)),
            "q50":  float(group_df["MMSE"].quantile(0.50)),
            "q75":  float(group_df["MMSE"].quantile(0.75)),
        },
        "gender": group_df["Gender"].value_counts().to_dict(),
    }

# 写入
distributions = {
    "source": "OpenNeuro ds004504",
    "doi": "https://doi.org/10.18112/openneuro.ds004504",
    "paper": "Miltiadous et al. 2023, MDPI Data 8(6):95",
    "n_total": int(len(df)),
    "groups": stats,
    "use_in_generator": {
        "purpose": "标定生成器输出 MMSE 分数, 让合成患者的认知评估分布像真实患者",
        "usage": "progression_to_mmse() 函数读这个 JSON 的 mmse.mean / mmse.sd",
    },
}

OUT.parent.mkdir(exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(distributions, f, ensure_ascii=False, indent=2)

# 打印验证
print(f"✓ 写入: {OUT}")
print()
print(f"总人数: {len(df)}")
print()
print("分组统计:")
for stage, s in stats.items():
    print(f"  [{stage}] n={s['n']}")
    print(f"    Age:  μ={s['age']['mean']:.1f} σ={s['age']['sd']:.1f}")
    print(f"    MMSE: μ={s['mmse']['mean']:.2f} σ={s['mmse']['sd']:.2f}  (median={s['mmse']['q50']:.0f})")
    print(f"    Gender: {s['gender']}")
    print()

# 给出"分期-MMSE"映射建议
print("=" * 50)
print("建议在 generate_synthetic_temporal.py 用法:")
print("=" * 50)
print(f'''
def progression_to_mmse(p, age, edu):
    """progression ∈ [0,1] → MMSE 分数 (基于 ds004504 真实分布)
    p<0.3 偏向健康, 0.3-0.7 偏向 FTD/MCI, p>0.7 偏向 AD
    """
    if p < 0.3:
        # ctrl: μ={stats['ctrl']['mmse']['mean']:.1f} σ={stats['ctrl']['mmse']['sd']:.1f}
        target_mean, target_sd = {stats['ctrl']['mmse']['mean']:.2f}, {stats['ctrl']['mmse']['sd']:.2f}
    elif p < 0.7:
        # ftd/mci 代理: μ={stats['ftd']['mmse']['mean']:.1f} σ={stats['ftd']['mmse']['sd']:.1f}
        target_mean, target_sd = {stats['ftd']['mmse']['mean']:.2f}, {stats['ftd']['mmse']['sd']:.2f}
    else:
        # ad: μ={stats['ad']['mmse']['mean']:.1f} σ={stats['ad']['mmse']['sd']:.1f}
        target_mean, target_sd = {stats['ad']['mmse']['mean']:.2f}, {stats['ad']['mmse']['sd']:.2f}

    score = np.random.normal(target_mean, target_sd)
    score += 0.05 * (edu - 12)  # 教育修正
    return np.clip(score, 0, 30)
''')
