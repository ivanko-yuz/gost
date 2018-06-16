
import pandas as pd
import csv

def genreToVector(genre):
    genres = ["POP", "CLASSIC", "UNKNOWN", "ROCK", "Metal"]
    vector = [0] * len(genre)
    vector[genres.index(genre)] = 1
    return vector


def vectorToGenre(vector):
    genres = ["POP", "CLASSIC", "UNKNOWN", "ROCK", "Metal"]
    genre = genres[np.where(vector==1)[0][0]]
    return genre



def slm_run():
    dfname = pd.read_csv('data_tittles.csv', sep=',', header=None)
    dfname.columns = ["Title"]

    dfgenre = pd.read_csv('data_styles.csv', sep=',', header=None)
    dfgenre.columns = ["Genre"]

    dfauthor = pd.read_csv('data_authors.csv', sep=',', header=None)
    dfauthor.columns = ["Author"]

    dfhashes = pd.read_csv('data.csv', sep=',', header=None)


    df_full = pd.concat([dfhashes,dfauthor,dfname,dfgenre] , axis=1)

    df_full=df_full.fillna(0)

    print(df_full)






