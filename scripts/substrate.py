import os
import pandas as pd
# Define file paths
substrate_dir = "/work/yinlab/yixing/CGC78/Final_analysis/data/metadata/substrate"
target_file = "/work/yinlab/yixing/CGC78/Final_analysis/out//instrainDBscaffold_info_with_RPKM.tsv"
# Read the target file and extract the second column values (before the second "|")
target_df = pd.read_csv(target_file, sep="\t", header=0)
target_df.insert(9, "substrate", "", allow_duplicates=True)  # Add new column at the position
def extract_prefix(value):
    """Extract the substring before the second | character"""
    parts = value.split("|")
    return "|".join(parts[:2]) if len(parts) > 1 else value
target_dict = {extract_prefix(row[1]): index for index, row in target_df.iterrows()}
# Iterate through all files in the substrate directory
for file in os.listdir(substrate_dir):
    file_path = os.path.join(substrate_dir, file)
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:  # Skip the first line
            parts = line.strip().split("\t")
            if len(parts) >= 5:
                key, value = parts[1], parts[4]
                if key in target_dict:
                    target_df.at[target_dict[key], "substrate"] = value
# Save the updated data
output_file = target_file.replace(".tsv", "_substrate.tsv")
target_df.to_csv(output_file, sep="\t", index=False)
print(f"File has been updated and saved to: {output_file}")
