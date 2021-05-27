# %%
import pandas as pd
import numpy as np
import plotly.express as px
import geopandas as gpd
import json
import os


import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from numpy import linspace
import geojsoncontour

import data

# script changing multi-point weather data to multipolygon weather data
# crediting code from the following article
# https://towardsdatascience.com/visualizing-spatial-data-with-geojson-heatmaps-1fbe2063ab86
# %%
df = 'file with weather data'
# %%
z = df['value']
y = df['lat']
x = df['lon']

# %%

xi = linspace(x.min(), x.max(), 100)
yi = linspace(y.min(), y.max(), 100)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='linear' )

cs = plt.contourf(xi,yi,zi, 15, cmap=plt.cm.jet)

geojson = geojsoncontour.contourf_to_geojson(
    contourf = cs,
    ndigits = 3
)
p_geojson = eval(geojson)

with open(os.path.join(data.path, 'geo.json'), 'w') as outfile:
    json.dump(p_geojson, outfile)

arr_temp = np.ones([len(p_geojson['features']),2])

list1= []
list2= []
for i in range(0 , len(p_geojson['features']) ):
    p_geojson['features'][i]['id'] =   str(i)
    title = p_geojson['features'][i]['properties']['title'][:4]
    p_geojson['features'][i]['properties']['title'] = title
    list1.append(str(i))
    list2.append(float(p_geojson['features'][i]['properties']['title']))

df_contour = pd.DataFrame()
df_contour['Id'] = list1
df_contour['Rain'] = list2
# %%
with open(os.path.join(data.path, 'geo.json'), 'w') as outfile:
    json.dump(p_geojson, outfile)

# %%
geo = gpd.read_file(os.path.join(data.path, 'geo.json') )
geo['id'] = [str(i) for i in range(len(geo))]
p_geojson = geo[['geometry','id']]
p_geojson
#
p_geojson.to_file(os.path.join(data.path, 'geo.json'), driver='GeoJSON')
# %%
with open(os.path.join(data.path,'geo.json')) as f:
    p_geojson = json.load(f)
p_geojson['features'] = p_geojson['features'][:-1]
# %%

fig = px.choropleth_mapbox(df_contour, geojson=p_geojson, color="Rain",
                           locations="Id", featureidkey="properties.id",
                           center={"lat": 52.1517, "lon": -1.073},
                           mapbox_style="carto-positron", zoom=9,
                           color_continuous_scale="jet",
                           height=740,
                           opacity=0.25,)


fig.show()

# %%
