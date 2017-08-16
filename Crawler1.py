# -*- coding: utf-8 -*-
from lxml import html
import requests
import sys
import urllib


def crawler():
    
    influencer_list = open('influencer_list' , 'w')


    for j in range(1,5):
        link = "http://influence.iconosquare.com/category/all/" + str(j)

        influencerPage = requests.get(link)
        influencerPageTree = html.fromstring(influencerPage.content)
	    
        for i in range(1,30):
	       
            influencer = influencerPageTree.xpath('//*[@id="home-top-brands"]/div[2]/table/tbody[1]/tr[%d]/td[1]/a/p' % i)
            #print(link)    
            #influencer_list.write('\t_(' + str(i+((j-1)*29)) + ')_\t\t' + influencer[0].text + '\n')
            
            influencer_list.write(influencer[0].text + '\n')
            
            #influencer_list.write(i)
            #print (influencer[0].text)

    influencer_list.close()

crawler()

