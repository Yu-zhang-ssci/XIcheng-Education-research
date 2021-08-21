
import json
import requests,csv
import pandas as pd 
from address_transform import *
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = '5UODhzjt5tyyYPXjIlS5rbuxrA1BdT5S'
    add=address
    uri = url + '?' + 'address=' + add  + '&output=json' + '&ak=' + ak+'&ret_coordtype=gcj02ll'
    print (uri)
    headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Referer": "https://m.douban.com/tv/american"
}

    req = requests.get(uri,headers=headers)
    req.encoding='utf-8'
    tmp=json.loads(req.text)
    try:
        lng=tmp['result']['location']['lng']
        lat=tmp['result']['location']['lat']
        confidence=tmp['result']['confidence']
    except:
        print(address,tmp)
    return (lng,lat,confidence)
#print (getlnglat('北京第二实验小学'))
with open('village_xicheng_with_roomnum.json',"r") as f:
    villages=json.load(f)
newlist=[]
for village in villages:
    village['gcj02lng']=float(village['y'])
    village['gcj02lat']=float(village['x'])
    [village['wgs84lng'],village['wgs84lat']]=gcj02towgs84(float(village['y']),float(village['x']))
#    print (school)
    newlist.append(village)
with open('village_xicheng_with_roomnum_gcj02ll_wgs84.json','w',encoding='utf-8') as jsonfile:
    jsonfile.write(json.dumps(newlist,ensure_ascii=False,indent=1))
#
