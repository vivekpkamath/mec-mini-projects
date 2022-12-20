import sys
import pytest
sys.path.append('..')
sys.path.append('../../sql')

from VADERSentimentModel import VADERSentimentModel

import pandas as pd
import numpy as np

class TestTopicModel:
    
    def test_all(self):
        
        model = VADERSentimentModel()
        model.pre_process()
        model.train()
        #send list of documents to the function
        model.predict("I dont like taking metformin.  This causes severe issues for me!")
        assert True