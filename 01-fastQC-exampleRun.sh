find|grep ".fastq" > hisat2-list.txt
mkdir largeData/04-hisat2/species/speciesDatabase-trimQ30/report
python3 01-fastQC-run.py