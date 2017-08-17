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

def convertToInteger(text):
	index = 0
	for x in range(1,len(text)):
		index += 1 
		if text[x] == ',':
			break
	return int((text[:index] + text[index+1:]).strip(" posts"))

def timestamp(html_datetime):


    d = datetime.strptime(html_datetime, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%s')
    d_in_ms = int(d)
    print(d_in_ms)
    print(datetime.fromtimestamp(float(d)))
    return d_in_ms


def crawler():

    influencer_info = open('influencer_info' , 'w')

    with open('influencer_list') as inf_list:
        influencers = inf_list.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    influencers = [x.strip() for x in influencers] 
    
    influencer_info.write('Kullanici Adi' + '\t\t' + 'Kullanici No' +'\t\t' + 'Takipci Sayisi' +'\t\t'+ 'Fotograf No' +'\t\t'+ 'Fotograf Link'+'\t\t' + 'Location'+'\t\t' + 'Hashtag' + '\n\n')

    index_count = 0

    

    for influencer in influencers:
        link = 'http://instagram.com/' + influencer + '/'
        #link = 'http://instagram.com/zachking/'

        collecting_media = True
        
        if index_count == 2:
        	break
        index_count += 1
        print(link)        

        driver = webdriver.Chrome()
        driver2 = webdriver.Chrome()
        
        driver.get(link)
        
        num_of_posts_text = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[1]')
        
        page_number = convertToInteger(num_of_posts_text.text) / 12

        print( 'Number of Posts:' + str(convertToInteger(num_of_posts_text.text)))

        for page in range(1,page_number):
        	
            for i in range(1,5):
                for j in range(1,4):


                    photo  = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div[1]/div[%d]/div[%d]' % (i , j))

                    photo_link = photo.find_element_by_css_selector('a').get_attribute('href')

                    
                    driver2.get(photo_link)

                    html_datetime = driver2.find_element_by_css_selector('time').get_attribute('datetime')

                    
                    photo_timestamp = timestamp(html_datetime)
                    if int(time.time()) - int(photo_timestamp) < 172800: #media posted in the last 2 days
                    	
                    	print('DIFF : ' + str(int(time.time()) - int(photo_timestamp)))
                    	print(int(time.time()))
                    	print(int(photo_timestamp))

                        influencer_name = influencer

                        index = str(index_count)
        
                        num_of_followers = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]')
 
                        print(num_of_followers.text)
       
                        num_of_media = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[1]')

                        print(num_of_media.text)
                    
                        #timestamp = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[2]/div/article/div[2]/div[2]/a/time')

                        photo_no = index + '_' + str((i-1)*3 + j)
 
                        #hashtags = driver2.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[1]/span')
                        
                        try:
                            #hashtag_link = hashtags.find_element_by_css_selector('a').get_attribute('href')
                            
                            hashtags = driver2.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[1]/span/a')

                            for i in range(1,len(hashtags)+1):
                                print('HASHTAG: ' + hashtags[i-1].text)
                        except selenium.common.exceptions.NoSuchElementException as e:
                            print('No hashtag')
                        	

                            
    

                        influencer_info.write(influencer_name + '\t\t'  + index + '\t\t' + num_of_followers.text + '\t\t' + photo_no + '\t\t' + num_of_media.text + '\t\t' + photo_link  + '\n')
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
                link = driver.find_element_by_link_text('Load more').get_attribute('href')           
                driver.get(link)


        driver.close()


crawler()

