import pandas as pd
# File path
input_file = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainCONscaffold_info_with_RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict.tsv"
output_file = input_file.replace(".tsv", "_lengthFiltered.tsv")
# Load TSV
df = pd.read_csv(input_file, sep="\t")
# Filter: keep rows with length >= 2933
df_filtered = df[df.iloc[:, 2] >= 2933]
# Save the result
df_filtered.to_csv(output_file, sep="\t", index=False)
print(f"Filtered file saved to: {output_file}")
