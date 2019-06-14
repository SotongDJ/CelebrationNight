# CelebrationNight
**This project released under GPL-3.0 License.**
## Scripts for StringTie/Cufflink hybrid protocol.

- This project include some experiment coding for testing purpose.
- Use it at your own risk.
- I will try my best to write descriptions.


## Script Type
### CoFRIL

- Full form:
    
    - **Co**nfig **F**irst and **R**un **I**t **L**ater
    
- Defination:
    
    |   **Defination**   |
    | ---- |
    | 1. Pack process code into python class (**.py** file with "lib" prefix) |
    | 2. must run \*-setConfig.py to configure dependent variables |
    | (\*-setConfig.py template: "\*-configExample.py") |
    | 3. run related python class in \*-run.py |
    | (\*-run.py template: "\*-exampleRun.py") |

### RuDi

- Full form:
    
    - **Ru**n **Di**rectly
    
- Defination:
    
    |   **Defination**                   |
    | ----                               |
    | 1. Declare sample-dependent variables on the begining of script |
    | 2. Derive downstream variables     |
    | 3. Run code directly without class |    

## Processing Stage (General usage)

### Stage 01 - FASTQ Quality Report
- Checking Quality

    | List   | Detail            |
    | ----   | ----              | 
    | Type   | Under development |
    | Binary | FastQC            |

### Stage 02 - HISAT2 index
- Prepare HISAT2 index

    | List   | Detail             |
    | ----   | ----               | 
    | Type   | CoFRIL             |
    | Class  | libHISAT.indexer() |
    | Binary | HISAT2 (index)     |

### Stage 03 - Trim
- Trim FASTQ files

    | List   | Detail            |
    | ----   | ----              | 
    | Type   | CoFRIL            |
    | Class  | libTrim.trimmer() |
    | Binary | Trimmomatic       |
    | Input  | raw NGS FASTQ     |

### Stage 04 - HISAT2


## Processing Stage (Distinctive usage)

### Stage 07 - Comparing Genomic Annotation
- Get information of isoform under each gene model

    | List         | Detail    |
    | ----         | ----      | 
    | Abbreviation | **07-cg** |
    | Type         | RuDi      |
    | Input        | **07-st** |
