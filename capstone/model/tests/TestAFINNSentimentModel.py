import sys
import pytest
sys.path.append('..')
sys.path.append('../../sql')

from AFINNSentimentModel import AFINNSentimentModel

from DatabaseIO import DatabaseIO
import pandas as pd
import numpy as np

class TestTopicModel:
    
    def test_all(self):
        db_io = DatabaseIO()
        model = AFINNSentimentModel(db_io)
        model.pre_process()
        model.train()
        #send list of documents to the function
        model.predict("I dont like taking metformin.  This causes severe issues for me!")
        assert True