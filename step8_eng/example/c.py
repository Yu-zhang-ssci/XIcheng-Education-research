import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import plotly.express as px

#district_fig.show()
token='pk.eyJ1IjoibWluZ3l1YW4yMDIwIiwiYSI6ImNrZjE2OHl6cTBwMWIyeXA3dGlpdDczYjAifQ.uBSZVa4tvUUf5pDxwrOKuw'
with open('./data/maps.json','r') as response:
    districts_map = json.load(response)
df = pd.read_csv("./data/mapinfo.csv")

district_fig = px.choropleth(df, geojson=districts_map, locations='area', color='index',featureidkey="properties.name",
                           color_continuous_scale="Viridis",
                           range_color=(0, 10),
                           #opacity=0.5,
                           )
center={"lat":df['lat'][4] , "lon": df['lng'][4]}
district_fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        #mapbox={"accesstoken":token,
        #    'center':center,
        #    'zoom':11,
        #    #'style':"open-street-map"},
        #    #'style':"outdoors"
        #    },
        showlegend=False)
district_fig.show()
