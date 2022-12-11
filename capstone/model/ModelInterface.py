import sys
sys.path.append('../sql')
from DatabaseIO import DatabaseIO 


class ModelInterface:

    def __init__(self, db_io ) -> None:
        self._db_io = db_io
        
    def pre_process(self):
        pass

    def train(self):
        pass

    def predict(self,unseen_doc):
        pass

