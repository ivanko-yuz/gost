
import pandas as pd

def csv_run():
    
    dfname = pd.read_csv('data_tittles.csv', sep=',')
    dfname_set = pd.read_csv('data_tittles.csv', sep=',', header=None)
    dfname_set.columns = ["Title"]
    
    dfstyle = pd.read_csv('data_styles.csv', sep=',')
    dfgenre_set = pd.read_csv('data_styles.csv', sep=',', header=None)
    dfgenre_set.columns = ['Genre']
    dfgenre_set['Genre'] = dfgenre_set['Genre'].str.strip()
    
    dfauthor = pd.read_csv('data_authors.csv', sep=',')
    dfauthor_set = pd.read_csv('data_authors.csv', sep=',', header=None)
    dfauthor_set.columns = ["Author"]
    
    dfhashes = pd.read_csv('data.csv', sep=',')
    dfhashes_set = pd.read_csv('data.csv', sep=',', header=None)
    
    df = pd.concat([dfhashes, dfstyle], axis=1, join='inner')
    df_full = pd.concat([dfhashes_set, dfauthor_set, dfname_set, dfgenre_set] , axis=1)

    return df, df_full, dfauthor, dfauthor_set, dfgenre_set, dfhashes, dfhashes_set, dfname_set, dfstyle