from flask import Flask
from flask import jsonify
from flask import request

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
    return request.json
#
# API to get list of trained models.  Only GET here.  models are added by 
# CRON based on request
#
@app.route('/model/', methods=['GET'])
def model():
    return request.json
#
# API to to get list of model metrics for a given trained model
# 
@app.route('/model/metrics/', methods=['GET'])
def model(id):
    return request.json

#
# document related APIs
#
#
# API to score topic on unseen document
#
@app.route('/document/topic/', methods=['POST'])
def model(unseen_doc):
    return request.json

#
# API to score sentiment on unseen document
#
@app.route('/document/sentiment/', methods=['POST'])
def model(unseen_doc):
    return request.json

if __name__ == '__main__':
    app.run('localhost',port=8080)
