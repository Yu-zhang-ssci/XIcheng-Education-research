
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
with open('District_2021_55_with_score.json',"r") as f:
    schools=json.load(f)
newlist=[]
for school in schools:
    g3,g4,c2=getlnglat('北京市西城区'+school['school'])
    g1,g2,c1=getlnglat('北京市西城区'+school['addressnum'])
    if c1>c2:
        school['gcj02lng'],school['gcj02lat']=g1,g2
    else:
        school['gcj02lng'],school['gcj02lat']=g3,g4
    #school['gcj02lng'],school['gcj02lat'],confidence=getlnglat('北京市西城区'+school['addressnum'])
    #print (school['gcj02lng'],school['gcj02lat'],confidence)
    #school['gcj02lng'],school['gcj02lat'],confidence=getlnglat('北京市西城区'+school['school'])
    #print (school['gcj02lng'],school['gcj02lat'],confidence)
    [school['wgs84lng'],school['wgs84lat']]=gcj02towgs84(school['gcj02lng'],school['gcj02lat'])
#    print (school)
    newlist.append(school)
with open('District_2021_55_with_score_gcj02ll_wgs84.json','w',encoding='utf-8') as jsonfile:
    jsonfile.write(json.dumps(newlist,ensure_ascii=False,indent=1))

