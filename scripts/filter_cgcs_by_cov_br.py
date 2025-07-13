import pandas as pd
# Load the annotated RPKM+metadata file
input_file = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainDBscaffold_info_with_RPKM_substrate_Lineage_Country_Continent.tsv"
df = pd.read_csv(input_file, sep="\t")
# Version A: lenient filter (without popANI)
df_lenient = df[(df["coverage"] >= 4) & (df["breadth"] >= 0.8)]
# Version B: strict filter (with popANI ≥ 0.95)
df_strict = df_lenient[df_lenient["popANI_reference"] >= 0.95]
# Save both versions
df_lenient.to_csv("/work/yinlab/yixing/CGC78/Final_analysis/out/instrainDBscaffold_info_with_RPKM_substrate_Lineage_Country_Continent_Cov4_Br085_filtered_lenient.tsv", sep="\t", index=False)
df_strict.to_csv("/work/yinlab/yixing/CGC78/Final_analysis/out/instrainDBscaffold_info_with_RPKM_substrate_Lineage_Country_Continent_Cov4_Br08_popANI95_filtered_strict.tsv", sep="\t", index=False)

# Print summary
print(f"Lenient version (coverage≥4 & breadth≥0.8): {df_lenient.shape[0]} entries")
print(f"Strict version (additionally popANI≥0.95): {df_strict.shape[0]} entries")
