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
        self._document_df = self._dal.getAllDocuments()
        #accept the default language of english
        print(self._document_df.head(5))
        self._model = Afinn()

    def train(self):
        print('train')
        #
        #There is no need to store the sentiment model.  It has not been trained
        #but we just create dummy record
        #
        model_id = self._dal.addOneModel('AFINNSentiment', "", "", "")       
        
        # compute scores (polarity) and labels
        print(self._document_df.shape[0])

        for row in self._document_df.itertuples():
            score = self._model.score(row.body)
            sentiment = 0
            if score > 0:
                sentiment = 1
            elif score < 0:
                sentiment = -1
            self._dal.addSentiment(model_id, row.id, sentiment)
            

        

    def predict(self,unseen_doc):
        print('predict')
        # compute scores (polarity) and labels
        score = self._model.score(unseen_doc) 
        sentiment = 0
        if score > 0:
            sentiment = 1
        elif score < 0:
            sentiment = -1
        
        return sentiment
