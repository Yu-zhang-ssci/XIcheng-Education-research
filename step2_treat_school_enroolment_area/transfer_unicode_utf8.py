import json 
with open('District_2021.json','r') as f:
    Districtlist=json.load(f)
with open("District_2021_chinese.json","w",encoding='utf-8') as jsonfile:
    jsonfile.write(json.dumps(Districtlist,ensure_ascii=False,indent=1))
