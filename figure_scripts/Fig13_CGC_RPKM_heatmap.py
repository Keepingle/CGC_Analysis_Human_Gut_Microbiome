import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==== Step 1: Load Data ====
con_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/instrainCONscaffold_info_cleaned__RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict_length.tsv"
db_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/instrainDBscaffold_info_cleaned__RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict_length.tsv"

con_df = pd.read_csv(con_path, sep='\t')
db_df = pd.read_csv(db_path, sep='\t')

# ==== Step 2: Add Group and Merge ====
con_df["Group"] = "Healthy"
db_df["Group"] = "Obese"
merged_df = pd.concat([con_df, db_df], ignore_index=True)

# ==== Step 3: Compute log(RPKM) ====
merged_df["log_RPKM"] = np.log1p(merged_df["RPKM"])

# ==== Step 4: Pivot Heatmap Matrix ====
heatmap_data = merged_df.pivot_table(index="sample_id", columns="scaffold", values="log_RPKM", fill_value=0)

# ==== Step 5: Determine Shared & Unique CGCs ====
sample_groups = merged_df[["sample_id", "Group"]].drop_duplicates().set_index("sample_id")
heatmap_data = heatmap_data.loc[sample_groups.index]

obese_samples = sample_groups[sample_groups["Group"] == "Obese"].index.tolist()
healthy_samples = sample_groups[sample_groups["Group"] == "Healthy"].index.tolist()

scaffold_presence = pd.DataFrame({
    "in_obese": (heatmap_data.loc[obese_samples] > 0).any(),
    "in_healthy": (heatmap_data.loc[healthy_samples] > 0).any()
})

def classify_scaffold(row):
    if row["in_obese"] and row["in_healthy"]:
        return "Shared"
    elif row["in_obese"]:
        return "Obese Unique"
    elif row["in_healthy"]:
        return "Healthy Unique"
    else:
        return "Absent"

scaffold_presence["Group"] = scaffold_presence.apply(classify_scaffold, axis=1)

# ==== Step 6: Sort CGCs ====
scaffold_means = heatmap_data.mean(axis=0)
shared_sorted = sorted(scaffold_presence[scaffold_presence["Group"] == "Shared"].index.tolist(), key=lambda x: -scaffold_means[x])
obese_sorted = sorted(scaffold_presence[scaffold_presence["Group"] == "Obese Unique"].index.tolist(), key=lambda x: -scaffold_means[x])
healthy_sorted = sorted(scaffold_presence[scaffold_presence["Group"] == "Healthy Unique"].index.tolist(), key=lambda x: -scaffold_means[x])

sorted_columns = shared_sorted + obese_sorted + healthy_sorted
heatmap_data = heatmap_data[sorted_columns]

# ==== Step 7: Sort samples (Obese on top) ====
heatmap_data = heatmap_data.loc[obese_samples + healthy_samples]

# ==== Step 8: Plot Heatmap with Vertical Annotations ====
plt.figure(figsize=(18, 6))
sns.heatmap(
    heatmap_data,
    cmap="Blues",
    cbar_kws={"label": "log(RPKM + 1)"},
    xticklabels=False,
    yticklabels=False
)

# Obese / Healthy sample group labels on Y-axis
obese_mid = len(obese_samples) / 2
healthy_mid = len(obese_samples) + len(healthy_samples) / 2
plt.text(-2, obese_mid, "Obese", va="center", ha="right", fontsize=12, fontweight="bold")
plt.text(-2, healthy_mid, "Healthy", va="center", ha="right", fontsize=12, fontweight="bold")

# Column breaks
shared_len = len(shared_sorted)
obese_len = len(obese_sorted)
healthy_len = len(healthy_sorted)

# Draw vertical dashed lines to separate groups
plt.axvline(shared_len, color='black', linestyle='--', linewidth=1.2)
plt.axvline(shared_len + obese_len, color='black', linestyle='--', linewidth=1.2)

# Add text labels above the regions
plt.text(shared_len / 2, -1.5, "Shared", ha="center", fontsize=12, fontweight="bold")
plt.text(shared_len + obese_len / 2, -1.5, "Obese Unique", ha="center", fontsize=12, fontweight="bold")
plt.text(shared_len + obese_len + healthy_len / 2, -1.5, "Healthy Unique", ha="center", fontsize=12, fontweight="bold")

# Axes
plt.xlabel("CGC Scaffolds")
plt.ylabel("Samples")
plt.tight_layout()
plt.show()
