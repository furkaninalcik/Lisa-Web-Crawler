# -*- coding: utf-8 -*-
from lxml import html
import requests
import sys
import urllib

users = []

with open(sys.argv[1], 'r') as f:
    for line in f:
        users.append(line.strip("\n"))

def get_user_page_data(link,name,userId, userData, inlineId, tp):
    userPage = requests.get(link)
    userPageTree = html.fromstring(userPage.content)

    inlinePhotoId = inlineId
    totalPost = tp
    nextUrl = ""
    for userPostBox in userPageTree.xpath('//*[@id="social-container"]/article'):
        userInstagramPhotoUrl = userPostBox.xpath('div/div[@class="panel-body"]/div[@class="content-image image"]/a/img/@src')
        if len(userInstagramPhotoUrl) != 0:
            urllib.urlretrieve(userInstagramPhotoUrl[0], str(userId) + "_" +str(inlinePhotoId) + ".jpg")
            likesayisi = userPostBox.xpath('div/div/div/span[@class="like"]/text()')[1].strip(" \n\t\r")
            totalPost += 1
            # pictaramUserMediaUrl = userPostBox.xpath('div/div[@class="panel-body"]/div/a/@href')[0]

            time = userPostBox.xpath('div/div/div/span[@class="time"]/text()')[0].strip(" \n\t\r").replace(" ", "-")

            location = userPostBox.xpath('div/div[@class="comments-like"]/div[@class="location"]/a/text()')
            if len(location) == 0:
                locationCount = 0
            else:
                locationCount = 1

            hashtags = []
            for tags in userPostBox.xpath('div/div[@class="panel-body"]/p[@class="content"]/a/text()'):
                hashtags.append(tags)

            if len(hashtags) == 0:
                hashtagCount = 0
            else:
                hashtagCount = 1

            userData.write(name + " " + str(userId) + " " + str(likesayisi) + " " + str(userId) + "_" +str(inlinePhotoId) + " " +str(locationCount)+ " " +str(hashtagCount) + " " + time+ "\n")
            inlinePhotoId += 1
    print (totalPost)

    if(totalPost <= 10):
        if len(userPageTree.xpath('/html/body/nav[@class="next-cont"]/a/@href')) != 0:
            nextUrl = userPageTree.xpath('/html/body/nav[@class="next-cont"]/a/@href')
    if nextUrl:
        get_user_page_data(str(nextUrl[0]),name,userId, userData, inlinePhotoId, totalPost)

userId = int(sys.argv[2]);
with open(sys.argv[2] + ".txt", "w") as userData:
    for u in users:
        searchPage = requests.get("http://www.pictaram.com/search?query=" + str(u))
        searchTree = html.fromstring(searchPage.content)

        for el in searchTree.xpath('/html/body/section/div/div/article'):
            for userLink in el.xpath('div/div/div/div/a/@href'):
                if u == userLink.split("/")[4]:
                    print ("Instagram user " + u + " is found in Pictagram search")
                    print ("Kullanici Instagram Id = " + userLink.split("/")[5])
                    get_user_page_data(userLink,u,userId, userData, 0, 0)
                    userId += 1

# for u in users:
#     searchPage = requests.get("http://www.pictaram.com/search?query=" + str(u))
#     parsedPage = BeautifulSoup(searchPage.content, 'html.parser')
#
#     for article in parsedPage.find_all('article', class_="item"):
#         for userLink in article.find_all('div', class_="content-image"):
#             print userLink
#
