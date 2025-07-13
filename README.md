# CGC Analysis Workflow for Human Gut Microbiome

This repository contains a reproducible bioinformatics workflow for analyzing Carbohydrate-active enzyme Gene Clusters (CGCs) in human gut metagenomic samples. The pipeline supports read mapping to a reference CGC database, RPKM abundance calculation, CGC filtering by coverage and breadth, substrate-level enrichment analysis, and data visualization. It is designed to compare CGC profiles between different cohorts, such as healthy and obese individuals.

---

## Repository Structure

<pre>
CGC_Analysis_Human_Gut_Microbiome/
├── scripts/                     # All analysis scripts (bash, Python, R)
│   ├── build_bowtie2_index.sh
│   ├── run_bowtie2_mapping.sh
│   ├── run_instrain_profile.sh
│   ├── merge_scaffold_info.py
│   ├── calculate_cgc_rpkm.py
│   ├── filter_cgcs_by_cov_br.py
│   ├── substrate_enrichment_analysis.R
│   └── plot_cgc_visualizations.R
├── data/                        # Reference files and annotation tables
├── results/                     # Output files (RPKM tables, plots, etc.)
├── example_data/                # (Optional) Small test data and outputs
└── README.md                    # Project documentation
</pre>

---

## Requirements

- Linux/macOS terminal
- [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/)
- [samtools](http://www.htslib.org/)
- [inStrain](https://instrain.readthedocs.io/)
- Python 3.x (with `pandas`, `argparse`)
- R (with `ggplot2`, `dplyr`, `readr`, `reshape2`)

---

## Workflow Overview

1. Build Bowtie2 index from the reference CGC database  
2. Map cleaned metagenomic reads to the reference using Bowtie2  
3. Use inStrain to profile scaffold-level statistics  
4. Merge scaffold info and annotate with substrate categories  
5. Calculate RPKM values for each CGC  
6. Filter CGCs using coverage and breadth thresholds  
7. Perform substrate-level enrichment analysis  
8. Visualize differences between healthy and obese microbiomes  

---











