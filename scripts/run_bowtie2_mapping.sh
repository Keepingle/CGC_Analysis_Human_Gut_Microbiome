#!/bin/bash
# Path settings
DATA_DIR="/mnt/raid5-1/yi/CGCobesehealthMarch28/data/sra_PRJEB12123_head20_DB_fastq"
OUT_DIR="/mnt/raid5-1/yi/CGCobesehealthMarch28/data/sra_PRJEB12123_head20_DB_output"
REF_INDEX="/mnt/raid5-1/yi/CGCobesehealthMarch28/out/bowtiebuildRef/All_Ref_CGC_94019"
THREADS=32
# Create output directory if it doesn't exist
mkdir -p "$OUT_DIR"
# Loop through all _1.fastq files in the DATA_DIR
for file1 in ${DATA_DIR}/*_1.fastq; do
  # Find corresponding _2.fastq file
  file2="${file1%_1.fastq}_2.fastq"
  # Check if the paired _2.fastq file exists
  if [[ -f "$file2" ]]; then
    base_name=$(basename "$file1" "_1.fastq")
    output_file="${OUT_DIR}/${base_name}_local_very_sensitive_strict.sam"
    
    # Print the processing message
    echo "Processing $base_name..."
    
    # Start time
    START_TIME=$(date +%s)
    echo "Start time: $(date)"
    
    # Run Bowtie2 with the specified options
    bowtie2 --very-sensitive --local --no-mixed --no-discordant -p $THREADS -x $REF_INDEX -1 "$file1" -2 "$file2" -S "$output_file"

    # End time and duration
    END_TIME=$(date +%s)
    echo "End time: $(date)"
    DURATION=$((END_TIME - START_TIME))
    echo "Elapsed time: ${DURATION} seconds"
    echo "====================================================================="
    echo ""
  else
    # Print a message if the pair is not found
    echo "Pair for $file1 not found."
  fi
done
