from DatabaseIO import DatabaseIO
from datetime import datetime
import pandas as pd
import sys
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
        return self._db_io.read_to_dataframe('select * from documents LIMIT 100;')

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
        params['model_type'] = model_type
        rows =  self._db_io.query(get_model, params=params)
        if (len(rows) != 1):
            print('more than one or no active model - how did this happen?')
        return rows
        
    def getCurrentModelId(self, model_type):
        params = dict()
        params['type'] = model_type
        return self._db_io.query('select id from models where isCurrent=1 and type = %(model_type)s',params)
        
    def getAllCurrentModels(self):
        return self._db_io.query('select * from models where isCurrent=1')

    def addOneModel(self, model_type, model_pkl, bow_pkl, dictionary_pkl):
        add_model = 'insert into models (type,model_pkl,bow_pkl, dictionary_pkl, updated_dt, isCurrent)  \
                        VALUES (%(model_type)s, %(model_pkl)s, %(bow_pkl)s, %(dictionary_pkl)s, %(updated_dt)s, %(isCurrent)s ); \
                        select LAST_INSERT_ID();'
        update_current = 'update models set isCurrent = 0 where isCurrent = 1 and type = %(model_type)s;'
        update_param = dict()
        update_param['model_type'] = model_type
        self._db_io.execute( update_current, update_param)
        self._db_io.commit()

        params = dict()
        params['model_type'] = model_type
        params['model_pkl'] = model_pkl
        params['bow_pkl'] = bow_pkl
        params['dictionary_pkl'] = dictionary_pkl
        params['updated_dt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params['isCurrent'] = '1'      
        
        row = None
        results = self._db_io.execute(add_model, params, multi=True)
        print(results, file=sys.stderr)
        for result in results:
            if result.with_rows:
                row = result.fetchall()

        self._db_io.commit()
        print(row, file=sys.stderr)
        if row is not None:
            return row[0][0]
        return None

    '''
        Topics DAL Section
    '''
    def getTopicsforModel(self, model_id):
        params = dict()
        params['model_id'] = model_id
        return self._db_io.query('select * from topics where model_id= %(model_id)s ;', params)
        

    def addTopicforModel(self, model_id, topic):
        add_topic = 'insert into topics ( model_id, topic) values ( %(model_id)s, %(topic)s ); \
                        select LAST_INSERT_ID();'
                        
        params = dict()
        params['model_id'] = model_id
        params['topic'] = topic
        
        row = None
        results = self._db_io.execute(add_topic, params, multi=True)
        print(results, file=sys.stderr)
        for result in results:
            if result.with_rows:
                row = result.fetchall()

        self._db_io.commit()
        
        
        print(row, file=sys.stderr)
        if row is not None:
            return row[0][0]
        return None

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
        row = None
        results = self._db_io.execute(add_metric, params, multi=True)
        print(results, file=sys.stderr)
        for result in results:
            if result.with_rows:
                row = result.fetchall()

        self._db_io.commit()
        
        
        print(row, file=sys.stderr)
        if row is not None:
            return row[0][0]
        return None
        

    '''
        Jobs DAL Section
    '''
    def addModelJob(self, job_dt, job_type, model_type, comment):
        #job_type  1 = training topic 2 = scoring sentiment on training data
        add_job = 'insert into model_jobs (job_dt, job_type, model_type, job_processed, comment) values \
                    (%(job_dt)s, %(job_type)s, %(model_type)s, 0, %(comment)s); \
                    select LAST_INSERT_ID();'
        params = dict()
        params['job_dt'] = job_dt
        params['job_type'] = job_type
        params['model_type'] = model_type
        params['comment'] = comment
        print(add_job, file=sys.stderr)
        print(params, file=sys.stderr)
        row = None
        results = self._db_io.execute(add_job, params, multi=True)
        print(results, file=sys.stderr)
        for result in results:
            if result.with_rows:
                row = result.fetchall()

        self._db_io.commit()
        
        
        print(row, file=sys.stderr)
        if row is not None:
            return row[0][0]
        return None
        
    def getAllJobs(self):
        return self._db_io.query('select * from model_jobs order by job_dt;')

    def getFirstUnprocessedModelJobs(self):
        return self._db_io.query('select * from model_jobs where job_processed = 0 order by job_dt ASC LIMIT 1;')
        

    def getProcessedModelJobs(self):
        return self._db_io.query('select * from model_jobs where job_processed = 1;')

    def updateModelJobToProcessed(self, job_id):
        update_job = 'update model_jobs set job_processed = 1 where id = %(job_id)s;'
        params = dict()
        params['job_id'] = job_id
        self._db_io.execute(update_job, params=params)
        self._db_io.commit()        
        
    '''
        Sentiment DAL Section
    '''

    def addSentiment(self, model_id, document_id, sentiment):
        add_sentiment = 'insert into document_sentiment (sentiment, model_id, document_id, sentiment_update_dt) \
                            values (%(sentiment)s, %(model_id)s, %(document_id)s, %(sentiment_update_dt)s ); \
                            select LAST_INSERT_ID();'
        
        params = dict()
        params['sentiment'] = sentiment
        params['model_id'] = model_id
        params['document_id'] = document_id
        params['sentiment_update_dt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = None
        results = self._db_io.execute(add_sentiment, params, multi=True)
        print(results, file=sys.stderr)
        for result in results:
            if result.with_rows:
                row = result.fetchall()

        self._db_io.commit()
        print(row, file=sys.stderr)
        if row is not None:
            return row[0][0]
        return None
