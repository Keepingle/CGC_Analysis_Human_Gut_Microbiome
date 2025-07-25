import matplotlib.pyplot as plt
import numpy as np

# --- Step 1: Read sequence lengths from FASTA ---
fasta_file = "/work/yinlab/yixing/CGC78/test4PRJEB12123/data/Glusam/All_Ref_CGC_94019.fna"
lengths = []

with open(fasta_file, "r") as f:
    seq = ""
    for line in f:
        if line.startswith(">"):
            if seq:
                lengths.append(len(seq))
                seq = ""
        else:
            seq += line.strip()
    if seq:
        lengths.append(len(seq))  # Add last sequence

# --- Step 2: Calculate statistics ---
percentile_10 = np.percentile(lengths, 10)
max_length = max(lengths)
avg_length = np.mean(lengths)

# --- Step 3: Plot ---
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(lengths, bins=50, color='skyblue', edgecolor='black')

# 10th percentile line and label
plt.axvline(percentile_10, color='indianred', linestyle='--', linewidth=2,
            label=f'10th Percentile: {int(percentile_10)} bp')
plt.text(percentile_10 + 500, max(n), f'{int(percentile_10)} bp',
         color='indianred', rotation=90, fontsize=9, va='top')

# Longest CGC line and label
plt.axvline(max_length, color='gray', linestyle='--', linewidth=2,
            label=f'Longest CGC: {int(max_length)} bp')
plt.text(max_length + 500, max(n), f'{int(max_length)} bp',
         color='gray', rotation=90, fontsize=9, va='top')

# Average CGC line and label
plt.axvline(avg_length, color='steelblue', linestyle='--', linewidth=2,
            label=f'Average: {int(avg_length)} bp')
plt.text(avg_length + 500, max(n), f'{int(avg_length)} bp',
         color='steelblue', rotation=90, fontsize=9, va='top')


# Axis labels and title
plt.title("CGC Length Distribution", fontsize=14)
plt.xlabel("Length (bp)", fontsize=12)
plt.ylabel("Count", fontsize=12)

# Reduce y-axis tick density
step = 5000
plt.yticks(np.arange(0, int(max(n)) + step, step))

# Grid lines (x-axis only)
plt.grid(axis='x', linestyle='--', alpha=0.3)

# Remove borders
ax = plt.gca()
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)

# Add legend
plt.legend(fontsize=10)

# --- Step 4: Save and show ---
#output_path = '/work/yinlab/yixing/CGC78/Final_analysis/out/firstdraft_Figure/CGC_Length_Distribution.png'
plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

# --- Step 5: Print statistics ---
#print(f"10th Percentile CGC Length: {int(percentile_10)} bp")
#print(f"Average CGC Length: {int(avg_length)} bp")
#print(f"Longest CGC Length: {int(max_length)} bp")

