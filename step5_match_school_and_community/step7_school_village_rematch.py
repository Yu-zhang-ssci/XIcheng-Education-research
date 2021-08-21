import json 
import re
import math
import numpy as np
from fuzzywuzzy import fuzz,process
with open('District_2021_55_with_score_gcj02ll_wgs84.json','r') as f:
    districts=json.load(f)
for district in districts:
    addresslist=[]
    for address in district['area']:
        addresslist+=re.split(r'[；：]',address)
    district['area']=addresslist

with open('village_xicheng_with_roomnum_gcj02ll_wgs84.json','r') as f:
    villages=json.load(f)
print (villages[0],districts[0])
address_schooldict={}
address_districtdict={}
for district in districts:
    for address in district['area']:
        if "居委会" not in address:
            address_schooldict[address]=district["school"]
            address_districtdict[address]=district["district"]
addresslist=address_schooldict.keys()
newvillages=[]
num0=0;num1=0
for village in villages:
    distancelist=[]
    for district in districts:
        dis=math.sqrt((float(village['gcj02lng'])-district['gcj02lng'])**2+(float(village['gcj02lat'])-district['gcj02lat'])**2)
        distancelist.append(dis)
    order=np.argsort(distancelist)[:4]

    candidatelist=[districts[i]['school'] for i in order]
    candidate_addresslist=[address for address in addresslist if address_schooldict[address] in candidatelist]

    villageaddress=re.split(r'］',village["address"])[-1]
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
            village['school']=[address_schooldict[closestaddresses[0][0]]]
            village['district']=[address_districtdict[closestaddresses[0][0]]]
        else:
            village['school']=list(set([address_schooldict[name[0]] for name in closestaddresses]))
            village['district']=list(set([address_districtdict[name[0]] for name in closestaddresses]))
        print (villageaddress,closestaddresses,set([address_schooldict[name[0]] for name in closestaddresses]))
        if len(village['school'])>1:
            num1+=1
    else:
        village['school']=[]
        village['district']=[]
        num0+=1
    print (num1,num0)
    newvillages.append(village)
for village in newvillages:
    if len(village['school'])>1 or len(village['school'])==0:
        dismin=100;schoolname='';districtname=''
        for district in districts:
            dis=math.sqrt((float(village['gcj02lng'])-district['gcj02lng'])**2+(float(village['gcj02lat'])-district['gcj02lat'])**2)
            if dis < dismin:
                dismin=dis
                schoolname=district['school']
                districtname=district['district']
        village['school']=[schoolname]
        village['district']=[districtname]

with open("villages_2021_allinfo_correct_schools.json","w",encoding='utf-8') as jsonfile:
    jsonfile.write(json.dumps(newvillages,ensure_ascii=False,indent=1))

