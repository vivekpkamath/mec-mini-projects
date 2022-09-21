'''
Data loader is responsible for scraping web site and import it into mysql database
'''
import sys
import os

sys.path.append('../sql')
import requests
from bs4 import BeautifulSoup
from DatabaseIO import DatabaseIO
from datetime import datetime

import logging

class DataLoader:

    _delete_all_documents = 'truncate table documents;'
    _add_document = 'insert into documents (title,body,document_update_dt) VALUES (%(title)s, %(body)s, %(document_update_dt)s );'

    def __init__(self, main_url, forum_url, max_pages, start_page):
        #create db connection
        self._dbconn = DatabaseIO()
        self._main_url = main_url
        self._forum_url = forum_url
        self._max_pages = max_pages
        self._start_page = start_page

    def __clean_content(self, content):
        content = content.replace('/', ' ')
        content = content.replace('\n', ' ')
        content = content.replace('\'', ' ')
        return content

    def __get_thread(self, thread_url):        
        one_thread = ""
        r_thread = requests.get(thread_url)
        thread_soup = BeautifulSoup(r_thread.content)
        thread_items = thread_soup.find_all('div', {'class': 'bbWrapper'})
        thread_date_time = thread_soup.find('time',  {'class': 'u-dt'})
        if thread_date_time is not None:
            thread_date_time = thread_date_time['datetime']

        for item in thread_items:
            one_thread = one_thread + item.get_text()
        return thread_date_time, one_thread

    def scrape_all(self):
        threads_added = 0
        for i in range( self._start_page, self._max_pages+1):

            page_url_part = ''
            if (i+1) != 1:
                page_url_part = 'page-' + str(i+1)
            
            r = requests.get(self._main_url+ self._forum_url + page_url_part)
            
            soup = BeautifulSoup(r.content)

            items = soup.find_all('div', {'class': 'structItem-title'})
            print('+++++++++++++++++++++ PAGE ' + str(i))
            for item in items:
                thread_url = item.find('a')['href']
                item_title = item.find('a').contents[0]        
                
                thread_date_time, thread = self.__get_thread(self._main_url+thread_url)
                
                #clean up item - remove forward slash, remove \n and remove single quotes
                item_title = self.__clean_content(item_title)
                thread = self.__clean_content(thread)
                
                #Write thread out to the database
                #Create dictionary for parameters only if some of the parameters are valid
                if (thread is not '') & (thread_date_time is not None):
                    params = dict()
                    params['title'] = item_title
                    params['body'] = thread
                    params['document_update_dt'] = datetime.strptime(thread_date_time, '%Y-%m-%dT%H:%M:%S%z')               
                    #print(params)
                    self._dbconn.execute(self._add_document, params)
                    self._dbconn.commit()
                    threads_added = threads_added+1

            print('--------------------- PAGE ' + str(i))
        return threads_added

    
