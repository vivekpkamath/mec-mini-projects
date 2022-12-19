import sys
sys.path.append('../sql')
from DAL import DAL 

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
    return request.json
#
# API to to get list of model metrics for a given trained model
# 
@app.route('/model/metrics/', methods=['GET'])
def model_metrics(id):
    return request.json

#
# document related APIs
#
#
# API to score topic on unseen document
#
@app.route('/document/topic/', methods=['POST'])
def document_topic(unseen_doc):
    return request.json

#
# API to score sentiment on unseen document
#
@app.route('/document/sentiment/', methods=['POST'])
def document_sentiment(unseen_doc):
    return request.json

if __name__ == '__main__':

    app.run('localhost',port=8080)
    