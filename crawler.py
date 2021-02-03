import requests
import bs4 as bs
import urllib.parse
import json
from datetime import datetime, timedelta
import time
import re





url='https://www.vrbo.com/el-gr/%CE%B5%CE%BD%CE%BF%CE%B9%CE%BA%CE%B9%CE%AC%CF%83%CE%B5%CE%B9%CF%82-%CE%B5%CE%BE%CE%BF%CF%87%CE%B9%CE%BA%CF%8E%CE%BD-%CE%BA%CE%B1%CF%84%CE%BF%CE%B9%CE%BA%CE%B9%CF%8E%CE%BD/p436317?adultsCount=2&arrival=2022-04-21&departure=2022-04-28&uni_id=1061960'
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

    req2 = requests.get(url).text

    search = re.search(r'window\.__INITIAL_STATE__ = ({.*});', req2).group(1)

    data = json.loads(search)

    items['latitude']= data['listingReducer']['geoCode']['latitude']
    items['longtitude']=data['listingReducer']['geoCode']['longitude']

    availability = (data['listingReducer']['availabilityCalendar']['availability']['unitAvailabilityConfiguration']['availability'])

    date_regex = r"(\d{4}-\d{2}-\d{2})"
    arrival_date = re.search(r"arrival=" + date_regex, url).group(1) #extracts arrival date from link
    departure_date = re.search(r"departure=" + date_regex, url).group(1) #extracts departure date from link

    items['arrival-date']=arrival_date
    items['departure-date']=departure_date

    arrival_day_of_year = datetime.strptime(arrival_date, '%Y-%m-%d')
    departure_day_of_year =datetime.strptime(departure_date, '%Y-%m-%d')

    arrival_day_of_year = arrival_day_of_year.timetuple().tm_yday #converts dates to the number of the day in the year
    departure_day_of_year= departure_day_of_year.timetuple().tm_yday #converts dates to the number of the day in the year

    if 'N' in (availability[arrival_day_of_year:departure_day_of_year]):
        items['availability']='Not Available'
    else:
        items['availability']='Available'
    
    parsed=json.dumps(items, ensure_ascii=False).encode('utf-8')

    print(parsed.decode())


get_basic_info()


