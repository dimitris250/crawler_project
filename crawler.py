import requests
import bs4 as bs
import urllib.parse
import json
from datetime import datetime, timedelta
import time
from selenium import webdriver





url='https://www.vrbo.com/el-gr/%CE%B5%CE%BD%CE%BF%CE%B9%CE%BA%CE%B9%CE%AC%CF%83%CE%B5%CE%B9%CF%82-%CE%B5%CE%BE%CE%BF%CF%87%CE%B9%CE%BA%CF%8E%CE%BD-%CE%BA%CE%B1%CF%84%CE%BF%CE%B9%CE%BA%CE%B9%CF%8E%CE%BD/p436144?adultsCount=2&arrival=2021-05-08&departure=2021-05-16'
headers={}
headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
req= urllib.request.Request(url, headers=headers)
source = urllib.request.urlopen(req).read()
soup = bs.BeautifulSoup(source,'html.parser')

data =[]

def get_basic_info():
    items={}
    lists=[]
    for name in soup.find('div', class_="property-headline u-freetext-fix"):
        items['name']= name.text

    for desc in soup.find('div', class_="collapsible-content"):
        items['description'] =desc.text

    for anemities in soup.find_all('div', class_="amenity-single__content")[0:9]:
        lists.append(anemities.text)
    
    items['anemities']= lists
    
    data.append(items)

    parsed=json.dumps(items, ensure_ascii=False).encode('utf-8')

    print(parsed.decode())

    

get_basic_info()