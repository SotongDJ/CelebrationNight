#!/usr/bin/env python3
import pandas as pd
import sqlite3
tsvPath = "data/dbga-GenomeAnnotation/arathTAIR/gene_descriptions.tsv"
sqlPath = "data/dbga-GenomeAnnotation/arathTAIR/gene_descriptions.db"

tsvDF = pd.read_csv(tsvPath,header=0,sep="\t",index_col=False)
columnSet = set(tsvDF.columns)

Connect = sqlite3.connect(sqlPath)
tsvDF.to_sql(name='GeneDescriptions', con=Connect)
Connect.commit()
Connect.close()
