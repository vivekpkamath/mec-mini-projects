create database if not exists diabetes_type_2;

use diabetes_type_2;

#
# All documents scraped from web
#
CREATE TABLE if not exists documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    body TEXT,
    document_update_dt DATETIME    
);


#
# model training 
# job_type - 1 = topic model training
#            2 = document sentiment scoring
#

CREATE TABLE if not exists model_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_dt DATETIME,
    job_type INT,
    model_type varchar(255),
    job_processed INT,
    comment varchar(255)
);

#
# All models trained - sentiment models may not be trained
#
CREATE TABLE if not exists models (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type varchar(255),
    model_pkl LONGTEXT,
    bow_pkl LONGTEXT,
    dictionary_pkl LONGTEXT,
    updated_dt DATETIME,
    isCurrent TINYINT,
    job_id INT,
    FOREIGN KEY(job_id)
        REFERENCES model_jobs(id)

);

#
# model metrics for models
# for topic models following metrics are kept
#     avg_coherence_cv FLOAT
#    avg_coherence_umass FLOAT
#    model_perplexity FLOAT
# For sentiment models, confusion matrix is kept
#
CREATE TABLE if not exists model_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_id INT,
    metric_name VARCHAR(255),
    metric_value VARCHAR(255),
    FOREIGN KEY(model_id)
        REFERENCES models(id)
);


#
# topics found in documents
#
CREATE TABLE if not exists topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_id INT,
    topic LONGTEXT,
    FOREIGN KEY (model_id)
      REFERENCES models(id)    
);

#
# sentiment for each document
#

CREATE TABLE if not exists document_sentiment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sentiment INT,
    sentiment_update_dt DATETIME,
    document_id INT,
    model_id INT,
    FOREIGN KEY(document_id)
        REFERENCES documents(id),
    FOREIGN KEY(model_id)
        REFERENCES models(id)
);