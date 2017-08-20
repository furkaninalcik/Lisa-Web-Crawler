
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
        'Kullanici Adi' + '\t\t' + 'Takipci Sayisi' + '\t\t' + 'Fotograf ID' + '\t\t' + 'Fotograf Link' + '\t\t' + 'Hashtags' + '\t\t' + 'Location exists?' + '\t\t' + 'Location:' + '\t\t' + 'Likes' + '\n\n')

    influencer_count = 0  # number of influencers whose profiles are going to be crawled

    for influencer in influencers[5:]:
        link = 'http://instagram.com/' + influencer + '/'

        collecting_media = True

        if influencer_count == 1:
            break
        influencer_count += 1
        print(link)

        driver = webdriver.Chrome()
        driver.get(link)
        tree = html.fromstring(driver.page_source)

        driver2 = webdriver.Chrome()



        while True:  # recursion ile degistir?
            try:

                # driver.find_element_by_link_text('Load more')    #this line is to check NoSuchElementException
                driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div')

                for i in range(1, 5):
                    for j in range(1, 4):
                        print('UU')
                        print(str(i))
                        print(str(j))
                        print(i+j)

                        media = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div[1]/div[%d]/div[%d]' % (i, j))
                        print(media)

                        media_link = media.find_element_by_css_selector('a').get_attribute('href')
                        print(media_link)
                        print('A')
                        driver2.get(media_link)  # opens a new window/tab in the browser for each media
                        print('B')

                        tree2 = html.fromstring(driver2.page_source)
                      
                        photo_link = tree2.xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div/div[1]/div[1]/img/@src')
                        if photo_link:
                        	photo_link = photo_link[0]
                        else:
                        	photo_link = 'video'

                        print(photo_link)
                        html_datetime = driver2.find_element_by_css_selector('time').get_attribute('datetime')
                        print('C')

                        photo_timestamp = timestamp(html_datetime)
                        if int(time.time()) - int(photo_timestamp) < 259200:  # media posted in the last 3 days


                            print('a')

                            num_of_followers = tree.xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/span/span/@title')[0]


                            print('b')

                            # num_of_followers = num_of_followers.get_attribute('title').text

                            print(num_of_followers)

                            num_of_media = driver.find_element_by_xpath(
                                '//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[1]/span/span')

                            print(num_of_media.text)

                            try:

                                hashtags = driver2.find_elements_by_xpath(
                                    '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[1]/span/a')

                                hashtag_list = []

                                for x in range(1, len(hashtags) + 1):
                                    print('HASHTAG: ' + hashtags[x - 1].text)
                                    hashtag_list.append(hashtags[x - 1].text)

                                location = driver2.find_elements_by_xpath(
                                    '/html/body/div[4]/div/div[2]/div/div[2]/div/article/header/div/div[2]')

                            except selenium.common.exceptions.NoSuchElementException as e:
                                print('No hashtag')

                            likes = driver2.find_element_by_xpath(
                                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span/span')
                            likes = likes.text

                            creation_time = html_datetime

                            try:
                                location = driver2.find_element_by_xpath(
                                    '//*[@id="react-root"]/section/main/div/div/article/header/div/div[2]/a').text
                                location_info = 1
                                
                            except selenium.common.exceptions.NoSuchElementException as e:
                                location = 'N/A'
                                location_info = 0

                            influencer_info.write(influencer + '\t\t' + num_of_followers + '\t\t' + influencer + '_' + str(creation_time) + '\t\t' + photo_link + '\t\t' + str(hashtag_list) +  '\t\t' + str(location_info) + '\t\t' + location + '\t\t' + '\t\t' + '\t\t' + likes + '\n')
                        else:
                            print('STOP!')
                            collecting_media = False
                        if collecting_media == False:
                            break
                    if collecting_media == False:
                        break
                if collecting_media == False:
                    break
                else:
                    print('NEXT PAGE')
                    link = driver.find_element_by_link_text('Load more').get_attribute('href')
                    driver.get(link)

            except selenium.common.exceptions.NoSuchElementException as e:
                print('LAST PAGE')
                break

        driver.close()
        driver2.close()


crawler()
