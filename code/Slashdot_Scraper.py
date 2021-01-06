# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:24:41 2017

@author: ABUSALEH
"""
from http.client import RemoteDisconnected
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as Soup 
from pymongo import MongoClient
import requests
import re
import sys
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException


client = MongoClient()

list_of_comments = []

######only facebook related posts matching
kwd_match = lambda kwd: re.compile(f"{'|'.join(kwd)}", flags=re.IGNORECASE).search
keywords = ['facebook']


######loading the browser in selenium
def get_browser(headless=False, extensions=False, notifications=False, incognito=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    
    if not extensions:
        chrome_options.add_argument("--disable-extensions")
    
    if not notifications:
        chrome_options.add_argument('--disable-notifications')
    
    if incognito:
        chrome_options.add_argument('--incognito')

    driver = webdriver.Chrome(executable_path='C:\\Users\\ABUSALEH\\Desktop\\Cavin_Slashdot\\chromedriver.exe',
                              options=chrome_options)
    return driver


    
def dictify(tag, cls_val):

    result={}
    #print(ok)
    for container in tag.find_all('div', {'class':re.compile('cw'), 'id': re.compile('comment')}, recursive=False):
        
        new_containers = container.find('div', {'id': re.compile('^comment_top')})
        
        #print(new_containers)
        if new_containers is not None:
            list1 = [a for a in new_containers.contents if a != '\n']
        
        
        #print(list1)
        
            for item in list1:
                
                if item['class'][0] == 'title':
                    #print('test')
                    result['comment_header'] = item.h4.a.text
                    href = 'https:'+item.h4.a['href'].strip()
                    result['comment_score'] = item.h4.span.a.text
                    #print(item.h4.span.text)
                    result['comment_type'] = item.h4.span.text
                
                elif item['class'][0] == 'details':
                    list2 = [a for a in item.contents if a != '\n']
                    for val in list2:
                        #name_tag2 = val.name
                        if val['class'][0]== 'by':
                            result['commenter'] = val.text
                            
                        elif val['class'][0]== 'otherdetails':
                            
                            if cls_val == 'comment oneline':
                                temp  = requests.get(href)
                                html = temp.text
                                new_soup = Soup(html, "lxml")
                                new_temp = new_soup.find('ul', {'id': 'commentlisting', 'class':'d2'}).find('li', {'class':re.compile('comment'), 'id': re.compile('tree')})\
                                .find('div', {'class':re.compile('cw'), 'id': re.compile('comment')})\
                                .find('div', {'id': re.compile('^comment_top')}).find('div', class_='details')\
                                .find('span', class_='otherdetails')
                                result['comment_time'] = new_temp.text.strip()
                                
                            else:    
                                result['comment_time'] = val.text.strip()
        
        another_container = container.find('div', {'class': 'commentBody'})
        
        if another_container is not None:
            result['comment_body'] = another_container.div.text.strip()
    #print(result)
            
    if result:
        list_of_comments.append(result)
        
    if tag.find('ul', {'id': re.compile('commtree')}, recursive=False):
        
        #print(tag)
        for commtree in tag.find_all('ul', {'id': re.compile('commtree')}, recursive=False):
            #list_of_comments.append(result)
            #print(commtree)
            retrieve_comments(commtree)
    else:
        return 
        
        
def retrieve_comments(new_soup):
       
    tags = new_soup.find_all('li', {'class':re.compile('comment'), 'id': re.compile('tree')}, recursive=False)
    
    for tag in tags:
        try:
            #print(create_soup(tag))
            class_val = ' '.join(tag['class'])
            dictify(tag, class_val)
             
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
            continue
        

list_of_dict = []

for i in range(137,165):    #set desired page range
    my_url = 'https://slashdot.org/?page={}'.format(i)
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    driver = get_browser(headless=False, incognito=True)
    try:
        driver.set_page_load_timeout(40)
        driver.get(my_url)
    except TimeoutException:
        print(f"\t{my_url} - Timed out receiving message from renderer")
        continue
    except RemoteDisconnected:
        print(f"\tError 404: {my_url} not found.")
        continue
        
    WebDriverWait(driver, timeout=40).until(EC.presence_of_element_located((By.ID, "fhft")))
    #soup = BeautifulSoup(driver.page_source, "html.parser")
    page_soup = Soup(driver.page_source, "lxml")
    containers = page_soup.findAll('article', {'class':'fhitem fhitem-story article usermode thumbs grid_24'})
    #print(len(containers))
    
    
    for container in containers:
        list_of_comments = []
        record = {}
        record['details'] = container.header.div.find('span', class_='story-byline').text.strip()
        record['category'] = container.header.span.a.img['title']
        record['title'] = container.header.h2.span.a.text
        #record['body_of_post'] = container.div.div.text
        link = 'https:' + container.header.h2.span.a['href']

        if not kwd_match(keywords)(link):
            continue
        
        r  = requests.get(link)
        data = r.text
        another_page_soup = Soup(data, "lxml")
        pge_soup = another_page_soup.find('ul', {'id': 'commentlisting', 'class':'d2'})
        retrieve_comments(pge_soup)
        record['comments'] = list_of_comments
        
        list_of_dict.append(record)
        

#####create appropriate MongoDB database and load. Change the DB name accordingly here:        
db =client.test_db.slashdot_data.insert_many(list_of_dict)

