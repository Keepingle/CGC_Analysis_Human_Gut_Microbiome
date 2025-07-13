import pandas as pd
import os
# === File paths ===
rpkm_file = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainDBscaffold_info_with_RPKM_substrate.tsv"
meta_file = "/work/yinlab/yixing/CGC78/Final_analysis/data/metadata/genomes-all_metadata/genomes-all_metadata.tsv"
output_file = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainDBscaffold_info_with_RPKM_metadata.tsv"
# === Load the input files ===
df_rpkm = pd.read_csv(rpkm_file, sep="\t")
df_meta = pd.read_csv(meta_file, sep="\t")
# === Extract Genome_ID from scaffold column ===
df_rpkm["Genome_ID"] = df_rpkm["scaffold"].str.extract(r"^(MGYG\d+)")
# === Select and rename metadata columns ===
meta_cols = ["Genome", "Lineage"]
if "Country" in df_meta.columns and "Continent" in df_meta.columns:
    meta_cols += ["Country", "Continent"]
df_meta_sub = df_meta[meta_cols].rename(columns={"Genome": "Genome_ID"})
# === Merge metadata into RPKM table ===
df_merged = df_rpkm.merge(df_meta_sub, on="Genome_ID", how="left")
# === Save the merged table ===
df_merged.to_csv(output_file, sep="\t", index=False)
print(f"Output saved to: {output_file}")
