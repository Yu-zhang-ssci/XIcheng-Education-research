import json 
with open('teachers.json','r') as f:
    teachers=json.load(f)
with open('leaders.json','r') as f:
    leaders=json.load(f)
with open('environmentrank.json','r') as f:
    envir=json.load(f)
with open('school_xicheng_chinese_lnglat.json','r') as f:
    schools=json.load(f)
with open('District_2021_55_chinese.json','r') as f:
    districts=json.load(f)
school_teacher=teachers.keys()
school_leaders=leaders.keys()
school_envir=envir.keys()
schoollist=[school['name'] for school in schools]
districtlist=[district['school'] for district in districts]
print (schoollist,districtlist)
for newschool in districts:
    for oldschool in schools:
        if newschool['school']==oldschool['name'] or '北京市西城区'+newschool['school']==oldschool['name'] or '北京市'+newschool['school']==oldschool['name']:
            newschool['level']=oldschool['level']
            newschool['addressnum']=oldschool['address']
            newschool['score']=oldschool['score']
            newschool['lng']=oldschool['lng']
            newschool['lat']=oldschool['lat']
    if newschool['school'] in teachers.keys():
        newschool['city_teachernum']=teachers[newschool['school']]
    elif '北京市西城区'+newschool['school'] in teachers.keys():
        newschool['city_teachernum']=teachers['北京市西城区'+newschool['school']]
    elif '北京市'+newschool['school'] in teachers.keys():
        newschool['city_teachernum']=teachers['北京市'+newschool['school']]
    else:
        print ('teachers:',newschool['school'])
        newschool['city_teachernum']=0
    if newschool['school'] in leaders.keys():
        newschool['city_leadernum']=leaders[newschool['school']]
    elif '北京市西城区'+newschool['school'] in leaders.keys():
        newschool['city_leadernum']=leaders['北京市西城区'+newschool['school']]
    elif '北京市'+newschool['school'] in leaders.keys():
        newschool['city_leadernum']=leaders['北京市'+newschool['school']]
    else:
        print ('leaders:',newschool['school'])
        newschool['city_leadernum']=0
    if newschool['school'] in envir.keys():
        newschool['envir_score']=envir[newschool['school']]
    elif '北京市西城区'+newschool['school'] in envir.keys():
        newschool['envir_score']=envir['北京市西城区'+newschool['school']]
    elif '北京市'+newschool['school'] in envir.keys():
        newschool['envir_score']=envir['北京市'+newschool['school']]
    else:
        print ('envir:',newschool['school'])
        newschool['envir_score']=0

for newschool in districts:
    if 'score' not in newschool.keys():
        print (newschool['school'])
with open('District_2021_55_with_score.json','w',encoding='utf-8') as f:
    f.write(json.dumps(districts,ensure_ascii=False,indent=1))

