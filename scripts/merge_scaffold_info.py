import os
import pandas as pd
# Define input and output paths
input_dir = "/work/yinlab/yixing/CGC78/Final_analysis/data/inStrainDBoutput"
output_file = "/work/yinlab/yixing/CGC78/Final_analysis/out/instrainDBscaffold_info_merged.tsv"
# List to hold dataframes
dfs = []
# Process each file
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith("_instrain_scaffold_info.tsv"):
        file_path = os.path.join(input_dir, filename)
        sample_id = filename.split("_")[0]  # Extract sample ID (e.g., ERR1190634)
        # Load the file, selecting only desired columns (1,2,3,4,16 → index 0,1,2,3,15)
        df = pd.read_csv(file_path, sep="\t", usecols=[0,1,2,3,15])
        # Add sample_id column at the beginning
        df.insert(0, "sample_id", sample_id)
        # Store dataframe
        dfs.append(df)
# Merge all dataframes
merged_df = pd.concat(dfs, ignore_index=True)
# Save to output file
merged_df.to_csv(output_file, sep="\t", index=False)
