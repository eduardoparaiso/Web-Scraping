
#CASO DE TESTE: 42973126
#CASO DE TESTE: 2181333 -  SEM VIDEOS
#CASO DE TESTE: 45287916 - SEM VIDEOS
#CASO DE TESTE: 1041801 - ACENTUAÇÃO
import time, datetime
import json
from selenium import webdriver
import re
import csv

#Converte tempo em milissegundos para data, retorna (d/m/s) ou (h:m:s)
def convert_date(ms, type):
    switcher = {
        'hour': datetime.datetime.fromtimestamp(ms/1000.0).strftime('%H:%M:%S'),
        'date': datetime.datetime.fromtimestamp(ms/1000.0).strftime('%d/%m/%Y')
    }
    return str(switcher.get(type, 'Invalid parameter'))
    
#Converte segundo para o padrão(h:m:s)
def convert_time(s):  
    return  str(datetime.timedelta(seconds=s))

#Remove tags html
def HTML_cleaner(html):
  regex = re.compile('<.*?>')
  text = re.sub(regex, '', html)
  return text

def get_json(user_id, view_max):
    api_path = 'https://booyah.live/api/v3/playbacks?channel_id=' + str(user_id) + '&cursor=0&count=' + str(view_max) + '&type=17&sort_method=1' 
   
    options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    # options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(options = options)
    # driver = selenium.webdriver.Chrome()
    driver.get('https://booyah.live/studio/' + str(user_id))
    time.sleep(1)
    driver.get(api_path)
    html = driver.page_source

    return json.loads(HTML_cleaner(html))

def get_origins():
    with open('Origens.txt') as file:
        origin = file.readlines()
        
    return origin

def execute_booyah(begin, end):
    return
#----------------------------------------------------------------------------------------------------------

origins = get_origins()
with open('booyah_info.csv', 'w', newline='') as file:
    w = csv.writer(file)
    w.writerow(['User_ID','Nickname', 'Data', 'Inicio', 'Duracao', 'Views', 'Likes', 'URL'])
    for origin in origins:
        data = get_json(origin, 50)

        user_id   = str(data['playback_list'][0]['user']['uid'])
        nickname  = data['playback_list'][0]['user']['nickname']
        followers = str(data['playback_list'][0]['user']['follower_count'])

        for i in data['playback_list']: 
            creation_date = convert_date(i['playback']['create_time_ms'], 'date')
            creation_time = convert_date(i['playback']['create_time_ms'], 'hour')
            duration      = convert_time(i['playback']['duration'])
            views         = str(i['playback']['views'])
            likes         = str(i['playback']['likes'])
            url           = i['playback']['share_url']

            w.writerow([user_id, nickname, creation_date, creation_time, duration, views, likes, url])