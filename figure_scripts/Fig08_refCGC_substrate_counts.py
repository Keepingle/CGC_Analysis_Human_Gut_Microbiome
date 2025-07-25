import glob
import os
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read all files and count lines
path = '/work/yinlab/yixing/CGC78/Final_analysis/data/metadata/substrate_merged/*'
file_list = glob.glob(path)

substrate_counts = {}

for file_path in file_list:
    # Get filename without extension
    substrate_name = os.path.basename(file_path).replace('.txt', '').lower()
    with open(file_path, 'r') as file:
        line_count = sum(1 for _ in file)
        substrate_counts[substrate_name] = line_count

# Step 2: Convert to DataFrame and sort
df_substrate_counts = pd.DataFrame.from_dict(
    substrate_counts, orient='index', columns=['CGC_Count']
).sort_values(by='CGC_Count', ascending=False)



# Step 4: Plot horizontal bar chart
plt.figure(figsize=(10, 8))
ax = df_substrate_counts['CGC_Count'].plot(
    kind='barh',
    color='steelblue',
)

# Add vertical grid lines
plt.grid(axis='x', linestyle='--', alpha=0.6)

# Remove top, right, bottom, and left spines (borders)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

# Add axis labels and title
plt.title('CGC Count per Substrate', fontsize=14)
plt.xlabel('CGC Count', fontsize=12)
plt.ylabel('Substrate', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Annotate counts
for i, value in enumerate(df_substrate_counts['CGC_Count']):
    plt.text(value + max(df_substrate_counts['CGC_Count']) * 0.01, i, str(value),
             va='center', fontsize=9)

plt.tight_layout()

# Save figure
#output_path = '/work/yinlab/yixing/CGC78/Final_analysis/out/firstdraft_Figure/substrate_CGC_counts_horizontal.png'
plt.savefig(output_path, bbox_inches='tight', dpi=300)

plt.show()
