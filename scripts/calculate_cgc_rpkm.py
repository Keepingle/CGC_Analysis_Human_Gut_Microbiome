import os
import subprocess
import pandas as pd
# Define file paths
info_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainCONscaffold_info_merged.tsv"
bam_dir = "/work/yinlab/yixing/CGC78/Final_analysis/data/sra_PRJEB12123_head20_CON_output/bam_sorted"
output_path = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainCONscaffold_info_with_RPKM.tsv"
# Load the original scaffold info table
df_info = pd.read_csv(info_path, sep="\t")
# List to store results for all samples
all_dfs = []
# Process each sample_id one by one
for sample_id in df_info["sample_id"].unique():
    bam_file = os.path.join(bam_dir, f"{sample_id}_local_very_sensitive_strict.sorted.bam")


    if not os.path.exists(bam_file):
        print(f"BAM file not found for {sample_id}, skipping.")
        continue
    # Run samtools idxstats and extract scaffold and mapped reads
    cmd = f"samtools idxstats {bam_file} | cut -f1,3"
    try:
        mapped_reads_output = subprocess.check_output(cmd, shell=True).decode().strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"samtools idxstats failed for {sample_id}")
        print(e.output.decode())
        continue
    # Parse the output and calculate total reads in the sample
    data = []
    total_reads_in_sample = 0


    for line in mapped_reads_output:
        if line:
            scaffold, mapped = line.strip().split("\t")
            mapped = int(mapped)
            total_reads_in_sample += mapped
            data.append({
                "sample_id": sample_id,
                "scaffold": scaffold,
                "mapped_reads": mapped
            })
    df_idx = pd.DataFrame(data)
    # Get the CGC-related scaffolds from the original table
    df_sub = df_info[df_info["sample_id"] == sample_id].copy()
  
    # Merge mapped_reads into the scaffold info
    df_merged = df_sub.merge(df_idx, on=["sample_id", "scaffold"], how="left")
    # Fill missing values (if any scaffold was not found in BAM)
    df_merged["mapped_reads"] = df_merged["mapped_reads"].fillna(0).astype(int)
    # Use total reads in sample for RPKM normalization
    df_merged["Total_Reads_in_Sample"] = total_reads_in_sample
    df_merged["RPKM"] = df_merged["mapped_reads"] / ((df_merged["length"] / 1000) * (total_reads_in_sample / 1e6))
    # Store result
    all_dfs.append(df_merged)
# Combine all sample results and save
df_final = pd.concat(all_dfs, ignore_index=True)
df_final.to_csv(output_path, sep="\t", index=False)


print(f"Output saved to: {output_path}")
