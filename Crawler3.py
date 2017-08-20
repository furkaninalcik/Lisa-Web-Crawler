
# -*- coding: utf-8 -*-
from lxml import html
import requests
import sys
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import selenium
from lxml import html

with open('influencer_info') as info:
    influencers = info.readlines()
influencers = [x.strip() for x in influencers]

num_of_likes = open('num_of_likes', 'w')

driver = webdriver.Chrome()


for x in influencers[1:]:

    x = x.split(' ')
    print(x[3])
    driver.get(x[3])
    tree = html.fromstring(driver.page_source)
    likes = tree.xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span/span/text()')
                            
    num_of_likes.write( x[2] + ' ' + x[3] + ' ' +  likes[0] +  '\n')

driver.close()
