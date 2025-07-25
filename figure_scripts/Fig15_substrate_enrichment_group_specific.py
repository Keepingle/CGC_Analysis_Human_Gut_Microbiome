import pandas as pd

# File paths
con_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/instrainCONscaffold_info_cleaned__RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict_length.tsv"
db_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/instrainDBscaffold_info_cleaned__RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict_length.tsv"

# Load data
df_con = pd.read_csv(con_path, sep="\t")
df_db = pd.read_csv(db_path, sep="\t")

# Count unique scaffolds
scaffold_count_con = df_con["scaffold"].nunique()
scaffold_count_db = df_db["scaffold"].nunique()

# Print results
print(f"Healthy (CON) unique scaffold count: {scaffold_count_con}")
print(f"Obese (DB) unique scaffold count: {scaffold_count_db}")

import pandas as pd

# File paths
con_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/instrainCONscaffold_info_cleaned__RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict_length.tsv"
db_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/instrainDBscaffold_info_cleaned__RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict_length.tsv"


# Load data
df_con = pd.read_csv(con_path, sep="\t")
df_db = pd.read_csv(db_path, sep="\t")

# Filter for RPKM >= 1
df_con_filtered = df_con[df_con["RPKM"] >= 1]
df_db_filtered = df_db[df_db["RPKM"] >= 1]

# Count unique scaffolds after filtering
scaffold_count_con = df_con_filtered["scaffold"].nunique()
scaffold_count_db = df_db_filtered["scaffold"].nunique()

# Print results
print(f"Healthy (CON) unique scaffold count (RPKM ≥ 1): {scaffold_count_con}")
print(f"Obese (DB) unique scaffold count (RPKM ≥ 1): {scaffold_count_db}")

import pandas as pd

# File paths
con_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainCONscaffold_info_cleaned.tsv"
db_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainDBscaffold_info_cleaned.tsv"

# Load data
df_con = pd.read_csv(con_path, sep="\t")
df_db = pd.read_csv(db_path, sep="\t")

# Filter for RPKM ≥ 1
df_con_filtered = df_con[df_con["RPKM"] >= 1]
df_db_filtered = df_db[df_db["RPKM"] >= 1]

# Get sets of unique scaffolds
scaffolds_con = set(df_con_filtered["scaffold"].unique())
scaffolds_db = set(df_db_filtered["scaffold"].unique())

# Compare
shared_scaffolds = scaffolds_con & scaffolds_db
unique_con = scaffolds_con - scaffolds_db
unique_db = scaffolds_db - scaffolds_con

# Print results
print(f"Healthy (CON) unique scaffold count (RPKM ≥ 1): {len(scaffolds_con)}")
print(f"Obese (DB) unique scaffold count (RPKM ≥ 1): {len(scaffolds_db)}")
print(f"Shared scaffolds: {len(shared_scaffolds)}")
print(f"Unique to CON: {len(unique_con)}")
print(f"Unique to DB: {len(unique_db)}")

# Save unique scaffolds to files
unique_con_df = df_con_filtered[df_con_filtered["scaffold"].isin(unique_con)]
unique_db_df = df_db_filtered[df_db_filtered["scaffold"].isin(unique_db)]

# Output as TSV files
unique_con_df.to_csv("/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/unique_scaffolds_CON.tsv", sep="\t", index=False)
unique_db_df.to_csv("/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/unique_scaffolds_DB.tsv", sep="\t", index=False)

print("Saved:")
print(" - unique_scaffolds_CON.tsv")
print(" - unique_scaffolds_DB.tsv")

import pandas as pd
import matplotlib.pyplot as plt

# File paths
con_file = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/unique_scaffolds_CON.tsv"
db_file = "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/unique_scaffolds_DB.tsv"

# Load data
df_con = pd.read_csv(con_file, sep="\t")
df_db = pd.read_csv(db_file, sep="\t")

# Count substrate frequencies
substrate_con = df_con["substrate"].value_counts().sort_index()
substrate_db = df_db["substrate"].value_counts().sort_index()

# Combine into one DataFrame
substrate_df = pd.DataFrame({
    "Healthy (CON)": substrate_con,
    "Obese (DB)": substrate_db
}).fillna(0).astype(int)

# Print table
print(substrate_df)

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import fisher_exact
import seaborn as sns
import numpy as np

# Load unique scaffold files
df_con = pd.read_csv("/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/unique_scaffolds_CON.tsv", sep="\t")
df_db = pd.read_csv("/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/unique_scaffolds_DB.tsv", sep="\t")

# Count substrate frequencies
substrate_con = df_con["substrate"].value_counts()
substrate_db = df_db["substrate"].value_counts()

# Combine into a single DataFrame
substrate_df = pd.DataFrame({
    "Healthy (CON)": substrate_con,
    "Obese (DB)": substrate_db
}).fillna(0).astype(int)

# Total counts for reference
total_con = substrate_df["Healthy (CON)"].sum()
total_db = substrate_df["Obese (DB)"].sum()

# Fisher’s exact test
results = []
for substrate in substrate_df.index:
    a = substrate_df.loc[substrate, "Obese (DB)"]
    b = total_db - a
    c = substrate_df.loc[substrate, "Healthy (CON)"]
    d = total_con - c
    table = [[a, b], [c, d]]
    oddsratio, pval = fisher_exact(table)
    enriched_in = "Obese" if a / total_db > c / total_con else "Healthy"
    results.append((substrate, a, c, pval, enriched_in))

# Convert results to DataFrame
results_df = pd.DataFrame(results, columns=["Substrate", "Obese_count", "Healthy_count", "p_value", "Enriched_in"])
results_df["-log10(p)"] = -np.log10(results_df["p_value"])

# Show results
print(results_df.sort_values("p_value"))

# --- Plot bar chart with enrichment annotation ---
plt.figure(figsize=(10, 6))
substrate_df.plot(kind="bar", stacked=False, figsize=(12, 6), alpha=0.8)
plt.ylabel("Count of Unique Scaffolds (RPKM ≥ 1)")
plt.title("Substrate Distribution in Healthy vs Obese")
plt.xticks(rotation=45, ha='right')

# Annotate enrichment on top
for i, row in results_df.iterrows():
    substrate = row["Substrate"]
    if row["p_value"] < 0.05:
        idx = list(substrate_df.index).index(substrate)
        max_val = max(row["Obese_count"], row["Healthy_count"])
        plt.text(idx, max_val + 1, f'*{row["Enriched_in"]}', ha='center', fontsize=9, color='red')

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Convert p-values to float and calculate -log10(p-value)
results_df["p_value"] = results_df["p_value"].astype(float)
results_df["-log10(p)"] = -np.log10(results_df["p_value"])

# Define significance markers
def sig_marker(p):
    if p < 0.05:
        return "*"
    elif p < 0.1:
        return "."
    else:
        return ""

results_df["Significance"] = results_df["p_value"].apply(sig_marker)

# Sort by significance (descending)
results_df_sorted = results_df.sort_values("-log10(p)", ascending=False)

# Plot the enrichment results
plt.figure(figsize=(12, 6))
barplot = sns.barplot(
    data=results_df_sorted,
    x="-log10(p)",
    y="Substrate",
    hue="Enriched_in",
    palette={"Obese": "#d95f02", "Healthy": "#1b9e77"},
    dodge=False
)

# Add significance markers next to bars
for i, row in results_df_sorted.iterrows():
    if row["Significance"]:
        barplot.text(
            row["-log10(p)"] + 0.02,
            i,
            row["Significance"],
            color='black',
            ha='left',
            va='center',
            fontsize=12,
            fontweight='bold'
        )

# Add threshold lines for p-value cutoffs
plt.axvline(-np.log10(0.05), linestyle="--", color="gray", label="p = 0.05")
plt.axvline(-np.log10(0.1), linestyle="--", color="lightgray", label="p = 0.1")

plt.xlabel("-log10(p-value)")
plt.title("Substrate Enrichment Significance")
plt.legend(title="Enriched in", loc="lower right")
plt.tight_layout()

# Save plot (optional)
plt.savefig("Fig15_substrate_enrichment_significance.pdf", bbox_inches="tight")
plt.show()

