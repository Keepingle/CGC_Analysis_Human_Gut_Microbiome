#!/bin/bash
SAM_DIR="/mnt/raid5-1/yi/CGCobesehealthMarch28/data/sra_PRJEB12123_head20_CON_output"
OUT_DIR="$SAM_DIR/bam_sorted"
mkdir -p "$OUT_DIR"
# Record total start time
TOTAL_START=$(date +%s)
echo "Total start time: $(date)"
echo ""
for SAM_FILE in "$SAM_DIR"/*.sam; do
  BASENAME=$(basename "$SAM_FILE" .sam)
  BAM_FILE="$OUT_DIR/${BASENAME}.bam"
  SORTED_BAM="$OUT_DIR/${BASENAME}.sorted.bam"
  echo "Processing $SAM_FILE"
  START_TIME=$(date +%s)
  echo "Start time: $(date)"
  samtools view -@ 32 -bS "$SAM_FILE" > "$BAM_FILE"
  samtools sort -@ 32 "$BAM_FILE" -o "$SORTED_BAM"
  samtools index "$SORTED_BAM"
  END_TIME=$(date +%s)
  ELAPSED=$((END_TIME - START_TIME))
  echo "End time: $(date)"
  echo "Elapsed time: ${ELAPSED} seconds"
  echo "Output files:"
  echo "  $SORTED_BAM"
  echo "  ${SORTED_BAM}.bai"
  echo ""
done



TOTAL_END=$(date +%s)
TOTAL_ELAPSED=$((TOTAL_END - TOTAL_START))
echo "Total end time: $(date)"
echo "Total elapsed time: ${TOTAL_ELAPSED} seconds"
