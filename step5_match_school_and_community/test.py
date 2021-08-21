import json 
from map import * 
import pickle 

with open('village_xicheng_with_roomnum_gcj02ll_wgs84.json','r') as f:
    villages=json.load(f)

with open('District_2021_55_with_score_gcj02ll_wgs84.json','r') as f:
    schools=json.load(f)

with open('village_school_distance.pickle','rb') as f:
    vsd=pickle.load(f)

with open('maps.json','r') as f:
    maps=json.load(f)

mapdict={}
for area in maps["features"]:
    mapdict[area['properties']['name']]=area["geometry"]["coordinates"]

disdict={}
for dis in vsd:
    print (dis)
    if dis['village'] not in disdict.keys():
        disdict[dis['village']]={}
    if 'taxi' in dis.keys():
        disdict[dis['village']][dis['school']]=dis['taxi'][0]
    else:
        disdict[dis['village']][dis['school']]=100000000000000

import math 
import numpy as np
import re
from fuzzywuzzy import fuzz,process 
newvillages=[]
for village in villages:
    posi=[village['wgs84lng'],village['wgs84lat']]
    for key in mapdict:
        flag=isPoiWithinPoly(posi, mapdict[key], tolerance=0.0001)
        if flag:
            village['district']=[key]
    schoollist=[]
    dislist=[]
    maxdis=100000000000
    if 'district' not in village.keys():
        print (village)
    else:
        for school in schools:
            if school['district']==village['district'][0]:
                dis=math.sqrt((float(village['gcj02lng'])-school['gcj02lng'])**2+(float(village['gcj02lat'])-school['gcj02lat'])**2)
                dislist.append(dis)
                schoollist.append(school)
        order=np.argsort(dislist)[:4]
        candi_schools=[schoollist[i] for i in order]
        addresslist=[]
        addressdict={}
        for school in candi_schools:
            for address in school['area']:
                addresslist.append(address)
                addressdict[address]=school['school']
        villageaddress=village["address"].split(' ')[-1]
        if '大街' in villageaddress:
            streetname=re.match(r'(.+)(大街|胡同|巷|里|路)(.)',villageaddress)
        elif '胡同' in villageaddress:
            streetname=re.match(r'(.+)(胡同)',villageaddress)
        else:
            streetname=re.match(r'(.+)(街|胡同|巷|里|路)(.)',villageaddress)
        if streetname:
            if '胡同' in villageaddress:
                streetname=streetname.group(1)
                print ('=========',streetname)
            else:
                streetname=streetname.group(1)
            screenlist=[m for m in addresslist if streetname in m]
            closestaddresses=process.extract(villageaddress,screenlist,limit=3,scorer=fuzz.partial_ratio)
        else:
            closestaddresses=process.extract(villageaddress,addresslist,limit=3,scorer=fuzz.partial_ratio)
        if len(closestaddresses)>0:
            if closestaddresses[0][1]>90:
                village['school']=[addressdict[closestaddresses[0][0]]]
                village['cscore']=[closestaddresses[0][1]]
            else:
                village['school']=list(set([addressdict[name[0]] for name in closestaddresses]))
                village['cscore']=list(set([name[1] for name in closestaddresses]))
                
            #print (villageaddress,closestaddresses,set([addressdict[name[0]] for name in closestaddresses]))
            if village['roomnum']!='暂无数据':
                newvillages.append(village)
        else:
            village['school']=[]
            village['csore']=[0]
 
        
unsure_num=0
for village in newvillages:
    if len(village['school'])>1 or len(village['school'])==0:
        dismin=100;schoolname=''
        for school in schools:
            if school['district']==village['district'][0]:
                dis=math.sqrt((float(village['gcj02lng'])-school['gcj02lng'])**2+(float(village['gcj02lat'])-school['gcj02lat'])**2)
                if dis < dismin:
                    dismin=dis
                    schoolname=school['school']
                
        village['school']=[schoolname]
        unsure_num+=1
print (unsure_num)
print (len(newvillages))
with open("villages_2021_allinfo_manu_correct.json","w",encoding='utf-8') as jsonfile:
    jsonfile.write(json.dumps(newvillages,ensure_ascii=False,indent=1)  )      
