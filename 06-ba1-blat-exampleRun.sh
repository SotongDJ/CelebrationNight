# Extract transcript sequences from GTF

# Input:
#     Genome Sequences FASTA     : data/dbgs-GenomeSequence/speciesEnsembl/speciesEnsembl.fn
#     Transcriptome GTF          : data/05-??-Stringtie/testing/speciesEnsembl-trimQ30-merged.gtf
# Output:
#     Transcript Sequences FASTA : data/05-??-Stringtie/testing/speciesEnsembl-trimQ30-transcript.fn
bin/cufflinks/gffread\
 -g data/dbgs-GenomeSequence/speciesEnsembl/speciesEnsembl.fn\
 -w data/05-??-Stringtie/testing/speciesEnsembl-trimQ30-transcript.fn\
 data/05-??-Stringtie/testing/speciesEnsembl-trimQ30-merged.gtf

# Show the amount of transcript sequences
cat data/05-??-Stringtie/testing/speciesEnsembl-trimQ30-transcript.fn|grep ">"|wc -l

# Blat query sequences on target sequences

# Input:
#     Target Sequences FASTA : data/05-??-Stringtie/testing/speciesEnsembl-trimQ30-transcript.fn
#     Query Sequences FASTA  : data/05-**-Stringtie/testing/speciesEnsembl-trimQ30-transcript.fn
# Output:
#     Result PSL: data/06-ba-blat/speciesEnsembl/T??Q**-testing-trimQ30.psl
time bin/blat/blat\
 data/05-??-Stringtie/testing/speciesEnsembl-trimQ30-transcript.fn\
 data/05-**-Stringtie/testing/speciesEnsembl-trimQ30-transcript.fn\
 data/06-ba-blat/speciesEnsembl/T??Q**-testing-trimQ30.psl
