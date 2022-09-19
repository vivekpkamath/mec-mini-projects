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
#
# should we create tables for ingestion timeline
#
