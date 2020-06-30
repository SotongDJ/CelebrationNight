# CelebrationNight
**This project released under GPL-3.0 License.**
## Scripts for StringTie/Cufflink hybrid protocol.

- This project include some experiment coding for testing purpose.
- Use it at your own risk.
- I will try my best to write documentation.
- Scripts for Stringtie were removed in current version (108-2 Generation)

## Script Type
### CoFRIL

- **Co**nfig **F**irst and **R**un **I**t **L**ater

|   **Definition**   |
| ---- |
| 1. Pack process code into python class (**.py** file with "lib" prefix) |
| 2. Run cf-\*.py first to configure dependent variables (Initialization) |
| (cf-\*.py template: "cf-\*-exampleRun.py") |
| 3. Run related python scripts in \*-run.py |
| (\*-run.py template: "\*-exampleRun.py") |

### RuDi

- **Ru**n **Di**rectly

|   **Definition**                   |
| ----                               |
| 1. Declare sample-dependent variables on the begining of script |
| 2. Derive downstream variables     |
| 3. Run code directly without class |

## Processing Stage (General usage)

### Stage 01 - FASTQ Quality Report
| List     | Detail        |
| ----     | ----          |
| Codename | **01-fastqc** |
| Usage    | Check Quality |
| Type     | RuDi          |
| Binary   | FastQC        |
| Input    | NGS FASTQ     |

### Stage 02 - HISAT2 index
| List     | Detail                   |
| ----     | ----                     |
| Codename | **02-hisat2-index**      |
| Usage    | Build HISAT2 index       |
| Type     | CoFRIL                   |
| Class    | libHISAT.indexer()       |
| Binary   | hisat2-build from HISAT2 |
| Input    | Genome sequences         |

### Stage 03 - Trim
| List     | Detail            |
| ----     | ----              |
| Codename | **03-trim**       |
| Usage    | Trim FASTQ files  |
| Type     | CoFRIL            |
| Class    | libTrim.trimmer() |
| Binary   | Trimmomatic       |
| Input    | raw NGS FASTQ     |

### Stage 04 - HISAT2
| List     | Detail                 |
| ----     | ----                   |
| Codename | **04-hisat2**          |
| Usage    | Alignment and mapping  |
| Type     | CoFRIL                 |
| Class    | libHISAT.aligner()     |
| Binary   | samtools from SAMtools |
|          | hisat2 from HISAT2     |
| Input    | **02-hisat2-index**    |
|          | **03-trim**            |

### Stage 05 - Transcriptome conversion
| List     | Detail                          |
| ----     | ----                            |
| Codename | **05-gffread**                  |
| Usage    | Convert genome to transcriptome |
| Type     | CoFRIL                          |
| Class    | libCuffdiff.converter()         |
| Binary   | gffread                         |
| Input    | Genomic annotation              |

### Stage 06 - Transcripts extraction and analysis
| List     | Detail           |
| ----     | ----             |
| Codename | **06-fastn**     |
| Usage    | Extract transcripts from transcriptome and analysis properties of transcriptome |
| Type     | RuDi             |
| Class    | none             |
| Binary   | none             |
| Input    | **05-gffread**   |
|          | **05-stringtie** |
|          | **05-cufflink**  |

### Stage 07 - Expression estimation
| List     | Detail                          |
| ----     | ----                            |
| Codename | **07-cuffdiff**                 |
| Usage    | Estimate the expression profile |
| Type     | CoFRIL                          |
| Class    | libCuffdiff.differ()            |
| Binary   | cuffdiff                        |
| Input    | **04-hisat2**                   |
|          | **05-gffread**                  |
|          | **05-stringtie**                |
|          | **05-cufflink**                 |

### Stage 08 - Homologous functional annotation
