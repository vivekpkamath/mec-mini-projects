from DatabaseIO import DatabaseIO
from datetime import datetime
import pandas as pd

'''
Data Access Layer for all models and such.  This will keep 
everything abstracted from all applications.  Primary interface
in and out is dataframe
'''
class DAL:

    def __init__(self) -> None:
        self._db_io = DatabaseIO()

    '''
        Documents DAL Section
    '''
    def getAllDocuments(self):
        return self._db_io.read_to_dataframe('select * from documents;')

    def getOneDocument(self, id):
        params = dict()
        params['id'] = id
        return self._db_io.query('select * from documents where id = %(id)s', params=params)

    '''
        Models DAL Section
    '''
    def getCurrentModelOfType(self, model_type):
        get_model = 'select * from models where isCurrent = 1 and type=%(model_type)s'
        params = dict()
        params['type'] = model_type
        rows =  self._db_io.query(get_model, params=params)
        if (len(rows) != 1):
            print('more than one or no active model - how did this happen?')
        return rows
        
    def getCurrentModelId(self, model_type):
        params = dict()
        params['type'] = model_type
        return self._db_io.query('select id from models where isCurrent=1 and type = %(model_type)s',params)
        

    def addOneModel(self, model_type, model_pkl, bow_pkl, dictionary_pkl):
        add_model = 'insert into models (type,model_pkl,bow_pkl, dictionary_pkl, updated_dt, isCurrent)  \
                        VALUES (%(model_type)s, %(model_pkl)s, %(bow_pkl)s, %(dictionary_pkl)s, %(updated_dt)s, %(isCurrent)s ); \
                        select LAST_INSERT_ID();'
        update_current = 'update models set isCurrent = 0 where isCurrent = 1 and type = %(model_type)s;'
        update_param = dict()
        params['type'] = model_type
        self._db_io.execute( update_current, update_param)
        self._db_io.commit()

        params = dict()
        params['model_type'] = model_type
        params['model_pkl'] = model_pkl
        params['bow_pkl'] = bow_pkl
        params['dictionary_pkl'] = dictionary_pkl
        params['updated_dt'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        params['isCurrent'] = '1'      

        self._db_io.execute(add_model, params )
        self._db_io.commit()
        return self._db_io.fetch_one()
    '''
        Topics DAL Section
    '''
    def getTopicsforModel(self, model_id):
        params = dict()
        params['model_id'] = model_id
        return self._db_io.query('select * from topics where model_id= %(model_id)s ;', params)
        

    def addTopicforModel(self, model_id, topic):
        add_topic = 'insert into topics ( model_id, topic) values ( %(model_id)s, %(topic)s); \
                        select LAST_INSERTED_ID();'
        params = dict()
        params['model_id'] = model_id
        params['topic'] = topic
        self._db_io.execute(add_topic, params )
        self._db_io.commit()
        return self._db_io.fetch_one()

    '''
        Metrics DAL Section
    '''

    def getModelMetrics(self, model_id):
        params = dict()
        params['model_id'] = model_id
        return self._db_io.query('select * from model_metrics where model_id = %(model_id)s;', params)
        

    def addModelMetric(self, model_id, metric_name, metric_value):
        add_metric = 'insert into model_metrics (model_id,metric_name,metric_value)  \
                        VALUES (%(model_id)s, %(metric_name)s, %(metric_value)s); \
                        select LAST_INSERT_ID();'
        params = dict()
        params['model_id'] = model_id
        params['metric_name'] = metric_name
        params['metric_value'] = metric_value

        self._db_io.execute(add_metric, params )
        self._db_io.commit()
        return self._db_io.fetch_one()
        

    '''
        Jobs DAL Section
    '''
    def addModelJob(self, job_dt, job_type, comment):

        add_job = 'insert into model_jobs (job_dt, job_type, job_processed, comment) values \
                    (%(job_dt)s, %(job_type)s, 0, %(comment)s); \
                    select LAST_INSERT_ID();'
        params = dict()
        params['job_dt'] = job_dt
        params['job_type'] = job_type
        params['comment'] = comment
        self._db_io.execute(add_job, params )
        self._db_io.commit()
        return self._db_io.fetch_one()
        
    def getUnprocessedModelJobs(self):
        return self._db_io.query('select * from model_jobs where job_processed = 0;')
        

    def getProcessedModelJobs(self):
        return self._db_io.query('select * from model_jobs where job_processed = 1;')

    def updateModelJobToProcessed(self, job_id):
        update_job = 'update model_jobs set job_processed = 1 where id = %(job_id)s'
        params = dict()
        params['job_id'] = job_id
        self._db_io.execute(update_job)
        self._db_io.commit()        
        