import pandas as pd

# Load the original FastQC statistics file
file_path = "/work/yinlab/yixing/CGC78/test4PRJEB12123/out/2_fastqc_multiqc_output/multiqc_data_1/general_stats_obese.csv"
df = pd.read_csv(file_path)

# Extract base sample ID (e.g., remove _1 or _2 suffix)
df["Sample_ID"] = df["Sample"].str.extract(r"(ERR\d+)")

# Group by base sample ID and aggregate:
# - Sum total reads (converted to millions)
# - Average GC content and average read length
summary_df = df.groupby("Sample_ID").agg({
    "FastQC_mqc-generalstats-fastqc-total_sequences": lambda x: round(x.sum() / 1e6, 2),
    "FastQC_mqc-generalstats-fastqc-percent_gc": "mean",
    "FastQC_mqc-generalstats-fastqc-avg_sequence_length": "mean"
}).reset_index()

# Rename columns for clarity
summary_df.columns = ["Sample", "Total Reads (M)", "GC Content (%)", "Avg Read Length"]

# Display the result
summary_df.head()
# Save the summary to a local file in this notebook environment
summary_df.to_csv("/work/yinlab/yixing/CGC78/test4PRJEB12123/out/2_fastqc_multiqc_output/multiqc_data_1/obese_summary.csv", index=False)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
healthy_path = "/work/yinlab/yixing/CGC78/test4PRJEB12123/out/2_fastqc_multiqc_output/multiqc_data/general_stats_healthy.csv"
obese_path = "/work/yinlab/yixing/CGC78/test4PRJEB12123/out/2_fastqc_multiqc_output/multiqc_data_1/general_stats_obese.csv"

# Load data
df_healthy = pd.read_csv(healthy_path)
df_obese = pd.read_csv(obese_path)

# Extract base sample ID (remove _1/_2 suffix)
df_healthy["Sample_ID"] = df_healthy["Sample"].str.extract(r"(ERR\d+)")
df_obese["Sample_ID"] = df_obese["Sample"].str.extract(r"(ERR\d+)")

# Summarize total reads per sample (paired-end sum, in millions)
df_healthy_sum = df_healthy.groupby("Sample_ID")["FastQC_mqc-generalstats-fastqc-total_sequences"].sum().reset_index()
df_obese_sum = df_obese.groupby("Sample_ID")["FastQC_mqc-generalstats-fastqc-total_sequences"].sum().reset_index()

# Add group labels
df_healthy_sum["Group"] = "Healthy"
df_obese_sum["Group"] = "Obese"

# Combine datasets
df_combined = pd.concat([df_healthy_sum, df_obese_sum])
df_combined["Total Reads (M)"] = df_combined["FastQC_mqc-generalstats-fastqc-total_sequences"] / 1e6

# Plot with custom colors
sns.set(style="whitegrid")
group_colors = {"Healthy": "#4CAF50", "Obese": "#FF7043"}

plt.figure(figsize=(6.5, 5))
sns.boxplot(data=df_combined, x="Group", y="Total Reads (M)", palette=group_colors, boxprops=dict(alpha=0.7))
sns.stripplot(data=df_combined, x="Group", y="Total Reads (M)", 
              color="black", jitter=0.15, size=4, alpha=0.5)

plt.title("Total Reads per Sample", fontsize=13)
plt.ylabel("Total Reads (Million)", fontsize=11)
plt.xlabel("")
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.show()

# Print mean values for each group
mean_values = df_combined.groupby("Group")["Total Reads (M)"].mean()
print("Mean Total Reads (Million) per Group:")
print(mean_values)
