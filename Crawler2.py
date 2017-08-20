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


def timestamp(html_datetime):
    d = datetime.strptime(html_datetime, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%s')
    d_in_ms = int(d)
    print(d_in_ms)
    print(datetime.fromtimestamp(float(d)))
    return d_in_ms


def crawler():
    influencer_info = open('influencer_info', 'w')

    with open('influencer_list') as inf_list:
        influencers = inf_list.readlines()
    influencers = [x.strip() for x in influencers]

    influencer_info.write(
        'Kullanici Adi' + ' ' + 'Takipci Sayisi' + ' ' + 'Fotograf ID' + ' ' + 'Post Link' +' ' + 'Fotograf Link' + ' ' + 'Hashtags' + ' ' + 'Location exists?' + ' ' + 'Location:' + ' ' + 'Likes' + '\n')


    for influencer in influencers[6:9]: #the indices are for testing
        link = 'http://instagram.com/' + influencer + '/'

        collecting_media = True


        driver = webdriver.Chrome()
        driver.get(link)
        tree = html.fromstring(driver.page_source)

        driver2 = webdriver.Chrome()

        while collecting_media:

                for i in range(1, 5):
                    for j in range(1, 4):


                        media = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div[1]/div[%d]/div[%d]' % (i, j))

                        media_link = media.find_element_by_css_selector('a').get_attribute('href')
                        driver2.get(media_link)  # opens a new window/tab in the browser for each media

                        tree2 = html.fromstring(driver2.page_source)
                      
                        photo_link = tree2.xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div/div[1]/div[1]/img/@src')
                        if photo_link:
                        	photo_link = photo_link[0]
                        else:
                        	photo_link = 'video'

                        html_datetime = driver2.find_element_by_css_selector('time').get_attribute('datetime')

                        photo_timestamp = timestamp(html_datetime)
                        if int(time.time()) - int(photo_timestamp) < 259200:  # media posted in the last 3 days


                            num_of_followers = tree.xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/span/span/@title')[0]


                            num_of_media = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[1]/span/span')

                            try:

                                hashtags = driver2.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[1]/span/a')

                                hashtag_list = []

                                for x in range(1, len(hashtags) + 1):
                                    hashtag_list.append(hashtags[x - 1].text)

                            except selenium.common.exceptions.NoSuchElementException as e:
                                hashtag_list = []
                                

                            likes = driver2.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span/span')
                            likes = likes.text

                            creation_time = str(photo_timestamp)

                            try:
                                location = driver2.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div/div[2]/a').text
                                location_info = 1
                                
                            except selenium.common.exceptions.NoSuchElementException as e:
                                location = 'N/A'
                                location_info = 0

                            influencer_info.write(influencer + ' ' + num_of_followers + ' ' + influencer + '_' + creation_time + ' '+  media_link + ' ' + photo_link + ' ' + str(hashtag_list) +  ' ' + str(location_info) + ' ' + location + ' ' + likes + '\n')
                        else:
                            collecting_media = False
                        if collecting_media == False:
                            break
                    if collecting_media == False:
                        break
                else:
                    link = driver.find_element_by_link_text('Load more').get_attribute('href')
                    driver.get(link)


        driver.close()
        driver2.close()


crawler()
