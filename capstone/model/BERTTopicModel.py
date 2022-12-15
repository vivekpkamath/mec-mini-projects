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

    def __init__(self) -> None:
        super().__init__()
        
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
        self._document_df = self._dal.getAllDocuments()
        #accept the default language of english
        print(self._document_df.head(5))
        self._model = BERTopic(language='english')
        


    def train(self):
        print('train')

        self._model.fit_transform(self._document_df['body'].to_list())
        print(self._model.get_topic_freq().head(10))
        print(self._model.get_topic(0)[:10])
        print(self._model.get_topic_info())
    
        print('------------------------------------------')
        print(self._model.get_topics())
        print('------------------------------------------')
        #persist model in database and add topics
        pickle_bert_model = base64.b64encode(pickle.dumps(self._model))
        pickle_bow_corpus = 'N/A'
        pickle_dictionary = 'N/A'
        #store model
        model_id = self._dal.addOneModel('BERTopic', pickle_bert_model, pickle_bow_corpus, pickle_dictionary)
        for topic in self._model.get_topics():
            self._dal.addTopicforModel(model_id, topic)
        #User OCTIS to get metrics and store them


    def predict(self, unseen_doc):
        print('predict')
        #read model from database
        rows = self._dal.getCurrentModelOfType('BERTopic')
        if (len(rows) != 1):
            return
        self._model = pickle.loads(base64.b64decode(rows[0][2]))

        predicted_topics, predicted_probs = self._model.transform(unseen_doc)
        print(predicted_topics)
        print(predicted_probs)
        

