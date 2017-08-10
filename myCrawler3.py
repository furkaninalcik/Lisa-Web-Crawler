# -*- coding: utf-8 -*-
from lxml import html
import requests
import sys
import urllib

users = []




#CATEGORY XPATH
#'//*[@id="home-top-brands"]/div[2]/table/tbody[1]/tr[1]/td[3]/ul/li/a'
#//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a/span

def crawler():
    
    with open('influencer_list') as inf_list:
        influencers = inf_list.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    influencers = [x.strip() for x in influencers] 


    for influencer in influencers:

        link = 'https://www.instagram.com/' + influencer
        influencerPage = requests.get(link)
        influencerPageTree = html.fromstring(influencerPage.content)
	    
        influencer_follower = influencerPageTree.xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a/span')
        if len(influencer_follower) > 0:
            
            number_of_followers = influencer_follower[0].text
            print(str(number_of_followers) + '\n')
        
            #number_of_followers = influencer_follower[0].text
            #print(str(number_of_followers) + '\n')
                
    #influencer_list.close()

crawler()

