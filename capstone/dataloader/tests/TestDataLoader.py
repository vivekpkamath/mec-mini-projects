import sys
import pytest
sys.path.append('..')
sys.path.append('../../sql')

from DataLoader import DataLoader

from DatabaseIO import DatabaseIO
import pandas as pd
import numpy as np

class TestDataLoader:
    _main_url = 'https://www.diabetesdaily.com'
    _forum_url = '/forum/forums/type-2-diabetes.14/'
    def test_scrape_all(self):
        database_io  = DatabaseIO()
        database_io.execute('truncate table documents')
        data_loader = DataLoader(self._main_url, self._forum_url, 2)
        # get a count of items loaded
        threads_added = data_loader.scrape_all()
        print('Threads Added: ' + str(threads_added))
        assert threads_added > 0
        print(threads_added)
        
        database_io.execute('select count(id) from documents')
        
        count_from_database = database_io.fetch_one()
        print(type(count_from_database))
        assert threads_added == count_from_database[0]
        