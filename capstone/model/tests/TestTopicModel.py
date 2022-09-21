import sys
import pytest
sys.path.append('..')
sys.path.append('../../sql')

from TopicModel import TopicModel

from DatabaseIO import DatabaseIO
import pandas as pd
import numpy as np

class TestTopicModel:
    
    def test_all(self):
        db_io = DatabaseIO()
        model = TopicModel(db_io)
        model.pre_process()
        model.train()
        assert True