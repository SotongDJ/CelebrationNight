# CelebrationNight
**This project released under GPL-3.0 License.**
## Scripts for StringTie/Cufflink hybrid protocol.

- This project include some experiment coding for testing purpose.
- Use it at your own risk.
- I will try my best to write descriptions.


## Script Type
### CoFRIL

- Full form: **Co**nfig **F**irst and **R**un **I**t **L**ater

|   **Definition**   |
| ---- |
| 1. Pack process code into python class (**.py** file with "lib" prefix) |
| 2. must run \*-setConfig.py to configure dependent variables |
| (\*-setConfig.py template: "\*-configExample.py") |
| 3. run related python class in \*-run.py |
| (\*-run.py template: "\*-exampleRun.py") |

### RuDi

- Full form: **Ru**n **Di**rectly

|   **Definition**                   |
| ----                               |
| 1. Declare sample-dependent variables on the begining of script |
| 2. Derive downstream variables     |
| 3. Run code directly without class |

## Processing Stage (General usage)

### Stage 01 - FASTQ Quality Report
| List     | Detail            |
| ----     | ----              |
| Codename | **01-fastqc**     |
| Usage    | Check Quality     |
| Type     | Under development |
| Binary   | FastQC            |
| Input    | NGS FASTQ         |

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

## Processing Stage (Distinctive usage)
**The scripts under this catalogue may lose function as their development didn't stick to the current coding style.**

### Stage 04 - HISAT2 Summariser
| List     | Detail                 |
| ----     | ----                   |
| Codename | **04-hs**              |
| Usage    | Analyse HISAT2 result  |
| Type     | CoFRIL                 |
| Class    | libHISAT.summariser()  |
| Binary   | samtools from SAMtools |
| Input    | **04-hisat2**          |

### Stage 07 - Comparing Genomic Annotation
| List     | Detail    |
| ----     | ----      |
| Codename | **07-cg** |
| Usage    | Get information of isoform under each gene model |
| Type     | RuDi      |
| Input    | **07-st** |