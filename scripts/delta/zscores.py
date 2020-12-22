import glob
import regex as re
from collections import Counter

import pandas as pd

from scipy.stats import zscore
from scipy.spatial import distance

import nltk
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer

class Zscores():
    def __init__(self, data):
        self.data = data

    def remove_stopwords(self):
        stopword = open("/home/piah/Dokumente/Uni/Projektarbeit/Projektarbeit_LyrikGattungszuweisung/scripts/zeta/de_stopwords.txt")
        stopwords = stopword.read()
        self.data['text'] = [str(i).lower() for i in self.data['text']]
        self.data['removedstopword'] = self.data['text'].apply(lambda x: ' '.join([item for item in str(x).split() if item not in stopwords]))
        return self.data


    def count_frequencies(self, df):
        freq_list = []
        for i, row in df.iterrows():
            title = str(row.Gattung)+"_"+str(i)
            vocab = Counter(row.removedstopword.split())
            frequencies = list(vocab.values())
            words = list(vocab.keys())
            freq_list.append(pd.Series(frequencies, words, name=title))
        return freq_list

    def calculate_zscores(self):
        df = self.remove_stopwords()
        #df = self
        freq_list = self.count_frequencies(df)
        counts = pd.DataFrame(freq_list)
        counts = counts.fillna(0)
        counts = counts.div(counts.sum(axis=1), axis=0)
        counts.loc['Total_per_word'] = counts.sum()
        counts = counts.sort_values(by='Total_per_word', axis=1, ascending=False)
        counts.drop('Total_per_word', inplace=True, axis=0)
        print(counts)

        zscores = (counts - counts.mean()) / counts.std()
        # zscores = counts.apply(zscore)
        print(zscores)

        zscores.drop(zscores.columns[1000:], inplace=True, axis=1)

        return zscores


poems = pd.read_csv('/home/piah/Dokumente/Uni/Projektarbeit/Projektarbeit_LyrikGattungszuweisung/corpus/csv_delta/Angepasst_Größe_balladen.csv', index_col=[0])
z = Zscores(poems)
zscores = z.calculate_zscores()
zscores.to_csv('/home/piah/Dokumente/Uni/Projektarbeit/Projektarbeit_LyrikGattungszuweisung/corpus/results/delta/zscores_Angepasst_Größe_balladen.csv')