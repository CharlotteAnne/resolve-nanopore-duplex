# resolve-nanopore-duplex
After duplex calling using Guppy you are left with a fastq of duplexes and one of simplexes - this script takes both and the list of paired reads to create one final file where there is not duplication of reads.

## Requirements
biopython

## Run
`python resolve-np-duplex.py -s merged_simplex.fastq.gz -d merged_duplex.fastq.gz -p pair_ids_filtered.txt`
