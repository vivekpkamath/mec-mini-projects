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
from bertopic import BERTopic
from datetime import datetime

class BERTTopicModel(ModelInterface):

    def __init__(self, db_io ) -> None:
        super().__init__(db_io)
        
    def pre_process(self):
        print('pre_process')
        '''
        #Need to do this first
        pip install bertopic
        pip install bertopic[flair]
        pip install bertopic[gensim]
        pip install bertopic[spacy]
        pip install bertopic[use]
        '''
        #load all documents from database 
        self._document_df = self._db_io.read_to_dataframe('select * from documents;')
        #accept the default language of english
        print(self._document_df.head(5))
        self._model = BERTopic(language='english')
        


    def train(self):
        print('train')
        self._model.fit_transform(self._document_df['title'].to_list())
        print(self._model.get_topic_freq().head(10))
        print(self._model.get_topic(0)[:10])
        print(self._model.get_topic_info())
    
        print('------------------------------------------')
        print(self._model.get_topics())
        print('------------------------------------------')
        #persist model in database

    def predict(self, unseen_doc):
        print('predict')
        #read model from database
        predicted_topics, predicted_probs = self._model.transform(unseen_doc)
        print(predicted_topics)
        print(predicted_probs)
        

