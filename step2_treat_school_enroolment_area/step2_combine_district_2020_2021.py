import json

with open("District_2021_55_chinese.json","r") as jsonfile:
    Districtlist_2021=json.load(jsonfile)
with open("District_2020_chinese.json","r") as jsonfile:
    Districtlist_2020=json.load(jsonfile)
print (len(Districtlist_2021),len(Districtlist_2020))

schoollist_2021=[district['school'] for district in Districtlist_2021]
schoollist_2020=[district['school'] for district in Districtlist_2020]
print (set(schoollist_2021))
print (set(schoollist_2020),len(set(schoollist_2020)))
for school in schoollist_2021:
    if school not in schoollist_2020:
        print (school)
print ('==========================')
for District in Districtlist_2020:
    if District['school'] not in schoollist_2021:
        Districtlist_2021.append(District)
#with open("District_2021_55_chinese.json","w",encoding='utf-8') as jsonfile:
#    jsonfile.write(json.dumps(Districtlist_2021,ensure_ascii=False,indent=1))



