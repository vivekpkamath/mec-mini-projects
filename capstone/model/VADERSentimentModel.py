import sys

sys.path.append('../sql')
from DatabaseIO import DatabaseIO 
from ModelInterface import ModelInterface
import text_normalizer as tn
import pandas as pd
import nltk
import tqdm
import gensim
import pickle
import base64
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from datetime import datetime


class VADERSentimentModel(ModelInterface):

    def __init__(self) -> None:
        super().__init__()

    def analyze_sentiment_vader_lexicon(self, doc, 
                                        threshold=0.1,
                                        verbose=False):
        # pre-process text
        #doc = tn.strip_html_tags(doc)
        #doc = tn.remove_accented_chars(doc)
        #doc = tn.expand_contractions(doc)
        
        # analyze the sentiment for doc
        self._model = SentimentIntensityAnalyzer()
        scores = self._model.polarity_scores(doc)
        # get aggregate scores and final sentiment
        agg_score = scores['compound']
        if agg_score > threshold:
            final_sentiment = 'positive' 
        elif agg_score < threshold:
            final_sentiment = 'negative'
        else:
            final_sentiment = 'neutral'
        if verbose:
            # display detailed sentiment statistics
            positive = str(round(scores['pos'], 2)*100)+'%'
            final = round(agg_score, 2)
            negative = str(round(scores['neg'], 2)*100)+'%'
            neutral = str(round(scores['neu'], 2)*100)+'%'
            sentiment_frame = pd.DataFrame([[final_sentiment, final, positive,
                                            negative, neutral]],
                                            columns=pd.MultiIndex(levels=[['SENTIMENT STATS:'], 
                                                                        ['Predicted Sentiment', 'Polarity Score',
                                                                        'Positive', 'Negative', 'Neutral']], 
                                                                labels=[[0,0,0,0,0],[0,1,2,3,4]]))
            print(sentiment_frame)
        
        return final_sentiment        
    
    def pre_process(self):
        print('pre_process')
        #nltk.download('vader_lexicon')

        #load all documents from database 
        self._document_df = self._db_io.read_to_dataframe('select * from documents LIMIT 1000;')
        #accept the default language of english
        print(self._document_df.head(5))
        self._model = SentimentIntensityAnalyzer()
        

    def train(self):
        print('train')
        #Let's get sentiment on all documents
        #and print them out
        # compute scores (polarity) and labels
        print(self._document_df.shape[0])
        for doc in self._document_df['body']:
            pred = self.analyze_sentiment_vader_lexicon(doc, 0.4, verbose=False )
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(doc, pred)
            print('------------------------------------------------------------------------------------')

    def predict(self,unseen_doc):
        pred = self.analyze_sentiment_vader_lexicon(unseen_doc, 0.4, verbose=False )
        print(pred)
        return pred

