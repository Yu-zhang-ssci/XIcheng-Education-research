# -*- coding: utf-8 -*-
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from ginical import * 
token='pk.eyJ1IjoibWluZ3l1YW4yMDIwIiwiYSI6ImNrZjE2OHl6cTBwMWIyeXA3dGlpdDczYjAifQ.uBSZVa4tvUUf5pDxwrOKuw'

def get_village_info(filename):
    villagelist=pd.read_json(filename)
    return villagelist
def get_statistic_data(filename):
    statistics=pd.read_csv(filename)
    return statistics

villages=get_village_info('./data/villages_allinfo.json')
statistics=get_statistic_data('./data/statistic.csv')
schools=pd.read_json('./data/schools_allinfo.json')
print (schools)


with open('./data/maps.json','r') as response:
    districts_map = json.load(response)

df = pd.read_csv("./data/mapinfo.csv")
print (df)
import plotly.express as px

#district_fig.show()

import dash
import dash_core_components as dcc
import dash_html_components as html
from details import *#info,districtdict
app = dash.Dash(__name__,meta_tags=[{"name":"viewport","content":"width=device-width"}])
app.layout = html.Div(
        children=
        [
             html.H2(id='Title',children="北京市西城区教育公平与资源配置研究",style={"width":"100%","text-align":"center","height":"50px","color":"#999"}),
             html.Div(id='Body',children=
             [
                html.Div(id='Map module',children=
                    [
                        html.Div(children=
                            dcc.RangeSlider(
                                       id='year',
                                       min=0,
                                       max=6,
                                       value=[0,6],
                                       marks={str(i):str(i+2020) for i in range(7)},
                                       step=1
                                       ),
                             style={"width":"80%","margin":"auto","height":"50px","align-item":"center"}),
                        html.Div(children=
                            [
                            #    dcc.Graph(figure=district_fig)
                            ],id='Map'),
                        html.Div(children=
                            dcc.Slider(id='districts',
                                       min=0,
                                       max=11,
                                       value=1,
                                       marks=districtdict,
                                       step=None),
                            style={"width":"85%","margin":"auto","height":"50px","align-item":"center"})
                        
                     ],className='pretty_container eight columns'),
                html.Div(id='left_module',children=[
                    html.Div(id='control tabs',children=
                    [
                        dcc.Tabs(id='tabs',value='what-is',children=
                        [
                        dcc.Tab(label='介绍',value='what-is',children=
                            [
                                html.Div(children=
                                [
                                    html.P(info['introduction'],\
                                        style={"text-align":"center","height":"100%"})
                                ])
                            ]),
                        dcc.Tab(label='控制',value='control page',id='control page',children=
                            [
                                html.Div(id='variable control',children=[
                                    html.Div(children=[
                                        html.Div(id='transport div',children=
                                            [
                                            html.P('适龄儿童上学交通方式',style={"text-align":"center"}),
                                            dcc.Dropdown(id='transport',
                                                         options=[{'label':op,'value':op} for op in avaliable_transportation],
                                                         value=avaliable_transportation[0],
                                                         style={"margin":"auto","width":"90","padding":"10px"},
                                                         multi=True),
                                            ],style={"width":"50%"}),
                                        html.Div(id='income div',children=
                                            [
                                            html.P('可支配收入水平',style={"text-align":"center"}),
                                            dcc.Dropdown(id='Income level',
                                                         options=[{'label':op,'value':op} for op in avaliable_incomelevel],
                                                         value=avaliable_incomelevel[0],
                                                         style={"margin":"auto","width":"90","padding":"10px"}),
                                            ],style={"width":"50%"})
                                        ],style={"display":"flex",'height':"4%"}),

                                    html.Div(children=[
                                        html.Div(id='policy div',children=
                                            [
                                            html.P('适龄儿童入学政策',style={"text-align":"center"}),
                                            dcc.Dropdown(id='policy',
                                                     options=[{'label':op,'value':op} for op in avaliable_policy],
                                                     value=avaliable_policy[0],
                                                     style={"margin":"auto","width":"90","padding":"10px"}),
                                            ],style={"width":"50%","align-item":"center"}),
                                        html.Div(id='research div',children=[
                                            html.P('教育公平观测维度',
                                                    style={"text-align":"center"}),
                                            dcc.Dropdown(id='research object',
                                                        options=[{'label':op,'value':op} for op in avaliable_research_object],
                                                        value=avaliable_research_object[0],
                                                        style={"margin":"auto","width":"90","padding":"10px"}),
                                        ],style={"width":"50%","align-item":"center"}),                                        
                                    ],style={"display":"flex","height":"4%"}),
                                    html.Div(id='show div',children=[
                                            html.P('显示信息',
                                                   style={"text-align":"center"}),    
                                            dcc.Dropdown(id='show object',
                                                         options=[{'label':op,'value':op} for op in avaliable_show_object],
                                                         value=[avaliable_show_object[1],avaliable_show_object[2]],
                                                         multi=True,
                                                         style={"width":"90%","margin":"auto","padding":"10px"})
                                        ],style={"width":"100%"})
                                ],style={"width":"100%"})
                            ]),
                        dcc.Tab(label='信息',value='info page',id='info page',children=[
                                            html.P('小区信息',
                                                   style={"text-align":"center"}),
                                            dcc.Dropdown(id='village option',
                                                         options=[{'label':op,'value':op} for op in avaliable_village_info],
                                                         value=avaliable_village_info[0],
                                                         style={"width":"90%","margin":"auto","padding":"10px"}),
                                            html.P('学校信息',
                                                   style={"text-align":"center"}),
                                            dcc.Dropdown(id='school option',
                                                         options=[{'label':op,'value':op} for op in avaliable_school_info],
                                                         value=avaliable_school_info[0],
                                                         style={"width":"90%","margin":"auto","padding":"10px"}),
                                            html.P('学区信息',
                                                   style={"text-align":"center"}),
                                            dcc.Dropdown(id='district option',
                                                         options=[{'label':op,'value':op} for op in avaliable_district_info],
                                                         value=avaliable_district_info[0],
                                                         style={"width":"90%","margin":"auto","padding":"10px"}),
                        ]),
                        dcc.Tab(label='建议',value='advice page',id='advice page',children=[]),
                        ])
                    ],className='pretty_container',style={"height":"42%"}),
                    html.Div(id='Data option',children=[
                        dcc.Dropdown(id='statistic option',
                                    options=[{'label':op,'value':op} for op in avaliable_statistics],
                                    value=avaliable_statistics[1],
                                    style={"width":"90%","margin":"auto","align":"center"}),
                    ],className='pretty_container'),
                    html.Div(id='Data show',className="pretty_container",style={"height":"42%"})
                ],className='four columns',style={'height':'930px'})
            ],className='raw flex-display',style={"color":"#999"}),
            html.Div(id='statistic chart',children=[
                html.Div(id='district select',
                        children=[
                                    html.P('学区',
                                            style={"text-align":"center"}),    
                                    dcc.Dropdown(id='district object',
                                                 options=[{'label':op,'value':op} for op in district_object],
                                                 value=[district_object[1],district_object[2]],
                                                 multi=True,
                                                 style={"width":"90%","margin":"auto","padding":"10px"})
                        ],
                className="pretty_container four columns"),
                html.Div(id='school select',
                        children=[
                                    html.P('学校',
                                            style={"text-align":"center"}),    
                                    dcc.Dropdown(id='school object',
                                                 options=[{'label':op,'value':op} for op in school_object],
                                                 value=[school_object[1],school_object[2]],
                                                 multi=True,
                                                 style={"width":"90%","margin":"auto","padding":"10px"}) 
                        ],
                className="pretty_container four columns"),
                html.Div(id='fair index select',
                        children=[
                                    html.P('公平性指标',
                                            style={"text-align":"center"}),    
                                    dcc.Dropdown(id='fairindex object',
                                                 options=[{'label':op,'value':op} for op in fairindex_object],
                                                 value=fairindex_object[1],
                                                 multi=False,
                                                 style={"width":"90%","margin":"auto","padding":"10px"}) 
                        ],
                className="pretty_container four columns"),
                
            ],className='raw flex-display',style={"color":"#999"}),
            html.Div(id='fairindex district display chart',children=[
                html.Div(id='fairindex_district',
                        children=[
                                    html.P('各学区公平性指标分布',
                                            style={"text-align":"center"}),    
                                    html.Div(id='district fairindex show',className="pretty_container",style={"height":"300px"})
                        ],
                className="pretty_container twelve columns"),],style={"color":"#999"}),
            html.Div(id='fairindex school display chart',children=[
                html.Div(id='fairindex_school',
                        children=[
                                    html.P('各学校学区房对应公平性指标分布',
                                            style={"text-align":"center"}),   
                                    html.Div(id='school fairindex show',className="pretty_container",style={"height":"300px"})
                        ],
                className="pretty_container twelve columns")
            ],style={"color":"#999"}),#className='raw flex-display',style={"color":"#999"}),
            html.Div(id='gini display chart',children=[
                html.Div(id='gini display',
                    children=[
                                html.P('各学区公平性指标的基尼系数变化',
                                            style={"text-align":"center"}), 
                                html.Div(id='gini show',className="pretty_container",style={"height":"300px"})
                ],className="pretty_container twelve columns") ,
                
                #html.Div(id='school display',
                #    children=[
                #                html.P('学校属性变化',
                #                            style={"text-align":"center"}), 
                #                html.Div(id='school show',className="pretty_container",style={"height":"42%"})
                #],className="pretty_container four columns") ,   
                #html.Div(id='village display',
                #    children=[
                #                html.P('学校属性变化',
                #                            style={"text-align":"center"}), 
                #                html.Div(id='village show',className="pretty_container",style={"height":"42%"})
                #],className="pretty_container four columns") ,   
                
                
            ],style={"color":"#999"}),#className='raw flex-display',style={"color":"#999"}),
        ])

from dash.dependencies import Input,Output

@app.callback(Output('Data show','children'),[Input('statistic option','value')])
def show_statics(value):
    if value in ['家庭户均人口数','人均可支配收入','人均消费支出','教育支出','教育文化娱乐总支出','每一就业负担人数','恩格尔系数','小学招生数']:
        statisticsdat=go.Scatter(
            x=statistics['年份'],
            y=statistics[value], 
            mode='markers+lines',
            opacity=0.7,
            marker={'size':10},            
        )
        #fig=go.Figure(statisticsdat)
        #fig.show()
        statisticlayout=go.Layout(margin={"r":60,"t":40,"l":60,"b":40},
                                  xaxis={"title":"年份"},
                                  yaxis={"title":value},
                                  showlegend=False)
        return dcc.Graph(figure={"data":[statisticsdat],"layout":statisticlayout},
                         style={"height":"100%","width":"100%"})
#@app.callback(Output('Transportation Time Cost','children'),[Input('year','value'),Input('districts','value')])
#def show_transportation_statistics(year,districtindex):

@app.callback(Output('Map','children'),[Input('year','value'),\
                                        Input('districts','value'),\
                                        Input('show object','value'),\
                                        Input('village option','value'),\
                                        Input('school option','value'),\
                                        Input('district option','value')])
def show_maps(year,districtindex,objects_show,village_option,school_option,district_option):
    print (year)
    year=year[0]+2010
    districtname=districtdict[str(districtindex)]
    print (year,districtname,objects_show)
    if '学区信息' in objects_show:
        district_opacity=0.3
    else:
        district_opacity=0.7

    district_fig = px.choropleth_mapbox(df, geojson=districts_map, locations='area', color='index',featureidkey="properties.name",
                           color_continuous_scale="Viridis",
                           range_color=(0, 10),
                           #color_discrete_map={'A':'b','B':'red','C':'green','D':'gray','E':'orange','F':'puple','G':'yellow','H':'g','I':'brown','J':'r','K':'orange'},
                           opacity=district_opacity,)
    
    if '小区信息' in objects_show:
        if  village_option=='位置':
            village_hovertext=[villages.name[i]+' '+villages.address[i] for i in range(len(villages))]
            village_marker={
                'size':10,'opacity':0.7,
                #'symbol':["town" for i in range(len(villages.price))]
            }       
        elif village_option=='房价':
            village_hovertext=[villages.name[i]+' %.2f'%villages.price[i]+' %s'%villages['school'][i][0] for i in range(len(villages))]
            village_marker={
                'size':(villages.price-np.min(villages.price))/(np.max(villages.price)-np.min(villages.price))*30+2,
                'color':villages.price,
                'opacity':0.7
            }
        """
        district_fig.add_trace(go.Scattermapbox(mode='markers',
                                     lon = villages.wgs84lng,
                                     lat = villages.wgs84lat,
                                     hovertext = village_hovertext,
                                     hoverinfo = 'text',
                                     marker=village_marker,
                                     ))
        """
        district_fig.add_trace(go.Densitymapbox(lat=villages.wgs84lat,lon=villages.wgs84lng,z=villages.price,radius=20))
        
    if '学校信息' in objects_show:
        if school_option=='位置':
            school_hovertext=[schools.school[i]+' '+schools.addressnum[i]+' '+schools.district[i]+' %.4f,%.4f'%(schools.gcj02lng[i],schools.gcj02lat[i]) for i in range(len(schools))]
            #school_marker={'size':30,'opacity':0.7,'color':[districtindexdict[schools.district[i].strip('学区')] for i in range(len(schools))],
            school_marker={'size':20,
                    'symbol':["bus" for i in range(len(schools))]}
        elif school_option=="管理水平":
            school_hovertext=[schools.school[i]+' '+str(schools.envir_score[i]) for i in range(len(schools))]
            school_marker={'size':(schools.envir_score-np.min(schools.envir_score))/(np.max(schools.envir_score)-np.min(schools.envir_score))*40+10,
                            'color':schools.envir_score,
            }
        elif school_option=="北京市学科带头人人数":
            school_hovertext=[schools.school[i]+' '+str(schools.city_leadernum[i]) for i in range(len(schools))]
            school_marker={'size':(schools.city_leadernum-np.min(schools.city_leadernum))/(np.max(schools.city_leadernum)-np.min(schools.city_leadernum))*40+10,
                            'color':schools.city_leadernum,
            }
        elif school_option=="北京市学科骨干教师人数":
            school_hovertext=[schools.school[i]+' '+str(schools.city_teachernum[i]) for i in range(len(schools))]
            school_marker={'size':(schools.city_teachernum-np.min(schools.city_teachernum))/(np.max(schools.city_teachernum)-np.min(schools.city_teachernum))*40+10,
                            'color':schools.city_teachernum,
            }
        elif school_option=="学校等级":
            school_hovertext=[schools.school[i]+' '+schools.level[i] for i in range(len(schools))]
            datarray=np.array([school_leveldict[schools.level[i]] for i in range(len(schools))])
            school_marker={'size':(datarray-np.min(datarray))/(np.max(datarray)-np.min(datarray))*40+10,
                            'color':datarray,
            }
        elif school_option=="家长评分":
            school_hovertext=[schools.school[i]+' '+str(schools.score[i]) for i in range(len(schools))]
            school_marker={'size':(schools.score-np.min(schools.score))/(np.max(schools.score)-np.min(schools.score))*40+10,
                            'color':schools.score,
            }
        elif school_option=="综合评分":
            datarray=np.array([school_leveldict[schools.level[i]] for i in range(len(schools))])
            avgscore=(schools.envir_score-np.min(schools.envir_score))/(np.max(schools.envir_score)-np.min(schools.envir_score))+\
                     (schools.city_leadernum-np.min(schools.city_leadernum))/(np.max(schools.city_leadernum)-np.min(schools.city_leadernum))+\
                     (schools.city_teachernum-np.min(schools.city_teachernum))/(np.max(schools.city_teachernum)-np.min(schools.city_teachernum))+\
                     (datarray-np.min(datarray))/(np.max(datarray)-np.min(datarray))+\
                     (schools.score-np.min(schools.score))/(np.max(schools.score)-np.min(schools.score))
            avgscore=avgscore/5.0*100
            school_marker={'size':(avgscore-np.min(avgscore))/(np.max(avgscore)-np.min(avgscore))*40+10,
                           'color':avgscore,
            }
            school_hovertext=[schools.school[i]+' '+str(avgscore[i]) for i in range(len(schools))]
        district_fig.add_trace(go.Scattermapbox(mode='markers',
                                     lon = schools.wgs84lng,
                                     lat = schools.wgs84lat,
                                     text = school_hovertext,
                                     #hoverinfo = 'text',
                                     marker = school_marker,))
    
    if districtindex<11:
        zoomlevel=14
        center={"lat":df['lat'][districtindex],"lon":df['lng'][districtindex]}
    else:
        zoomlevel=12
        center={"lat":df['lat'][4] , "lon": df['lng'][4]}
    district_fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox={"accesstoken":token,
            'center':center,
            'zoom':zoomlevel,
            #'style':"open-street-map"},
            #'style':"outdoors"
            "style":"light"},
        showlegend=False,
        height=800,)
    return dcc.Graph(figure=district_fig)

@app.callback(Output('district fairindex show','children'),[Input('year','value'),Input('district object','value'),Input('fairindex object','value')])
def plot_fair_index_district(years,districts,key):    
    figdict={}
    #for key in ['current price','educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
    figdict[key]=go.Figure()
    nowresult  =[now_villages[key][i]        for i in range(len(now_villages[key])) if now_villages['学区'][i] in districts]
    nowdistrict=[now_villages['学区'][i] for i in range(len(now_villages[key])) if now_villages['学区'][i] in districts]
    figdict[key].add_trace(go.Box(y=nowresult,x=nowdistrict,name='2020'))
    for i in range(years[0],years[1]+1,1):
        newresult=[vlist[i][key][j] for j in range(len(vlist[i][key])) if vlist[i]['学区'][j] in districts]
        newdistrict=[vlist[i]['学区'][j] for j in range(len(vlist[i][key])) if vlist[i]['学区'][j] in districts]
        figdict[key].add_trace(go.Box(y=newresult,x=newdistrict,name=str(2020+i)))
    figdict[key].update_layout(
        yaxis_title=key,
        boxmode='group', # group together boxes of the different traces for each value of x
        margin={"r":60,"t":40,"l":60,"b":40},
        )
    return [dcc.Graph(figure=figdict[key],
                         style={"height":"100%","width":"100%"})]

@app.callback(Output('school fairindex show','children'),[Input('year','value'),Input('school object','value'),Input('fairindex object','value')])
def plot_fair_index_school(years,schools,key):    
    figdict={}
    #for key in ['current price','educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
    figdict[key]=go.Figure()
    nowresult  =[now_villages[key][i]        for i in range(len(now_villages[key])) if now_villages['学校'][i] in schools]
    nowdistrict=[now_villages['学校'][i]   for i in range(len(now_villages[key])) if now_villages['学校'][i] in schools]
    figdict[key].add_trace(go.Box(y=nowresult,x=nowdistrict,name='2020'))
    for i in range(years[0],years[1]+1,1):
        newresult=[vlist[i][key][j] for j in range(len(vlist[i][key])) if vlist[i]['学校'][j] in schools]
        newdistrict=[vlist[i]['学校'][j] for j in range(len(vlist[i][key])) if vlist[i]['学校'][j] in schools]
        figdict[key].add_trace(go.Box(y=newresult,x=newdistrict,name=str(2020+i)))
    figdict[key].update_layout(
        yaxis_title=key,
        boxmode='group', # group together boxes of the different traces for each value of x
        margin={"r":60,"t":40,"l":60,"b":40},
        )
    return [dcc.Graph(figure=figdict[key],
                         style={"height":"100%","width":"100%"})]

@app.callback(Output('gini show','children'),[Input('year','value'),Input('district object','value'),Input('fairindex object','value')])                         
def plot_gini_district(years,districts,key):
    figdict={}
    #for key in ['educost','timecost','eduresource','educost_efficiency','timecost_efficiency','edu_resource difference district','edu_resource difference xicheng']:
    figdict[key]=go.Figure()
    for district in districts:
        result=[]
        for i in range(years[0],years[1]+1,1):
            result.append(ginilist[i][district][key])
        figdict[key].add_trace(go.Scatter(x=list(range(2020+years[0],2020+years[1]+1,1)),y=result,name=district))
    figdict[key].update_layout(
        yaxis_title=key,
        xaxis_title='year',
        margin={"r":60,"t":40,"l":60,"b":40}, 
        )
    return [dcc.Graph(figure=figdict[key],
                         style={"height":"100%","width":"100%"})]

if __name__=="__main__":
    app.run_server(debug=True, use_reloader=True)
