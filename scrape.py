# --coding:utf-8--
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
import urllib
import re
import os
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

EMAIL = '********'
PASSWORD = '********'
URL = 'https://en-gb.facebook.com/login/'
driver = webdriver.Chrome()
driver.get(URL)
time.sleep(1)

#   
time.sleep(2)
#                           
driver.find_element_by_name('email').send_keys(EMAIL) 
time.sleep(2)
#
driver.find_element_by_name('pass').send_keys(PASSWORD)
time.sleep(2)
driver.find_element_by_name('login').click()
cookie=driver.get_cookies()
time.sleep(3)
driver.get('https://www.facebook.com/groups/1717731545171536/')
time.sleep(3)
def execute_times(times, driver):
    for i in range(times + 1):
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print i
execute_times(250, driver)

base=r'Users/nyfkxj/web_crawler/meme_archive/images'
url = driver.page_source
data = {}
i = 0;
soup = BeautifulSoup(url, "lxml")
for story in soup.select('div[class*="_5pcr fbUserStory"]'):
    aTag = story.select('a[class*="_4-eo _2t9n"]')
    if len(aTag) != 0:
        imgURL = aTag[0]['data-ploi'];
    #    urllib.urlretrieve(imgURL, os.getcwd())
        timeTag = story.select('abbr[class*="timestamp"]')
        likeTag = story.select('span[class*="_4arz"]')
        descriptionTag = story.select('div[class*="_5pbx userContent"]')
        
        if len(timeTag) and len(likeTag) and len(timeTag):
            post_time = timeTag[0]['title']
            likeTag2 = likeTag[0].select('span')[0].contents
            likeString = likeTag2[0]
            if len(descriptionTag):
                description = descriptionTag[0].find('p').getText()
            else:
                description = ''
            data[i] = []
            data[i].append({'hotness':likeString, 'time': post_time, 'image': imgURL, 'description_text': description})
        i = i + 1
with open('data_with_description.json', 'w') as outfile:
    json.dump(data, outfile)


 

