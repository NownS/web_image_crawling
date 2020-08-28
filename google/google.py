import sys, os
from bs4 import BeautifulSoup
#pip install bs4
from selenium import webdriver
#pip install selenium
import urllib
import urllib.request
import requests
import random
import time
from selenium.webdriver.common.keys import Keys
import magic
#pip install python-magic

###initial set

folder = "./image/"
url0 = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="
webDriver = "./chromedriver"
searchItem = ["전소민"]
name = ""

print("name : {}".format(searchItem))
for name in searchItem:
    print(name)
    url = url0+name
    browser = webdriver.Chrome(webDriver)
    time.sleep(0.5)
    browser.get(url)
    html = browser.page_source
    time.sleep(0.5)

    ### get number of image for a page

    soup_temp = BeautifulSoup(html,'html.parser')
    img4page = len(soup_temp.findAll("img"))
    print("img per page : "+str(img4page))

    ### page down

    elem = browser.find_element_by_tag_name("body")
    tflag = 0
    while(1):
        elem.send_keys(Keys.END)
        time.sleep(1)
        try:
            more = browser.find_element_by_css_selector("#islmp > div > div > div > div > div.YstHxe > input")
            more.click()
        except:
            if tflag > 10:
                break
            tflag += 1
            continue
        try:
            end = browser.find_elements_by_css_selector("#islmp > div > div > div > div > div.DwpMZe > div.K25wae > div.OuJzKb.Yu2Dnd > div")
            for i in range(3):
                time.sleep(1)
                elem.send_keys(Keys.END)
            break
        except:
            continue


    html = browser.page_source
    soup = BeautifulSoup(html,'html.parser')
    img = soup.findAll("img")
    browser.find_elements_by_tag_name('img')

    fileNum = 0
    srcURL = []

    for line in img:
        if str(line).find('data-src') != -1 and str(line).find('http')<100:
            print(fileNum, " : ", line['data-src'])
            srcURL.append(line['data-src'])
            fileNum += 1
        elif str(line).find('src') != -1 and str(line).find('http')<100:
            print(fileNum, " : ", line['src'])
            srcURL.append(line['src'])
            fileNum += 1
        if fileNum==300:
            break

    ### make folder and save picture in that directory

    saveDir = folder+name

    try:
        if not(os.path.isdir(saveDir)):
            os.makedirs(os.path.join(saveDir))
    except OSError as e:
        if e.errno != e.errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    for i,src in zip(range(fileNum),srcURL):
        try:
            urllib.request.urlretrieve(src, saveDir+"/"+str(i))
            mime_type = magic.from_file(saveDir+"/"+str(i), mime=True)
            if mime_type == "image/jpeg":
                os.rename(saveDir+"/"+str(i), saveDir+"/"+str(i)+".jpg")
            elif mime_type == "image/png":
                os.rename(saveDir+"/"+str(i), saveDir+"/"+str(i)+".png")
            print(i,"saved")
        except Exception as e:
            print(e)
    browser.close()
