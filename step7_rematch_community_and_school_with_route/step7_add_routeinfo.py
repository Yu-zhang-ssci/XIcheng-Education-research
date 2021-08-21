import pickle 
import json 
with open('village_school_distance.pickle','rb')  as f:
    routes=pickle.load(f)
    for info in routes:
        if info['village']=='力学胡同小区':
            print (info)
#print (routes[0])
with open('villages_2021_allinfo_manu_correct.json','r') as f:
    villages=json.load(f)
with open('District_2021_55_with_score_gcj02ll_wgs84.json','r') as f:
    schools=json.load(f)
districtdict={}
for school in schools:
    if school['district'] not in districtdict.keys():
        districtdict[school['district']]=[]
    districtdict[school['district']].append(school['school'])
district_neighbor={}
district_neighbor['德胜学区']=['什刹海学区','新街口学区']
district_neighbor['什刹海学区']=['德胜学区','新街口学区','金融街学区','长安街学区']
district_neighbor['新街口学区']=['展览路学区','月坛学区','金融街学区','长安街学区','什刹海学区','德胜学区']
district_neighbor['展览路学区']=['新街口学区','月坛学区','金融街学区']
district_neighbor['月坛学区']=['展览路学区','金融街学区','新街口学区','广安门外','广安门内-牛街学区']
district_neighbor['金融街学区']=['展览路学区','新街口学区','什刹海学区','月坛学区','长安街学区','广安门外学区','广安门内-牛街学区','大栅栏-椿树-天桥学区']
district_neighbor['长安街学区']=['新街口学区','什刹海学区','金融街学区','广安门内-牛街学区','大栅栏-椿树-天桥学区']
district_neighbor['广安门外学区']=['月坛学区','广安门内-牛街学区','金融街学区','大栅栏-椿树-天桥学区','长安街学区','陶然亭-白纸坊学区']
district_neighbor['广安门内-牛街学区']=['月坛学区','金融街学区','长安街学区','大栅栏-椿树-天桥学区','陶然亭-白纸坊学区','广安门外学区']
district_neighbor['大栅栏-椿树-天桥学区']=['陶然亭-白纸坊学区','广安门内-牛街学区','金融街学区','长安街学区']
district_neighbor['陶然亭-白纸坊学区']=['广安门外学区','广安门内-牛街学区','大栅栏-椿树-天桥学区']
with open("district_neighborinfo.json","w",encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(district_neighbor,ensure_ascii=False,indent=1))

villagedict={}
schooldict={}
for village in villages:
    villagedict[village['name']]=village
    villagedict[village['name']]['now school taxi']=[]
    villagedict[village['name']]['now school common transportation']=[]
    villagedict[village['name']]['neighbor school taxi']={}
    villagedict[village['name']]['neighbor school common transportation']={}

for school in schools:
    schooldict[school['school']]=school
    schooldict[school['school']]['now village taxi']=[]
    schooldict[school['school']]['now village common transportation']=[]
    schooldict[school['school']]['neighbor village taxi']={}
    schooldict[school['school']]['neighbor village common transportation']={}

import numpy as np
for route in routes:
    if 'common_transport' in route.keys():
        try:
            if 'common transportation' not in villagedict[route['village']].keys():
                villagedict[route['village']]['common transportation']={}
            if 'common transportation' not in schooldict[route['school']].keys():
                schooldict[route['school']]['common transportation']={}
            timecost=[r[1] for r in route['common_transport']]
            distancecost=[r[0] for r in route['common_transport']]
            moneycost=[r[2] for r in route['common_transport']]
            timeindex=np.argmin(timecost)
            distanceindex=np.argmin(distancecost)
            moneyindex=np.argmin(moneycost)
            if route['school']==villagedict[route['village']]['school'][0]:
                villagedict[route['village']]['now school common transportation']=(route['common_transport'][timeindex],route['common_transport'][distanceindex],route['common_transport'][moneyindex])
                schooldict[route['school']]['now village common transportation'].append({route['village']:(route['common_transport'][timeindex],route['common_transport'][distanceindex],route['common_transport'][moneyindex])})
    
            if (schooldict[route['school']]['district'] in district_neighbor[villagedict[route['village']]['district'][0]])\
               or (schooldict[route['school']]['district']==villagedict[route['village']]['district']):
                villagedict[route['village']]['neighbor school common transportation'][route['school']]=(route['common_transport'][timeindex],route['common_transport'][distanceindex],route['common_transport'][moneyindex])
                schooldict[route['school']]['neighbor village common transportation'][route['village']]=(route['common_transport'][timeindex],route['common_transport'][distanceindex],route['common_transport'][moneyindex])
            villagedict[route['village']]['common transportation'][route['school']]=(route['common_transport'][timeindex],route['common_transport'][distanceindex],route['common_transport'][moneyindex])
            schooldict[route['school']]['common transportation'][route['village']]=(route['common_transport'][timeindex],route['common_transport'][distanceindex],route['common_transport'][moneyindex])
        except Exception as e:
            pass  
newschools=[]
newvillages=[]
for key in schooldict.keys():
    newschools.append(schooldict[key])
for key in villagedict.keys():
    newvillages.append(villagedict[key])
with open("schools_allinfo.json","w",encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(newschools,ensure_ascii=False,indent=1))
with open("villages_allinfo.json","w",encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(newvillages,ensure_ascii=False,indent=1))
        for village in newvillages:
            if village['school'][0]=='力学小学':
                print (village['name'],village['now school common transportation'])



print(routes[0])

