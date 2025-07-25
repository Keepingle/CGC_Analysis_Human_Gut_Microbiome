import pandas as pd

# Load your file (adjust filename as needed)
df = pd.read_csv("/work/yinlab/yixing/CGC78/CGCobesehealthMarch28/dataAn/instrain_scaffold_filtered_counts.tsv", sep="\t")

# Extract sample ID and parameter group
df['Sample'] = df['Directory'].str.extract(r'^(ERR\d{7})')
df['Parameter'] = df['Directory'].str.extract(r'ERR\d{7}_(.*?)_instrain')

# Optional: sort for clarity
df = df.sort_values(by=['Sample', 'Parameter'])

# Save cleaned file
df.to_csv("/work/yinlab/yixing/CGC78/CGCobesehealthMarch28/dataAn/cleaned_CGC_counts.tsv", sep="\t", index=False)

import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned file
df = pd.read_csv("/work/yinlab/yixing/CGC78/CGCobesehealthMarch28/dataAn/cleaned_CGC_counts.tsv", sep="\t")

# Clean column names in case of hidden spaces
df.columns = df.columns.str.strip()

# Make the plot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Parameter", y="Retained_CGC")
plt.xticks(rotation=45)
plt.title("Retained CGC Count Across Bowtie2 Parameter Groups")
plt.tight_layout()
plt.savefig("boxplot_retained_CGC.png")
plt.show()
