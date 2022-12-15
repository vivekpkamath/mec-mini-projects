import sys

sys.path.append('../sql')
from DatabaseIO import DatabaseIO 
from ModelInterface import ModelInterface
import pandas as pd
import nltk
import tqdm
import gensim
import pickle
import base64
from afinn import Afinn
from datetime import datetime


class AFINNSentimentModel(ModelInterface):

    def __init__(self ) -> None:
        super().__init__()
        
    def pre_process(self):
        #load all documents from database 
        self._document_df = self._db_io.read_to_dataframe('select * from documents LIMIT 100;')
        #accept the default language of english
        print(self._document_df.head(5))
        self._model = Afinn()

    def train(self):
        print('train')
        #Let's get sentiment on all documents
        #and print them out
        # compute scores (polarity) and labels
        print(self._document_df.shape[0])
        
        scores = [self._model.score(doc) for doc in self._document_df['body']]
        sentiment = ['positive' if score > 0
                                else 'negative' if score < 0
                                    else 'neutral'
                                        for score in scores]
        self._document_df['sentiment'] = sentiment
        print(self._document_df)
        pass

    def predict(self,unseen_doc):
        print('predict')
        # compute scores (polarity) and labels
        score = self._model.score(unseen_doc) 
        if score > 0:
            sentiment = 'positive'
        elif score < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        print(sentiment)
