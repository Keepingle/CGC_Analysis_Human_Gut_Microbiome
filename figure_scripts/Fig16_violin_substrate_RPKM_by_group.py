import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import mannwhitneyu

# Load data
df_con = pd.read_csv(
    "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/unique_scaffolds_CON.tsv", sep="\t"
)
df_db = pd.read_csv(
    "/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/unique_scaffolds_DB.tsv", sep="\t"
)


# Optional: Filter substrates with enough data points (samples)
substrate_counts = df_sum["substrate"].value_counts()
selected_substrates = substrate_counts[substrate_counts >= 5].index
df_plot = df_sum[df_sum["substrate"].isin(selected_substrates)]

# Prepare result list
results = []

# Plot and test
for substrate in df_plot["substrate"].unique():
    df_sub = df_plot[df_plot["substrate"] == substrate]

    group_healthy = df_sub[df_sub["Group"] == "Healthy"]["RPKM"]
    group_obese = df_sub[df_sub["Group"] == "Obese"]["RPKM"]

    # Mann–Whitney U test
    stat, p_value = mannwhitneyu(group_healthy, group_obese, alternative="two-sided")

    # Store result
    results.append((substrate, p_value))

    # Plot
    plt.figure(figsize=(5, 2.5))
    sns.violinplot(
        data=df_sub,
        y="Group",
        x="RPKM",
        palette={"Healthy": "#66c2a5", "Obese": "#a05fa5"},
        cut=0,
        inner="box",
        scale="width",
    )
    plt.xscale("log")
    plt.xlabel("Total RPKM per sample (log scale)")
    plt.ylabel("")

    # Add title with p-value
    significance = ""
    if p_value < 0.001:
        significance = "***"
    elif p_value < 0.01:
        significance = "**"
    elif p_value < 0.05:
        significance = "*"
    elif p_value < 0.1:
        significance = "."

    plt.title(f"{substrate} (p = {p_value:.3g}) {significance}")
    plt.tight_layout()
    plt.show()

# Convert result list to DataFrame
df_stats = pd.DataFrame(results, columns=["Substrate", "p_value"])
df_stats["-log10(p)"] = -np.log10(df_stats["p_value"])
df_stats.sort_values("p_value", inplace=True)

# Optional: save to file
#df_stats.to_csv("/work/yinlab/yixing/CGC78/Final_analysis/out/firstdraft_Figure/substrate_stats.tsv", sep="\t", index=False)
plt.savefig(f"/work/yinlab/yixing/CGC78/Final_analysis/out/Finalout/draft_Figure/{substrate}_RPKM_violin.pdf")
plt.close()
# Show
print(df_stats)
