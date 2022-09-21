import sys
import pytest
sys.path.append('..')
from DatabaseIO import DatabaseIO
import pandas as pd
import numpy as np
import pandas as pd

class TestDatabaseIO:

    def test_read_to_dataframe(self):
        database_io = DatabaseIO()
        document_df = database_io.read_to_dataframe('select * from documents')
        #make sure we have id, title, body and date columns
        #get count of rows in the dataframe and match test data.
        print(document_df.columns)
        print(document_df.count)
        print(document_df.head(10))
        assert np.array_equal(document_df.columns,  ['id', 'title', 'body', 'document_update_dt'])

