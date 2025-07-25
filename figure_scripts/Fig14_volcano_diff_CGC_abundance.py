import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from matplotlib.lines import Line2D

# === Step 1: Load cleaned input files ===
obese_file = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/instrainDBscaffold_info_cleaned__RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict_length.tsv"
healthy_file = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/instrainCONscaffold_info_cleaned__RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict_length.tsv"

df_obese = pd.read_csv(obese_file, sep="\t")
df_healthy = pd.read_csv(healthy_file, sep="\t")

# === Step 2: Identify CGCs (scaffolds) common to both groups ===
obese_cgcs = set(df_obese["scaffold"].unique())
healthy_cgcs = set(df_healthy["scaffold"].unique())
common_cgcs = obese_cgcs & healthy_cgcs

# === Step 3: Filter both groups to only common CGCs ===
df_obese_common = df_obese[df_obese["scaffold"].isin(common_cgcs)]
df_healthy_common = df_healthy[df_healthy["scaffold"].isin(common_cgcs)]

# === Step 4: Perform Mann–Whitney U test on each common scaffold ===
results = []
for scaffold in sorted(common_cgcs):
    obese_vals = df_obese_common[df_obese_common["scaffold"] == scaffold]["RPKM"]
    healthy_vals = df_healthy_common[df_healthy_common["scaffold"] == scaffold]["RPKM"]
    
    if len(obese_vals) >= 3 and len(healthy_vals) >= 3:
        stat, p = mannwhitneyu(obese_vals, healthy_vals, alternative="two-sided")
        results.append({
            "scaffold": scaffold,
            "obese_mean": obese_vals.mean(),
            "healthy_mean": healthy_vals.mean(),
            "p_value": p
        })

# === Step 5: Compile results and calculate additional metrics ===
df_stats = pd.DataFrame(results)
df_stats["p_value_adj"] = df_stats["p_value"] * len(df_stats)  # Bonferroni correction

# Compute log2 fold change
df_stats["log2_FC"] = np.log2(df_stats["healthy_mean"] + 1e-6) - np.log2(df_stats["obese_mean"] + 1e-6)
df_stats["neg_log10_p"] = -np.log10(df_stats["p_value"] + 1e-10)
df_stats = df_stats.sort_values("p_value")

# === Step 6: Annotate significance and enrichment group ===
p_threshold = 0.05
fc_threshold = 1  # log2 fold change ≥ 1 or ≤ -1 (2-fold)

df_stats["significant"] = (df_stats["p_value"] < p_threshold) & (abs(df_stats["log2_FC"]) >= fc_threshold)

# 👇 This is the corrected enrichment group logic
def assign_enrichment(row):
    if row["p_value"] < p_threshold and row["log2_FC"] >= fc_threshold:
        return "Healthy"
    elif row["p_value"] < p_threshold and row["log2_FC"] <= -fc_threshold:
        return "Obese"
    else:
        return "None"

df_stats["enriched_group"] = df_stats.apply(assign_enrichment, axis=1)

# Save full and significant results
df_stats.to_csv("common_cgc_rpkm_diff_analysis_log2FC_with_group.tsv", sep="\t", index=False)
df_significant = df_stats[df_stats["significant"]]
df_significant.to_csv("significant_cgc_log2FC_filtered_with_group.tsv", sep="\t", index=False)

# === Step 6.5: Count and display summary ===
total = len(df_stats)
n_healthy = (df_stats["enriched_group"] == "Healthy").sum()
n_obese = (df_stats["enriched_group"] == "Obese").sum()
n_not_significant = total - (n_healthy + n_obese)

pct_healthy = n_healthy / total * 100
pct_obese = n_obese / total * 100
pct_not_significant = n_not_significant / total * 100

print(f"Total CGCs: {total}")
print(f"Healthy enriched (p < 0.05 & log2FC > 1): {n_healthy} ({pct_healthy:.2f}%)")
print(f"Obese enriched (p < 0.05 & log2FC < -1): {n_obese} ({pct_obese:.2f}%)")
print(f"Not significant: {n_not_significant} ({pct_not_significant:.2f}%)")

# === Step 7: Volcano plot ===
plt.figure(figsize=(7, 5))

color_map = {
    "Healthy": "#D73027",
    "Obese": "#4575B4",
    "None": "gray"
}
colors = df_stats["enriched_group"].map(color_map)

plt.scatter(
    df_stats["log2_FC"],
    df_stats["neg_log10_p"],
    c=colors,
    alpha=0.8,
    edgecolor="black",
    linewidth=0.5
)

# Threshold lines
plt.axhline(-np.log10(p_threshold), color="black", linestyle="--", linewidth=1)
plt.axvline(fc_threshold, color="black", linestyle="--", linewidth=1)
plt.axvline(-fc_threshold, color="black", linestyle="--", linewidth=1)

# Threshold labels
plt.text(fc_threshold + 0.05, 2.2, "+1", fontsize=9, fontweight="bold", color="black")
plt.text(-fc_threshold - 0.25, 2.2, "-1", fontsize=9, fontweight="bold", color="black")
plt.text(1.7, -np.log10(p_threshold) + 0.1, "p = 0.05", fontsize=9, fontweight="bold", color="black")

# Axis labels and title
plt.xlabel("log2 Fold Change (Healthy - Obese)", fontsize=11)
plt.ylabel("-log10(p-value)", fontsize=11)
plt.title("Volcano Plot of Differential CGC Abundance", fontsize=13)

# Legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Healthy enriched', markerfacecolor=color_map["Healthy"], markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Obese enriched', markerfacecolor=color_map["Obese"], markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Not significant', markerfacecolor=color_map["None"], markersize=8)
]
plt.legend(handles=legend_elements, loc='upper right', frameon=True)

# Show/save
plt.tight_layout()
# plt.savefig("volcano_log2FC_CGCs.png", dpi=300)
plt.show()
