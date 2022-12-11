create database if not exists diabetes_type_2;

use diabetes_type_2;

drop table documents;

CREATE TABLE if not exists documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    body TEXT,
    document_update_dt DATETIME    
);

show tables;

select * from documents;

CREATE TABLE if not exists models (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type varchar(255),
    model_pkl LONGTEXT,
    bow_pkl LONGTEXT,
    dictionary_pkl LONGTEXT,
    avg_coherence_cv FLOAT,
    avg_coherence_umass FLOAT,
    model_perplexity FLOAT,
    updated_dt DATETIME,
    isCurrent TINYINT    
);

CREATE TABLE if not exists topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_id INT,
    topic LONGTEXT,
    FOREIGN KEY (model_id)
      REFERENCES models(id)    
);
#
# should we create tables for ingestion timeline
#
