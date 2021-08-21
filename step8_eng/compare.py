import pickle 
import json 
import numpy as np
import pandas as pd 
from details import * 
from copy import deepcopy 
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import random
from dash.dependencies import Input,Output
import plotly.io as pio
def Gini_coeffient(data,possibility=None):
    #https://www.jianshu.com/p/7d503cceae3e
    data = np.asarray(data)
    nanlist = np.where(np.isnan(data))
    data=[data[i] for i in range(len(data)) if i not in nanlist[0]]
    if possibility is not None:
        possibility=[possibility[i] for i in range(len(possibility)) if i not in nanlist[0]] 
    data= data-np.min(data)
    for i in range(len(data)):
        if data[i]<0.001:
            data[i]=0
    if np.sum(np.sqrt(data**2))>0.01:
        if possibility is not None:
            possibility = np.asarray(possibility)
            sorted_indices = np.argsort(data)
            sorted_data = data[sorted_indices]
            sorted_possibility = possibility[sorted_indices]
            # Force float dtype to avoid overflows
            cumpossibility = np.cumsum(sorted_possibility, dtype=float)
            cumdata_possibility = np.cumsum(sorted_data * sorted_possibility, dtype=float)
            return (np.sum(cumdata_possibility[1:] * cumpossibility[:-1] - cumdata_possibility[:-1] * cumpossibility[1:]) / 
                    (cumdata_possibility[-1] * cumpossibility[-1]))
        else:
            sorted_data = np.sort(data)
            n = len(data)
            cumdata = np.cumsum(sorted_data, dtype=float)
            # The above formula, with all weights equal to 1 simplifies to:
            return (n + 1 - 2 * np.sum(cumdata) / cumdata[-1]) / n
    else:
        return 0

def fair_analysis(villages,schools,policy,cutoff=10000,year=0):
    Gdictlist=[]
    Vdictlist=[]
    average_livearea_per_person=21.9 # 2019 北京西城统计年鉴
    average_peoplenum_per_home=3.67 # 2020 中国统计年鉴（每户大于三人）
    average_income_per_person=81678 #2019 北京西城统计年鉴
    average_interest_rate=0.049 # 2020 北京贷款基准利率 （商业）
    average_month_payment_per_person=8136
    average_rate=0.05 
    
    for village in villages:
        village['tmp_price']=float(village['price'])*1.05**year
    Premium={}
    tscorelist=[]
    lscorelist=[]
    escorelist=[]
    pscorelist=[]
    rscorelist=[]
    
    for school in schools:
        tscorelist.append(school['city_teachernum'])
        lscorelist.append(school['city_leadernum'])
        escorelist.append(school['envir_score'])
        pscorelist.append(school['score'])
        rscorelist.append(school_leveldict[school['level']])
    
    tmin,tmax=np.min(tscorelist),np.max(tscorelist)
    lmin,lmax=np.min(lscorelist),np.max(lscorelist)
    emin,emax=np.min(escorelist),np.max(escorelist)
    pmin,pmax=np.min(pscorelist),np.max(pscorelist)
    rmin,rmax=np.min(rscorelist),np.max(rscorelist)
    
    schooldict={}
    for school in schools:
        school['average_score']=((school_leveldict[school['level']]-rmin)/(rmax-rmin)+\
            (school['city_teachernum']-tmin)/(tmax-tmin)+\
            (school['city_leadernum']-lmin)/(lmax-lmin)+\
            (school['envir_score']-emin)/(emax-emin)+\
            (school['score']-pmin)/(pmax-pmin))/5*100
        schooldict[school['school']]=school
    
    with open('./data/district_neighborinfo.json','r') as f:
        district_neighborinfos=json.load(f)
    for village in villages:
        village['neighbor schools']=[school['school'] for school in schools if school['district'] in district_neighborinfos[village['district'][0]]+ [village['district'][0]]]
    district_info={}
    
    for district in list(district_neighborinfos.keys()):
        district_info[district]={}
        """
        normal_sh_price  = np.array([village['tmp_price'] for village in villages if schooldict[village['school'][0]]['level']=='普通' and village['district'][0]+'学区' in     district_neighborinfos[district]+[district]])
        normal_sh_num    = np.array([village['roomnum'] for village in villages if schooldict[village['school'][0]]['level']=='普通' and village['district'][0]+'学区' in       district_neighborinfos[district]+[district]])
        area_sh_price    = np.array([village['tmp_price'] for village in villages if schooldict[village['school'][0]]['level']=='区重点' and village['district'][0]+'学区' in   district_neighborinfos[district]+[district]])
        area_sh_num      = np.array([village['roomnum'] for village in villages if schooldict[village['school'][0]]['level']=='区重点' and village['district'][0]+'学区' in     district_neighborinfos[district]+[district]])
        city_sh_price    = np.array([village['tmp_price'] for village in villages if schooldict[village['school'][0]]['level']=='市重点' and village['district'][0]+'学区' in   district_neighborinfos[district]+[district]])
        city_sh_num      = np.array([village['roomnum'] for village in villages if schooldict[village['school'][0]]['level']=='市重点' and village['district'][0]+'学区' in     district_neighborinfos[district]+[district]])
        country_sh_price = np.array([village['tmp_price'] for village in villages if schooldict[village['school'][0]]['level']=='全国重点' and village['district'][0]+'学区' in district_neighborinfos[district]+[district]])
        country_sh_num   = np.array([village['roomnum'] for village in villages if schooldict[village['school'][0]]['level']=='全国重点' and village['district'][0]+'学区' in   district_neighborinfos[district]+[district]])
        """
        normal_sh_price  = np.array([village['tmp_price'] for village in villages if schooldict[village['school'][0]]['level']=='普通' ])
        normal_sh_num    = np.array([village['roomnum'] for village in villages if schooldict[village['school'][0]]['level']=='普通' ])
        area_sh_price    = np.array([village['tmp_price'] for village in villages if schooldict[village['school'][0]]['level']=='区重点' ])
        area_sh_num      = np.array([village['roomnum'] for village in villages if schooldict[village['school'][0]]['level']=='区重点' ])
        city_sh_price    = np.array([village['tmp_price'] for village in villages if schooldict[village['school'][0]]['level']=='市重点' ])
        city_sh_num      = np.array([village['roomnum'] for village in villages if schooldict[village['school'][0]]['level']=='市重点' ])
        country_sh_price = np.array([village['tmp_price'] for village in villages if schooldict[village['school'][0]]['level']=='全国重点' ])
        country_sh_num   = np.array([village['roomnum'] for village in villages if schooldict[village['school'][0]]['level']=='全国重点' ])
        district_info[district]['average_price_normal']=np.sum(normal_sh_price*normal_sh_num)/np.sum(normal_sh_num)
        district_info[district]['average_price_area']=np.sum(area_sh_price*area_sh_num)/np.sum(area_sh_num)
        district_info[district]['average_price_city']=np.sum(city_sh_price*city_sh_num)/np.sum(city_sh_num)
        district_info[district]['average_price_country']=np.sum(country_sh_price*country_sh_num)/np.sum(country_sh_num)
        district_info[district]['premium_area']=district_info[district]['average_price_area']-district_info[district]['average_price_normal']
        district_info[district]['premium_city']=district_info[district]['average_price_city']-district_info[district]['average_price_normal']
        district_info[district]['premium_country']=district_info[district]['average_price_country']-district_info[district]['average_price_normal']
    
    for key in schooldict.keys():
        schooldict[key]['average price']=np.mean([village['tmp_price'] for village in villages if village['school'][0]==key])
        schooldict[key]['premium']=np.mean([village['tmp_price'] for village in villages if village['school'][0]==key])-district_info[schooldict[key]['district']]['average_price_normal']
    
    def month_payment(price):
        payment=price/100000*8136
        return payment
    
    def select_school(village,policy='one',cutoff=10000,year=0):
        schoollist=[]
        if policy=='one':
            schoollist.append(village['school'][0])
        elif policy=='neighbor':
            schoollist=village['neighbor schools']#list(village['neighbor school common transportation'].keys())
        elif policy=='Time':
            schoollist=list([key for key in village['common transportation'].keys() if village['common transportation'][key][0][1]<cutoff])
        elif policy=='Distance':
            schoollist=list([key for key in village['common transportation'].keys() if village['common transportation'][key][1][0]<cutoff])
        elif policy=='Money':
            schoollist=list([key for key in village['common transportation'].keys() if village['common transportation'][key][2][2]<cutoff])
        return schoollist
    
    #def Price_for_school(village,policy='one',cutoff=10000,year=0,transmethod='Time cost'):
    for village in villages:
        tmpschoollist=select_school(village,policy,cutoff,year=6)
        areaschools=[schoolname for schoolname in tmpschoollist if schooldict[schoolname]['level']=='区重点']
        cityschools=[schoolname for schoolname in tmpschoollist if schooldict[schoolname]['level']=='市重点']
        countryschools=[schoolname for schoolname in tmpschoollist if schooldict[schoolname]['level']=='全国重点']
        tmpprice=village['tmp_price']-schooldict[village['school'][0]]['premium']
        for schoolname in tmpschoollist:
            tmpprice+=1/len(tmpschoollist)*schooldict[schoolname]['premium']
        village['current price']=tmpprice
    
    def Educational_cost(village,policy='one',cutoff=10000,year=0,transmethod='Time cost'):
        
        schoollist=select_school(village,policy,cutoff,year)
        schoolpayment=80*2
        ori_price=float(village['price'])
        ori_yearpayment=month_payment(ori_price)*12
        ori_transportation_cost=(village['now school common transportation'][0][-1]*2*365)
        ori_educost=(ori_yearpayment+ori_transportation_cost+schoolpayment)/1000
        
        if policy=='neighbor':
            cur_price=float(village['current price'])
            cur_yearpayment=month_payment(cur_price)*12
            cur_costs=[]
        
            for schoolname in schoollist:
                try:
                    if len(village['common transportation'][schoolname])>0:
                        cur_costs.append(village['common transportation'][schoolname][0][-1]*2*365)
                except:
                    pass
            cur_transportation_cost=np.sum(cur_costs)/len(cur_costs)
            cur_educost=(cur_yearpayment+cur_transportation_cost+schoolpayment)/1000
            return ori_educost*(6-year)/6+cur_educost*year/6
        if policy=='one':
            cur_price=float(village['tmp_price'])
            cur_yearpayment=month_payment(cur_price)*12
            cur_transportation_cost=(village['now school common transportation'][0][-1]*2*365)
            cur_educost=(cur_yearpayment+ori_transportation_cost+schoolpayment)/1000
            return ori_educost*(6-year)/6+cur_educost*year/6
    
    def Time_cost(village,policy='one',cutoff=10000,year=0):
        schoollist=select_school(village,policy,cutoff,year)
        ori_timecost=village['now school common transportation'][0][1]/60
        cur_cost=[]
        for schoolname in schoollist:
            try:
                cur_cost.append(village['common transportation'][schoolname][1])
            except:
                pass
        cur_timecost=np.average(cur_cost)/60 
        if policy=='one':
            return ori_timecost
        elif policy=='neighbor':
            return ori_timecost*(6-year)/6+cur_timecost*year/6 
        
    
    def Education_resource(village,policy='one',cutoff=10000,year=0):
        schoollist=select_school(village,policy,cutoff,year)
        ori_schoolscore=schooldict[village['school'][0]]['average_score']

        cur_rlist=[]
        for schoolname in schoollist:
            cur_rlist.append(schooldict[schoolname]['average_score'])
        cur_schoolscore=np.average(cur_rlist)
        if policy=='one':
            return ori_schoolscore 
        elif policy=='neighbor':
            return ori_schoolscore*(6-year)/6+cur_schoolscore*year/6
    
    for village in villages:
        village['fair index']={}
        village['educost']=Educational_cost(village,policy,cutoff,year)
        village['timecost']=Time_cost(village,policy,cutoff,year)
        village['eduresource']=Education_resource(village,policy,cutoff,year)
    total_mineducost=[1000000,1000000]
    total_mintimecost=[1000000,1000000]
    for district in district_neighborinfos.keys():
        #print (district)
        possibility=[village['roomnum'] for village in villages if village['district'][0]==district]
        district_info[district]['possibility']=possibility/np.sum(possibility)
        educost=[village['educost'] for village in villages if village['district'][0]==district]
        timecost=[village['timecost'] for village in villages if village['district'][0]==district]
        eduresource=[village['eduresource'] for village in villages if village['district'][0]==district]
        district_info[district]['min educost'] =(np.min(educost),eduresource[np.argmin(educost)])
        if np.min(educost)<total_mineducost[0]:
            total_mineducost=district_info[district]['min educost']
        district_info[district]['min timecost']=(np.min(timecost),eduresource[np.argmin(timecost)])
        if np.min(timecost)<total_mintimecost[0]:
            total_mintimecost=district_info[district]['min timecost']

    for village in villages:
        #village['educost_efficiency']=(village['eduresource']-district_info[village['district'][0]+'学区']['min educost'][1])/(village['educost']-district_info[village['district'][0]+'学区']['min educost'][0])
        #print (village['eduresource'],district_info[village['district'][0]+'学区']['min educost'][1],village['educost'],district_info[village['district'][0]+'学区']['min educost'][0],village['educost_efficiency'])
        #village['timecost_efficiency']=(village['eduresource']-district_info[village['district'][0]+'学区']['min timecost'][1])/(village['timecost']-district_info[village['district'][0]+'学区']['min timecost'][0])

        if (village['educost']-total_mineducost[0])<0.0001:
            village['educost_efficiency']=0
        else:
            village['educost_efficiency']=(village['eduresource']-total_mineducost[1])/(village['educost']-total_mineducost[0])

        if (village['timecost']-total_mintimecost[0])<0.0001:
            village['timecost_efficiency']=0
        else: 
            village['timecost_efficiency']=(village['eduresource']-total_mintimecost[1])/(village['timecost']-total_mintimecost[0])
        
    sum_eduresource={}
    total_eduresource=0
    total_housenum=0

    for district in district_neighborinfos.keys():
        eduresource=np.array([village['eduresource'] for village in villages if village['district'][0]==district])
        deducost=np.array([village['educost'] for village in villages if village['district'][0]==district])
        dtimecost=np.array([village['timecost'] for village in villages if village['district'][0]==district])
        dedueff=np.array([village['educost_efficiency'] for village in villages if village['district'][0]==district])
        dtimeeff=np.array([village['timecost_efficiency'] for village in villages if village['district'][0]==district])
        housenum=[village['roomnum'] for village in villages if village['district'][0]==district]
        
        sum_eduresource=np.sum(eduresource*housenum)
        sum_housenum=np.sum(housenum)
        district_info[district]['average eduresource']=sum_eduresource/sum_housenum 
        district_info[district]['average educost']=np.sum(deducost*housenum)/sum_housenum
        district_info[district]['average timecost']=np.sum(dtimecost*housenum)/sum_housenum
        district_info[district]['average edueff']=np.sum(dedueff*housenum)/sum_housenum
        district_info[district]['average_timeeff']=np.sum(dtimeeff*housenum)/sum_housenum

        total_eduresource+=sum_eduresource
        total_housenum+=sum_housenum
     
    total_average_eduresource=total_eduresource/total_housenum
    
    for village in villages:
        village['edu_resource difference district']=village['eduresource']-district_info[village['district'][0]]['average eduresource']
        village['edu_resource difference xicheng']=village['eduresource']-total_average_eduresource
        
    for district in district_neighborinfos.keys():
        housenum=[village['roomnum'] for village in villages if village['district'][0]==district]
        sum_housenum=np.sum(housenum)
        diffdistrict=np.array([village['edu_resource difference district'] for village in villages if village['district'][0]==district])
        diffxicheng =np.array([village['edu_resource difference xicheng'] for village in villages if village['district'][0]==district])
        
        district_info[district]['average diffdistrict']=np.sum(diffdistrict*housenum)/sum_housenum 
        district_info[district]['average diffxicheng']=np.sum(diffxicheng*housenum)/sum_housenum
        

    for key in schooldict.keys():
        schooldict[key]['neighbor average price']=np.mean([village['current price'] for village in villages if village['school'][0]==key])
        schooldict[key]['neighbor premium']=np.mean([village['current price'] for village in villages if village['school'][0]==key])-district_info[schooldict[key]['district']]['average_price_normal']
    chinesekeydict={}
    ekeys=['educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']
    ckeys=['教育花费(千元/年)','时间成本(分钟)','占有教育资源','教育花费效率','时间成本效率','学区内教育资源占有差别','西城区教育资源占有差别']
    for i in range(len(ekeys)):
        chinesekeydict[ekeys[i]]=ckeys[i]
    Ginidict={}
    for district in district_neighborinfos.keys():
        Ginidict[district]={}
        for key in ['educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
            fairindex=[village[key] for village in villages if village['district'][0]==district]
            possibility=district_info[district]['possibility']
            #print (key,district,np.array(fairindex),np.array(possibility))
            g=Gini_coeffient(fairindex,possibility)
            if key=='eduresource' and district=='长安街学区':
                print (set(fairindex),g)
            Ginidict[district][chinesekeydict[key]]=g
    
    Ginidict['西城']={}
    for key in ['educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
        fairindex=[village[key] for village in villages]
        housenum=[village['roomnum'] for village in villages]
        possibility=np.array(housenum)/np.sum(housenum)
        g=Gini_coeffient(fairindex,possibility)
        Ginidict['西城'][chinesekeydict[key]]=g
    ginidata=pd.DataFrame(Ginidict)
    #Gdictlist.append(Ginidict)
    vdict={}
    #for village in villages:
    if policy=='neighbor':
        vdict['当前学区房价格']=[village['current price'] for village in villages]
    elif policy=='one':
        vdict['当前学区房价格']=[village['tmp_price'] for village in villages]
    vdict['教育花费(千元/年)']=[village['educost'] for village in villages]
    vdict['时间成本(分钟)']=[village['timecost'] for village in villages]
    vdict['占有教育资源']=[village['eduresource'] for village in villages]
    vdict['学校']=[village['school'][0] for village in villages]
    vdict['学区']=[village['district'][0] for village in villages]
    vdict['教育花费效率']=[village['educost_efficiency'] for village in villages]
    vdict['时间成本效率']=[village['timecost_efficiency'] for village in villages]
    vdict['学区内教育资源占有差别']=[village['edu_resource difference district'] for village in villages]
    vdict['西城区教育资源占有差别']=[village['edu_resource difference xicheng'] for village in villages]
    vdict['小区']=[village['name'] for village in villages]
    vdict['户数']=[village['roomnum'] for village in villages]
    tmpschools=[schooldict[key] for key in schooldict.keys()]
    sdict={}
    sdict['综合打分']=[school['average_score'] for school in tmpschools]
    sdict['市学科带头人人数']=[school['city_leadernum'] for school in tmpschools]
    sdict['市级优秀教师人数']=[school['city_teachernum'] for school in tmpschools]
    sdict['环境管理评级通过批次']=[school['envir_score'] for school in tmpschools]
    sdict['家长评分']=[school['score']for school in tmpschools]
    sdict['学校等级']=[school['level'] for school in tmpschools]
    sdict['学区房平均价格']=[school['average price'] for school in tmpschools]
    sdict['学区房溢价']=[school['premium'] for school in tmpschools]
    sdict['所属学区']=[school['district'] for school in tmpschools]
    sdict['多校划片后原学区房的平均溢价']=[school['neighbor premium'] for school in tmpschools]
    sdict['多校划片后原学区房的平均价格']=[school['neighbor average price'] for school in tmpschools]
    sdict['学校']=[school['school'] for school in tmpschools]
    vdata=pd.DataFrame(vdict)
    #Vdictlist.append(vdict)
    #finalgdict=deepcopy(Gdictlist[0])
    #for key1 in finalgdict.keys():
    #    for key2 in finalgdict[key1].keys():
    #        finalgdict[key1][key2]=np.mean([tmpdict[key1][key2] for tmpdict in Gdictlist])
    
    finalginidata=ginidata 
    finalvdata=vdata 
    finalsdata=pd.DataFrame(sdict)
    finalddata=pd.DataFrame(district_info)
    #print (finalginidata)
    finalginidata.to_csv('Xicheng_Gini_%s_%d_%d.csv'%(policy,year,cutoff))
    finalvdata.to_csv('Xicheng_Data_%s_%d_%d.csv'%(policy,year,cutoff))
    finalsdata.to_csv('Xicheng_School_%s_%d_%d.csv'%(policy,year,cutoff))
    finalddata.to_csv('Xicheng_District_%s_%d_%d.csv'%(policy,year,cutoff))
    return vdict,finalsdata,finalginidata


with open('data/villages_allinfo.json','r') as f:
    tmpvillages=json.load(f)
#    print(tmpvillages[0].keys())
    dict_villages=[]
    for  village in tmpvillages:
        if 'roomnum' in village.keys() and len(village['now school common transportation'])>0:
            if village['roomnum']!='暂无数据':
                dict_villages.append(village)
for village in dict_villages:
    village['roomnum']=int(village['roomnum'][:-1])

with open('data/schools_allinfo.json','r') as f:
    dict_schools=json.load(f)
vlist=[]
slist=[]
ginilist=[]
year=6
for policy in ['one','neighbor']:
    v,s,gini=fair_analysis(dict_villages,dict_schools,policy=policy,year=year)
    vlist.append(v)
    slist.append(s)
    ginilist.append(gini)
village_object=[village['name'] for village in dict_villages]
school_object=[school['school'] for school in dict_schools]
lang='Eng'
fairindex_object=['当前学区房价格','教育花费(千元/年)','时间成本(分钟)','占有教育资源','教育花费效率','时间成本效率','学区内教育资源占有差别','西城区教育资源占有差别']
fairindex_engdict={
    '当前学区房价格':r'$\large{\large{\text{Current house price}\ P_{house}\ (\text{CNY}/m^2)}}$',
    "教育花费(千元/年)":r"$\large{\text{Educational expenses}\ C_{edu} (10^3 \text{CNY}/year)}$",
    "时间成本(分钟)":r"$\large{\text{Time expenses}\ C_{time}\ (min)}$",
    "占有教育资源":r"$\large{\text{Educational resource evaluation}\ R_{school}}$",
    "教育花费效率":r"$\large{\text{Efficiency of educational expenses}\ \lambda_{c}}$",
    "时间成本效率":r"$\large{\text{Efficiency of time expenses}\ \lambda_{t}}$",
    '学区内教育资源占有差别':r"$\large{\text{Difference of educational resources of community}\\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \text{in same schhol district}\ D_{district}}$",
    "西城区教育资源占有差别":r"$\large{\text{Difference of educational resources of community}\\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \text{in the whole Xicheng area}\ D_{Xicheng}}$"
    }
district_engdict={
                  "展览路学区":"Zhanlan Road",
                  "德胜学区":"Desheng",
                  "什刹海学区":"Shichahai",
                  "新街口学区":"Xinjiekou",
                  "月坛学区":"YueTan",
                  "金融街学区":"Jinrong Street",
                  "长安街学区":"Chang'an Avenue",
                  "广安门外学区":"Guang'anmen Outer Street",
                  "广安门内-牛街学区":"Gunag'anmen Inner Street-Niujie Street",
                  "大栅栏-椿树-天桥学区":"Dashilan-Chunshu-Tiaoqiao",
                  "陶然亭-白纸坊学区":"Taoranting-Baizhifang"
                  }

from details import * 
for kid,key in enumerate(fairindex_object):
    fig=go.Figure()
    if lang!='Eng':
        one_result=[vlist[0][key][i] for i in range(len(vlist[0][key])) if vlist[0]['学区'][i] in district_object]
        one_district=[vlist[0]['学区'][i] for i in range(len(vlist[0][key])) if vlist[0]['学区'][i] in district_object]
        neighbor_result=[vlist[1][key][i] for i in range(len(vlist[1][key])) if vlist[1]['学区'][i] in district_object]
        neighbor_district=[vlist[1]['学区'][i] for i in range(len(vlist[1][key])) if vlist[1]['学区'][i] in district_object]
    else:
        one_result=[vlist[0][key][i] for i in range(len(vlist[0][key])) if vlist[0]['学区'][i] in district_object]
        one_district=[district_engdict[vlist[0]['学区'][i]] for i in range(len(vlist[0][key])) if vlist[0]['学区'][i] in district_object]
        neighbor_result=[vlist[1][key][i] for i in range(len(vlist[1][key])) if vlist[1]['学区'][i] in district_object]
        neighbor_district=[district_engdict[vlist[1]['学区'][i]] for i in range(len(vlist[1][key])) if vlist[1]['学区'][i] in district_object]
        
     
    fig.add_trace(go.Box(y=one_result,x=one_district,name='NEP'))
    fig.add_trace(go.Box(y=neighbor_result,x=neighbor_district,name='MSDP'))
    if lang!='Eng':
        fig.update_layout(
        yaxis_title=key,
        boxmode='group',
        margin={"r":60,"l":60,'t':40,'b':40},
        height=900,width=1200,
        font={'size':32})
    else:
        fig.update_layout(
        yaxis_title=fairindex_engdict[key],
        boxmode='group',
        margin={"r":60,"l":60,'t':40,'b':40},
        height=900,width=1200,
        font={'size':28,},
        font_family='Open Sans')
        
#    pio.write_image(fig,f'{kid}.png')
    fig.show()
    
"""
plotlist=plot_fair_index_district([1,5],['金融街','新街口'])
for plot in plotlist:
    plot.show()
plotlist=plot_gini_district([1,5],['金融街','新街口'])
for plot in plotlist:
    plot.show()
plotlist=plot_fair_index_school([1,5],['北京第二实验小学'])
for plot in plotlist:
    plot.show()
plot=plot_school([1,5],'北京第二实验小学')
plot.show()
plot=plot_village([1,5],'朱雀门小区')
plot.show()
"""
