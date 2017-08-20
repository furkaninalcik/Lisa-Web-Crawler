# -*- coding: utf-8 -*-
from lxml import html
import requests
import sys
import urllib


def crawler():
    
    influencer_list = open('influencer_list' , 'w')
    
    num_of_pages = 5 #number of pages to be crawled

    for j in range(1,num_of_pages):
        link = "http://influence.iconosquare.com/category/all/" + str(j)

        influencerPage = requests.get(link)
        influencerPageTree = html.fromstring(influencerPage.content)
	    
        for i in range(1,30):
	       
            influencer = influencerPageTree.xpath('//*[@id="home-top-brands"]/div[2]/table/tbody[1]/tr[%d]/td[1]/a/p' % i)
            
            influencer_list.write(influencer[0].text + '\n')

    influencer_list.close()

crawler()

