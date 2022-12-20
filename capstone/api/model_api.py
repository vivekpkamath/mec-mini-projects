import sys
sys.path.append('../sql')
sys.path.append('../model')

from DAL import DAL 
from TopicModel import TopicModel
from BERTTopiceModel import BERTTopicModel
from AFINNSentimentModel import AFINNSentimentModel
from VADERSentimentModel import VADERSentimentModel

from flask import Flask
from flask import jsonify
from flask import request
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/test/', methods=['GET','POST'])
def test():
    if request.method == 'GET':
        return jsonify({'name':'testname','value':'testvalue'})
    elif request.method == 'POST':
        print('********POST received')
        return request.json
#
# Document job API
#
#
# API on model_jobs
#
@app.route('/model_job/', methods=['GET','POST'])
def model_job():
    print('model_job: ' + request.method, file=sys.stderr)
    if request.method == 'POST':
        #create new job
        dal = DAL()
        data = request.get_json()
        print(data, file=sys.stderr)
        job_id = dal.addModelJob(datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'), data['job_type'], data['model_type'], data['comment'])
        return json.dumps({'job_id':job_id}), 200, {'Content-Type':'application/json'} 
    elif request.method == 'GET':
        #Get all jobs from the database and send them back to the client
        
        dal = DAL()
        jobs = dal.getAllJobs()
        return json.dumps( jobs,default=str ), 200, {'Content-Type':'application/json'} 
    else:
        Flask.abort(404, 'Not Supported')
    
    
#
# API to get list of trained models.  Only GET here.  models are added by 
# CRON based on training job request
#
@app.route('/model/', methods=['GET'])
def model():
    if request.method == 'GET':
        #Get all jobs from the database and send them back to the client
        
        dal = DAL()
        models = dal.getAllCurrentModels()

        return json.dumps( models,default=str ), 200, {'Content-Type':'application/json'} 
    else:
        Flask.abort(404, 'Not Supported')


#
# API to to get list of model metrics for a given trained model
# 
@app.route('/model/metrics/', methods=['GET'])
def model_metrics(model_id):
    #get all metrics if any for a given model
    if request.method == 'GET':
        #Get all jobs from the database and send them back to the client
        
        if model_id is None:
            Flask.abort(404, 'Not Supported')
        else:
            dal = DAL()
            metrics = dal.getModelMetrics(model_id)

            return json.dumps( metrics,default=str ), 200, {'Content-Type':'application/json'} 
    else:
        Flask.abort(404, 'Not Supported')


#
# document related APIs
#
#
# API to score topic on unseen document with current model for given type
#
@app.route('/document/topic/', methods=['POST'])
def document_topic():

    if request.method == 'POST':
        
        data = request.get_json()
        dal = DAL()
        # Move this to a factory
        model_type = data['model_type']
        if model_type == 'topicLDA':
            model = TopicModel()
        elif model_type == 'BERTopic':
            model = BERTTopicModel()
        else:
            Flask.abort(404, 'Not Supported')
            return    

        prediction = model.predict(data['unseen_document'])

        return json.dumps( prediction,default=str ), 200, {'Content-Type':'application/json'} 
    else:
        Flask.abort(404, 'Not Supported')

#
# API to score sentiment on unseen document
#
@app.route('/document/sentiment/', methods=['POST'])
def document_sentiment(unseen_doc):
    if request.method == 'POST':
        
        data = request.get_json()
        dal = DAL()
        # Move this to a factory
        model_type = data['model_type']

        if model_type == 'AFINNSentiment':
            model = AFINNSentimentModel()
        elif model_type == 'VADERSentiment':
            model = VADERSentimentModel()
        else:
            Flask.abort(404, 'Not Supported')
            return    

        prediction = model.predict(data['unseen_document'])

        return json.dumps( prediction,default=str ), 200, {'Content-Type':'application/json'} 
    else:
        Flask.abort(404, 'Not Supported')

if __name__ == '__main__':

    app.run('localhost',port=8080)
    