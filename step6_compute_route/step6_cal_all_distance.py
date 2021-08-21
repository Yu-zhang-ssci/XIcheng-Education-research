import json 
import pandas as pd 
import requests,csv

villages=pd.read_json('./village_2021_with_roomnum_school_gcj02ll_wgs84.json')
schools=pd.read_json('./District_2021_55_with_score_gcj02ll_wgs84.json')
#print (schools)

villageposlist=[]
for id,name in enumerate(villages.name):
    villagepos=(name,villages.gcj02lat[id],villages.gcj02lng[id])
    villageposlist.append(villagepos)
#print (poslist)

schoolposlist=[]
for id,name in enumerate(schools.school):
    schoolpos=(name,schools.gcj02lat[id],schools.gcj02lng[id])
    schoolposlist.append(schoolpos)

def get_route_v2s(vpos,spos,type='gcj02',mode='common'):
    Ak='ctxg7K1UqUfGfu5QbsVSgpYMGtnyQ32v'
    if mode=='common':
        url="http://api.map.baidu.com/directionlite/v1/transit?origin=%f,%f&destination=%f,%f&ak=%s&coord_type=%s&ret_coordtype=%s"%(vpos[1],vpos[2],spos[1],spos[2],Ak,type,type)
    else:
        url="http://api.map.baidu.com/directionlite/v1/walking?origin=%f,%f&destination=%f,%f&ak=%s&coord_type=%s&ret_coordtype=%s"%(vpos[1],vpos[2],spos[1],spos[2],Ak,type,type)
    headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Referer": "https://m.douban.com/tv/american"
    }
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    tmp=json.loads(req.text)     
    return tmp 

import pprint    
num=0
dirnum=0
infolist=[]
import pickle 
import os

for vpos in villageposlist:
    for spos in schoolposlist:
        
        try:
            if not os.path.exists('./route/%s-%s.route.json'%(vpos[0],spos[0]) ):
                route=get_route_v2s(vpos,spos,mode='common')
                if route["status"]!=0:
                    route=get_route_v2s(vpos,spos,mode='walk')
    
                with open('./route/%s-%s.route.json'%(vpos[0],spos[0]),'w',encoding='utf-8') as jsonfile:
                    jsonfile.write(json.dumps(route,ensure_ascii=False,indent=4))
                print (vpos,spos, ' not exist!, saved')
            else:
                route=json.load(open ('./route/%s-%s.route.json'%(vpos[0],spos[0]),'r'))
                if route["status"]!=0:
                    route=get_route_v2s(vpos,spos,mode='walk')
                    
                    with open('./route/%s-%s.route.json'%(vpos[0],spos[0]),'w',encoding='utf-8') as jsonfile:
                        jsonfile.write(json.dumps(route,ensure_ascii=False,indent=4))
            
            info={}
            info["village"]=vpos[0]
            info["school"]=spos[0]
            if route["status"]==0:
                if "taxi" in route["result"].keys():
                    taxidetail=route["result"]["taxi"]
                    info["taxi"]=[taxidetail["distance"],taxidetail["duration"]/60]
                if "routes" in route["result"].keys():
                    info["common_transport"]=[]
                    for rline in route["result"]["routes"]:
                        if 'price' in rline.keys():
                            info["common_transport"].append([rline["distance"],rline["duration"],rline["price"]])
                        else:
                            info["common_transport"].append([rline["distance"],rline["duration"],0])
            infolist.append(info)            
        except Exception as e:
            print (vpos,spos, ' error! ',e)
with open('./village_school_distance.pickle','wb')  as f:
    pickle.dump(infolist,f)
for info in infolist:
    if info['village']=='力学胡同小区':
        print (info)