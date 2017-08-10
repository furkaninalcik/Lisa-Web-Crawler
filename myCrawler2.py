# -*- coding: utf-8 -*-
from lxml import html
import requests
import sys
import urllib

users = []





'//*[@id="home-top-brands"]/div[2]/table/tbody[1]/tr[1]'


'//*[@id="home-top-brands"]/div[2]/table/tbody[1]/tr[2]'

'//*[@id="home-top-brands"]/div[2]/table/tbody[1]'


def crawler():
    
    influencer_list = open('influencer_list' , 'w')


    for j in xrange(1,5):
        link = "http://influence.iconosquare.com/category/all/" + str(j)
        influencerPage = requests.get(link)
        influencerPageTree = html.fromstring(influencerPage.content)
	    
        for i in xrange(1,30):
	       
            influencer = influencerPageTree.xpath('//*[@id="home-top-brands"]/div[2]/table/tbody[1]/tr[%d]/td[1]/a/p' % i)
            influencer_list.write(str(i+((j-1)*29)) + ") " + influencer[0].text + '\n')
            #influencer_list.write(i)
            #print (influencer[0].text)

    influencer_list.close()

crawler()

