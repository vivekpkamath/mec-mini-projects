curl -X GET -H "Content-type: application/json" -H "Accept: application/json" http://localhost:8080/model_job/
curl -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d '{"job_type":"1","model_type":"topicLDA", "comment":"test"}'   http://localhost:8080/model_job/
curl -X GET -H "Content-type: application/json" -H "Accept: application/json" http://localhost:8080/model_job/
