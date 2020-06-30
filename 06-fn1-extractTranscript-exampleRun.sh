bin/cufflinks/gffread\
 -g userData/dbgs-GenomeSequence/speciesDatabase/speciesDatabase.fn\
 -w userData/06-gr-exportTranscript/speciesTreatment/speciesDatabase-trimQ30-transcript.fn\
 userData/05-gr-transcriptomeConstruction/speciesTreatment/speciesDatabase-trimQ30-final.gtf

cat userData/06-gr-exportTranscript/speciesTreatment/speciesDatabase-trimQ30-transcript.fn|grep ">"|wc -l
#42193