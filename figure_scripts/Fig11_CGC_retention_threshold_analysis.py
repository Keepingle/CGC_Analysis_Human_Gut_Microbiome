import pandas as pd
import matplotlib.pyplot as plt

# === Step 1: Load retention matrix ===
file_path = "/work/yinlab/yixing/CGC78/test4PRJEB12123/out/Gluout/sra_PRJEB12123_head20_CON.profile/allscaffold/CGC_retention_matrix_cov5-10_br0.50-0.90.csv"
df = pd.read_csv(file_path)

# === Step 2: Compute average retained CGCs for each (coverage, breadth) combination ===
avg_retained = df.groupby(["Coverage", "Breadth"])["Retained_CGCs"].mean().reset_index()

# === Step 3: Plot line chart (Breadth vs Avg CGCs) for each coverage ===
plt.figure(figsize=(10, 6))
for cov in sorted(avg_retained["Coverage"].unique()):
    sub = avg_retained[avg_retained["Coverage"] == cov]
    plt.plot(sub["Breadth"], sub["Retained_CGCs"], marker='o', label=f"Coverage {cov}")

plt.xlabel("Breadth Threshold")
plt.ylabel("Average Retained CGCs")
plt.title("Retention Curve: Avg CGCs vs Breadth (Grouped by Coverage)")
plt.legend(title="Coverage")
plt.grid(True)
plt.tight_layout()
plt.show()

# === Step 4: Rank all combinations by highest CGC retention ===
top_retained = avg_retained.sort_values(by="Retained_CGCs", ascending=False)

# === Step 5: Calculate drop rate (ΔCGC) between breadth intervals (first derivative) ===
avg_retained["Drop"] = avg_retained.groupby("Coverage")["Retained_CGCs"].diff(-1).fillna(0)

# === Step 6: Identify best combinations with high CGCs and small drop ===
best_stable = avg_retained.sort_values(by=["Retained_CGCs", "Drop"], ascending=[False, True])

# === Step 7: Export results to CSV ===
top_retained.to_csv("Top_Retained_CGCs.csv", index=False)
best_stable.to_csv("Stable_High_Retention_Cutoffs.csv", index=False)
