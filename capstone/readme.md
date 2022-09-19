# Capstone Project - Sentiment Analysis(SA) and Topic Discovery on Type 2 Diabetes Social Media and Forum Data

## Motivation

Sentiment Analysis (SA) is used quite extensively in the context of retail industry, marketing,  politics and many such fields.  However, one area lacking is health care.  Because of the COVID-19 pandemic a lot of people with diseases of high severity and chronicity have started relying on several internet forums to provide their experiences in managing diseases, discuss different topics and share their experiences with other members on the forum.  One such chronic disease that is quite prevalent in the world is diabetes.  There are several issues worldwide around this disease that are discussed in many different forums on MEDLINE, diabetes daily, twitter, facebook etc.  The state of one’s health is based on complete physical, mental and social well being and not just absence of disease.  

This project works towards the possibility of discovering topics in threads on this disease and performing sentiment analysis to inform everyone on the forum of several things such as experiences with certain drugs, certain diets, certain procedures and exercises, certain care providers etc.  There are several topics possible in a discussion thread in a forum that might indicate different topics which are lurking in a thread.  If it becomes prevalent, it  will hugely benefit communities around different disease states across the world.

## The What

The question is how does one go about implementing a system like this.  While this is a lofty and altruistic goal, is there any way to actually do SA on diabetes discussion forums.  After doing some digging around and getting inspiration from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7013658/, looks like the answer is yes.

Use the data in this forum on diabetes at: https://www.diabetesdaily.com/forum/.

The focus of this project will be on disease state type 2 diabetes and there are a lot of documents to analyze and train models in this forum.  This forum is used widely and has a lot of rich discussion threads and is open.  It has categorized data around type 1, type 1.5, type 2 diabetes and prediabetes.  There are separate forums for care providers as well.  

The project has two parts:
1. Search for topics in documents and across documents
2. Analyze sentiments in each of the documents.

## The How
1. Get data from forum using web scraping modules like BeautifulSoup
2. Create database schema in mySQL
3. Load documents containing discussion threads retrieved from scraping the forum into database
4. Train topic model using https://github.com/dipanjanS/nlp_workshop_odsc_europe20/blob/master/notebooks/Module_03_NLP%20Applications%20-%20Machine%20and%20Deep%20Learning/09_NLP_Applications_Topic_Modeling.ipynb and https://github.com/MaartenGr/BERTopic
5. Train SA model using XXX
6. Create API to consume model and store data in database

## Structure
This project is organized as follows
 api - API for model training and consumption.  Current thought is to use flask
 data - any local data
 dataloader - python scripts to scrape and load data
 model - topic models and SA models
 notebooks - Jupyter notebooks used for experimentation
 sql - DDL for database
 UI - ui for model.  Current thought is to use streamlit
 readme.md - this readme file
 requirements.txt - python env

