import sys
sys.path.append('../sql')
from DAL import DAL 


class ModelInterface:

    def __init__(self) -> None:
        self._dal = DAL()
        
    def pre_process(self):
        pass

    def train(self):
        pass

    def predict(self,unseen_doc):
        pass

