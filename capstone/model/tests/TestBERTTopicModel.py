import sys
import pytest
sys.path.append('..')
sys.path.append('../../sql')

from BERTTopicModel import BERTTopicModel


import pandas as pd
import numpy as np

class TestTopicModel:
    
    def test_all(self):
        
        model = BERTTopicModel()
        model.pre_process()
        model.train()
        #send list of documents to the function
        model.predict(list("I dont like taking metformin.  This causes severe issues for me!"))
        assert True