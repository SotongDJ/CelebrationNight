#!/usr/bin/env python3
import pandas as pd
import sqlite3
tsvPath = "*.tsv"
sqlPath = "*.db"

tsvDF = pd.read_csv(tsvPath,header=0,sep="\t",index_col=False)
# tsvDF = pd.read_csv(tsvPath,header=None,names=("col1", "col2", "col3", "col4", "col5"),sep="\t",index_col=False)
columnSet = set(tsvDF.columns)

Connect = sqlite3.connect(sqlPath)
tsvDF.to_sql(name='Primary', con=Connect, index=False)
Connect.commit()
Connect.close()