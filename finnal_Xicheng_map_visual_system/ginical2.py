import pickle 
import json 
import numpy as np
import pandas as pd 
from details import * 
from copy import deepcopy 
import plotly.express as px
import plotly.graph_objects as go
import random
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
    for time in range(10):
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
                choicelist=[0]*(6-year)+[1]*year
                choice=random.choice(choicelist)
                if choice!=0:
                    schoollist=village['neighbor schools']#list(village['neighbor school common transportation'].keys())
                else:
                    schoollist=[village['school'][0]]
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
            if len(schoollist)==1:
                price=float(village['price'])
                yearpayment=month_payment(price)*12
                current_transportation_cost=(village['now school common transportation'][0][-1]*2*365)
            else:
                price=float(village['current price'])
                yearpayment=month_payment(price)*12
                costs=[]
                for schoolname in schoollist:
                    try:
                        if len(village['common transportation'][schoolname])>0:
                            costs.append(village['common transportation'][schoolname][0][-1]*2*365)
                    except:
                        pass
                current_transportation_cost=np.sum(costs)/len(costs)
            schoolpayment=80*2
            return (yearpayment+current_transportation_cost+schoolpayment)/1000
       
        def Time_cost(village,policy='one',cutoff=10000,year=0):
            schoollist=select_school(village,policy,cutoff,year)
            if len(schoollist)==1:
                current_timecost=village['now school common transportation'][0][1]
            else:
                cost=[]
                for schoolname in schoollist:
                    try:
                        cost.append(village['common transportation'][schoolname][1])
                    except:
                        pass
                current_timecost=np.average(cost)
            
            return current_timecost/60
       
        def Education_resource(village,policy='one',cutoff=10000,year=0):
            schoollist=select_school(village,policy,cutoff,year)
            if len(schoollist)==1:
                current_schoolscore=schooldict[village['school'][0]]['average_score']
            else:
                rlist=[]
                for schoolname in schoollist:
                    rlist.append(schooldict[schoolname]['average_score'])
                current_schoolscore=np.average(rlist)
            return current_schoolscore
       
        for village in villages:
            village['fair index']={}
            village['educost']=Educational_cost(village,policy,cutoff,year)
            village['timecost']=Time_cost(village,policy,cutoff,year)
            village['eduresource']=Education_resource(village,policy,cutoff,year)

        for district in district_neighborinfos.keys():
            #print (district)
            possibility=[village['roomnum'] for village in villages if village['district'][0]==district]
            district_info[district]['possibility']=possibility/np.sum(possibility)
            educost=[village['educost'] for village in villages if village['district'][0]==district]
            timecost=[village['timecost'] for village in villages if village['district'][0]==district]
            eduresource=[village['eduresource'] for village in villages if village['district'][0]==district]
            district_info[district]['min educost'] =(np.min(educost),eduresource[np.argmin(educost)])
            district_info[district]['min timecost']=(np.min(timecost),eduresource[np.argmin(timecost)])
        
        for village in villages:
            village['educost_efficiency']=(village['eduresource']-district_info[village['district'][0]]['min educost'][1])/(village['educost']-district_info[village['district'][0]]['min educost'][0])
            village['timecost_efficiency']=(village['eduresource']-district_info[village['district'][0]]['min timecost'][1])/(village['timecost']-district_info[village['district'][0]]['min timecost'][0])
         
        sum_eduresource={}
        total_eduresource=0
        total_housenum=0

        for district in district_neighborinfos.keys():
            eduresource=np.array([village['eduresource'] for village in villages if village['district'][0]==district])
            housenum=[village['roomnum'] for village in villages if village['district'][0]==district]
            sum_eduresource=np.sum(eduresource*housenum)
            sum_housenum=np.sum(housenum)
            district_info[district]['average eduresource']=sum_eduresource/sum_housenum 
            total_eduresource+=sum_eduresource
            total_housenum+=sum_housenum
         
        total_average_eduresource=total_eduresource/total_housenum
       
        for village in villages:
            village['edu_resource difference district']=village['eduresource']-district_info[village['district'][0]]['average eduresource']
            village['edu_resource difference xicheng']=village['eduresource']-total_average_eduresource
            
        #print (villages[0]['educost'],villages[0]['timecost'],villages[0]['eduresource'],villages[0]['educost_efficiency'],villages[0]['timecost_efficiency'],villages[0]['edu_resource difference district'],villages[0]['edu_resource difference xicheng'])
        for key in schooldict.keys():
            schooldict[key]['neighbor average price']=np.mean([village['current price'] for village in villages if village['school'][0]==key])
            schooldict[key]['neighbor premium']=np.mean([village['current price'] for village in villages if village['school'][0]==key])-district_info[schooldict[key]['district']]['average_price_normal']

        Ginidict={}
        for district in district_neighborinfos.keys():
            Ginidict[district]={}
            for key in ['educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
                fairindex=[village[key] for village in villages if village['district'][0]==district]
                possibility=district_info[district]['possibility']
                #print (key,district)
                g=Gini_coeffient(fairindex,possibility)
                Ginidict[district][key]=g
        
        Ginidict['西城']={}
        for key in ['educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
            fairindex=[village[key] for village in villages]
            housenum=[village['roomnum'] for village in villages]
            possibility=np.array(housenum)/np.sum(housenum)
            g=Gini_coeffient(fairindex,possibility)
            Ginidict['西城'][key]=g
        ginidata=pd.DataFrame(Ginidict)
        Gdictlist.append(Ginidict)
        vdict={}
        #for village in villages:
        vdict['current price']=[village['current price'] for village in villages]
        vdict['educost']=[village['educost'] for village in villages]
        vdict['timecost']=[village['timecost'] for village in villages]
        vdict['eduresource']=[village['eduresource'] for village in villages]
        vdict['school']=[village['school'][0] for village in villages]
        vdict['district']=[village['district'][0] for village in villages]
        vdict['educost_efficiency']=[village['educost_efficiency'] for village in villages]
        vdict['timecost_efficiency']=[village['timecost_efficiency'] for village in villages]
        vdict['edu_resource difference district']=[village['edu_resource difference district'] for village in villages]
        vdict['edu_resource difference xicheng']=[village['edu_resource difference xicheng'] for village in villages]
        vdict['name']=[village['name'] for village in villages]
        vdict['roomnum']=[village['roomnum'] for village in villages]
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
        Vdictlist.append(vdict)
    finalgdict=deepcopy(Gdictlist[0])
    for key1 in finalgdict.keys():
        for key2 in finalgdict[key1].keys():
            finalgdict[key1][key2]=np.mean([tmpdict[key1][key2] for tmpdict in Gdictlist])
    finalvdict=deepcopy(Vdictlist[-1])
    finalginidata=pd.DataFrame(finalgdict)
    finalvdata=pd.DataFrame(finalvdict)
    finalsdata=pd.DataFrame(sdict)
    print (finalginidata)
    finalginidata.to_csv('Xicheng_Gini_%s_%d_%d.csv'%(policy,year,cutoff))
    finalvdata.to_csv('Xicheng_Data_%s_%d_%d.csv'%(policy,year,cutoff))
    finalsdata.to_csv('Xicheng_School_%s_%d_%d.csv'%(policy,year,cutoff))
    return finalvdict,finalsdata,finalginidata


with open('data/villages_allinfo2.json','r') as f:
    tmpvillages=json.load(f)
#    print(tmpvillages[0].keys())
    dict_villages=[]
    for  village in tmpvillages:
        if 'roomnum' in village.keys() and len(village['now school common transportation'])>0:
            if village['roomnum']!='暂无数据':
                dict_villages.append(village)
for village in dict_villages:
    village['roomnum']=int(village['roomnum'][:-1])

with open('data/schools_allinfo2.json','r') as f:
    dict_schools=json.load(f)
now_villages,now_schools,now_gini=fair_analysis(dict_villages,dict_schools,policy='one')
newlist=[]
vlist=[]
slist=[]
ginilist=[]
for year in [0,1,2,3,4,5,6]:
    v,s,gini=fair_analysis(dict_villages,dict_schools,policy='neighbor',year=year)
    vlist.append(v)
    slist.append(s)
    ginilist.append(gini)
village_object=[village['name'] for village in dict_villages]
school_object=[school['school'] for school in dict_schools]
fairindex_object=['current price','educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']
def plot_fair_index_district(years,districts):    
    figdict={}
    for key in ['current price','educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
        figdict[key]=go.Figure()
        nowresult  =[now_villages[key][i]        for i in range(len(now_villages[key])) if now_villages['district'][i] in districts]
        nowdistrict=[now_villages['district'][i] for i in range(len(now_villages[key])) if now_villages['district'][i] in districts]
        
        figdict[key].add_trace(go.Box(y=nowresult,x=nowdistrict,name='2020'))
        for i in range(years[0],years[1]+1,1):
            newresult=[vlist[i][key][j] for j in range(len(vlist[i][key])) if vlist[i]['district'][j] in districts]
            newdistrict=[vlist[i]['district'][j] for j in range(len(vlist[i][key])) if vlist[i]['district'][j] in districts]
            figdict[key].add_trace(go.Box(y=newresult,x=newdistrict,name=str(2020+i)))
        figdict[key].update_layout(
            yaxis_title=key,
            boxmode='group' # group together boxes of the different traces for each value of x
            )
    return [figdict[key] for key in figdict.keys()]

def plot_gini_district(years,districts):
    figdict={}
    for key in ['educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
        figdict[key]=go.Figure()
        for district in districts:
            result=[]
            for i in range(years[0],years[1]+1,1):
                result.append(ginilist[i][district][key])
            figdict[key].add_trace(go.Scatter(x=list(range(2020+years[0],2020+years[1]+1,1)),y=result,name=district))
        figdict[key].update_layout(
            yaxis_title=key,
            xaxis_title='year'
            )
    return [figdict[key] for key in figdict.keys()]

def plot_fair_index_school(years,schools):    
    figdict={}
    for key in ['current price','educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
        figdict[key]=go.Figure()
        nowresult  =[now_villages[key][i]        for i in range(len(now_villages[key])) if now_villages['school'][i] in schools]
        nowdistrict=[now_villages['school'][i]   for i in range(len(now_villages[key])) if now_villages['school'][i] in schools]
        figdict[key].add_trace(go.Box(y=nowresult,x=nowdistrict,name='2020'))
        for i in range(years[0],years[1]+1,1):
            newresult=[vlist[i][key][j] for j in range(len(vlist[i][key])) if vlist[i]['school'][j] in schools]
            newdistrict=[vlist[i]['school'][j] for j in range(len(vlist[i][key])) if vlist[i]['school'][j] in schools]
            figdict[key].add_trace(go.Box(y=newresult,x=newdistrict,name=str(2020+i)))
        figdict[key].update_layout(
            yaxis_title=key,
            boxmode='group' # group together boxes of the different traces for each value of x
            )
    return [figdict[key] for key in figdict.keys()]
def plot_school(years,school):
    figure=go.Figure()
    for key in ['学区房溢价','学区房平均价格','多校划片后原学区房的平均价格','多校划片后原学区房的平均溢价']:
        result=[]
        for i in range(years[0],years[1]+1,1):
            result.append([slist[i][key][j] for j in range(len(slist[i][key])) if slist[i]['学校'][j]==school][0])
        figure.add_trace(go.Scatter(x=list(range(2020+years[0],2020+years[1]+1,1)),y=result,name=key))
    figure.update_layout(
            yaxis_title=school, 
            xaxis_title='year',
            )
    return figure
           
def plot_village(years,village):
    figure=go.Figure()
    for key in ['current price','educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
        result=[]
        for i in range(years[0],years[1]+1,1):
            result.append([vlist[i][key][j] for j in range(len(vlist[i][key])) if vlist[i]['name'][j]==village][0])
        figure.add_trace(go.Scatter(x=list(range(2020+years[0],2020+years[1]+1,1)),y=result,name=key))
    figure.update_layout(
            yaxis_title=village, 
            xaxis_title='year',
            )
    return figure
    
    
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
