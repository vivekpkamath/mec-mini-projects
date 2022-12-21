import sys
sys.path.append('../sql')
sys.path.append('../model')
from DAL import DAL 
from TopicModel import TopicModel
from BERTTopicModel import BERTTopicModel
from AFINNSentimentModel import AFINNSentimentModel
from VADERSentimentModel import VADERSentimentModel
import schedule
import time

def job():
    # Get the first incomplete jobs
    # process one at a time
    # store results back in database
    dal = DAL()
    
    records = dal.getFirstUnprocessedModelJobs()
    for record in records:
        #
        #based on the informaiton in record, kick off
        #appropriate model and preprocessing routine
        #
        print(record)
        model_type = record[3]
        print(model_type)
        if model_type == 'topicLDA':
            model = TopicModel()
        elif model_type == 'BERTopic':
            model = BERTTopicModel()
        elif model_type == 'AFINNSentiment':
            model = AFINNSentimentModel()
        elif model_type == 'VADERSentiment':
            model = VADERSentimentModel()
        else:
            print('invalid model type ' + model_type)
            return
        
        model.pre_process()
        model.train()
        
        #update the database to indicate job's done
        print(record[0])
        dal.updateModelJobToProcessed(record[0])

    #Next job will be picked up in the next run - this wakes up every minute


if __name__ == '__main__':

    schedule.every(1).minutes.do(job)
    print('job scheduled for every 1 minute')
    while 1:
        schedule.run_pending()
        time.sleep(1)