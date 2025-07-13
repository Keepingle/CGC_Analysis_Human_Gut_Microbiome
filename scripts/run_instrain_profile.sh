#!/bin/bash
# Input paths
BAM_DIR="/mnt/raid5-1/yi/CGCobesehealthMarch28/data/sra_PRJEB12123_head20_CON_output/bam_sorted"
REF="/mnt/raid5-1/yi/CGCobesehealthMarch28/data/All_Ref_CGC_94019.fna"
OUT_DIR="/mnt/raid5-1/yi/CGCobesehealthMarch28/out/Test_May12/inStrain_CON_profiles"
mkdir -p "$OUT_DIR"
# Log time
TOTAL_START=$(date +%s)
echo "Start running inStrain..."
echo "Start time: $(date)"
echo ""
# Run inStrain profile for each BAM
for BAM in "$BAM_DIR"/*.sorted.bam; do
  BASENAME=$(basename "$BAM" .sorted.bam)
  IS_OUT="$OUT_DIR/${BASENAME}_instrain"
  echo "Processing $BASENAME"
  START=$(date +%s)
  echo "Start time: $(date)"
  inStrain profile "$BAM" "$REF" -o "$IS_OUT" -p 32
  END=$(date +%s)
  echo "End time: $(date)"
  ELAPSED=$((END - START))
  echo "Elapsed time: ${ELAPSED} seconds"
  echo "Output folder: $IS_OUT"
  echo ""
done

# Log total time
TOTAL_END=$(date +%s)
TOTAL_ELAPSED=$((TOTAL_END - TOTAL_START))
echo "All inStrain jobs finished."
echo "End time: $(date)"
echo "Total elapsed time: ${TOTAL_ELAPSED} seconds"
