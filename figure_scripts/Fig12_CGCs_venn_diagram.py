import pandas as pd

# File paths
con_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainCONscaffold_info_cleaned.tsv"
db_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainDBscaffold_info_cleaned.tsv"

# Load datasets
df_con = pd.read_csv(con_path, sep="\t")
df_db = pd.read_csv(db_path, sep="\t")

# Identify unique scaffolds in each dataset
scaffold_con = set(df_con["scaffold"].unique())
scaffold_db = set(df_db["scaffold"].unique())

unique_con = scaffold_con - scaffold_db
unique_db = scaffold_db - scaffold_con

# Extract data corresponding to unique scaffolds
unique_con_df = df_con[df_con["scaffold"].isin(unique_con)]
unique_db_df = df_db[df_db["scaffold"].isin(unique_db)]

# Apply RPKM filtering
RPKM_threshold = 1  # Adjust threshold as necessary

filtered_unique_con_df = unique_con_df[unique_con_df["RPKM"] >= RPKM_threshold]
filtered_unique_db_df = unique_db_df[unique_db_df["RPKM"] >= RPKM_threshold]

# Save filtered data to files
filtered_unique_con_df.to_csv("/work/yinlab/yixing/CGC78/Final_analysis/out/filtered_unique_CON_scaffold.tsv", sep="\t", index=False)
filtered_unique_db_df.to_csv("/work/yinlab/yixing/CGC78/Final_analysis/out/filtered_unique_DB_scaffold.tsv", sep="\t", index=False)

# Print summary
print(f"Unique CON scaffolds (RPKM ≥ {RPKM_threshold}): {filtered_unique_con_df.shape[0]}")
print(f"Unique DB scaffolds (RPKM ≥ {RPKM_threshold}): {filtered_unique_db_df.shape[0]}")

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn2

# Define consistent color mapping
color_mapping = {"CON": "#1b9e77", "DB": "#d95f02"}

# Ensure copies to avoid warnings
filtered_unique_con_df = filtered_unique_con_df.copy()
filtered_unique_con_df["Group"] = "CON"

filtered_unique_db_df = filtered_unique_db_df.copy()
filtered_unique_db_df["Group"] = "DB"

combined_df = pd.concat([filtered_unique_con_df, filtered_unique_db_df])

# --------------------------------------------
# 1. Venn Diagram: Shared vs Unique Scaffolds
# --------------------------------------------
plt.figure(figsize=(6, 6))
venn = venn2(
    subsets=[scaffold_con, scaffold_db],
    set_labels=('CON (Healthy)', 'DB (Obese)'),
    set_colors=(color_mapping["CON"], color_mapping["DB"]),
    alpha=0.7
)
plt.title("Unique and Shared CGC Scaffolds")
plt.show()
