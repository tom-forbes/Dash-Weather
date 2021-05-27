
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output 
import plotly.express as px
import pandas as pd
import os
import numpy as np
import json

from app import app
import data
import sidebars 
import routes

content = html.Div(id="page-content", style=sidebars.CONTENT_STYLE)

app.layout = html.Div([ dcc.Location(id="url"), 
                        html.Div([
                                dbc.Button("Menu", outline=False, color="primary", className="mr-1", id='menu')],
                                style={"position": "absolute", "top": "10px", "left": "90px", "zIndex": "4"}),
                        html.Div([
                                routes.sidebar],
                                style={"position": "absolute", "top": "10px", "left": "90px", "zIndex": "3"}), 
                        content
                        ])



@app.callback(
    [Output("plotly-map", "figure"),
    Output("weather-div", "hidden"),
    Output('weather-slider-label', 'children'),
    Output('weather-dropdown2', 'options'),
    Output("weather-slider", "marks"),
    ],
    [
    Input('weather-dropdown2', 'value'),
    Input('weather-slider', 'value'),
    ])
def update_plotly(  weather_dropdown2, weather_slider):
    
    
    weather_dropdown2_opt=[]
    weather_slider_marks={}
    weather_slider_label = ''
    
    date_slider_div=True
    weather_div=False
    if str(weather_dropdown2) == 'None':
        weather_dropdown2 = '2020-09-16'
    
    weather_dropdown2_opt = [{'label':day,'value':day} for day in sorted(os.listdir(os.path.join(data.path,f'CE')))[1:] ]

    
    directory = [i for i in os.listdir(os.path.join(data.path,f'CE/{weather_dropdown2}')) if i[-1]=='n']
    
    sd = data.slider_dict
    weather_slider_marks = {sd[time[11:16]]:time[11:16] for time in directory}
    try:
        weather_slider_label = weather_slider_marks[weather_slider]
    except:
        weather_slider_label = weather_slider_marks[sd[str(directory[0])[11:16]]]

    catchment_bound = data.catchment_boundary
    lat_ = catchment_bound['avg_lat'][catchment_bound['short-code']=='CE'].iloc[0]
    lon_ = catchment_bound['avg_lon'][catchment_bound['short-code']=='CE'].iloc[0]
    zoom = catchment_bound['zoom'][catchment_bound['short-code']=='CE'].iloc[0]
    try:
        df = pd.read_csv(os.path.join(data.path,f'CE/{weather_dropdown2}/{weather_dropdown2}T{weather_slider_label}:00Z_precip15min.csv'))
        
        with open(os.path.join(data.path,f'CE/{weather_dropdown2}/{weather_dropdown2}T{weather_slider_label}:00Z_precip15min.json')) as f:
            p_geojson = json.load(f)
        lons = np.array(p_geojson['features'][-1]['geometry']['coordinates'][0][0]).flatten()[::2]
        if np.var(lons)<0.0000001:
            p_geojson['features'] = p_geojson['features'][:-1]
        p_geojson['features'] = p_geojson['features'][1:]
        
        
        fig = px.choropleth_mapbox(df, geojson=p_geojson, color="Rain",
                                locations="Id", featureidkey="properties.id",
                                center={"lat": lat_, "lon": lon_},
                                mapbox_style="carto-positron", zoom=zoom,
                                color_continuous_scale="jet",
                                range_color=[0,3],
                                height=740,
                                opacity=0.25,)

        fig.update_layout(mapbox_style="carto-positron")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(showlegend=False)
        fig.update_layout(coloraxis_showscale=False)
        
    except:
        pass
        
    # add extra plots (scatter etc. on top of chloropleth map)
    #try:
    #    fig.add_trace(fig2.data[0])
    #    fig.add_trace(fig3.data[0])
    #except:
    #    pass
 
    

    return fig, weather_div, weather_slider_label, weather_dropdown2_opt, weather_slider_marks
     

'''
Callback to show the plotted technolog data 
given the selected map data and various custom values
'''




# Hide / show summary container when summary button clicked
@app.callback(Output("summary-container", "hidden"), [Input("summary-button", "n_clicks")])
def summary_click(nclick):
    if nclick==None:
        return True
    elif (nclick+3)%2==0:
        return False
    else:
        return True


# Hide / Show the alert datatable on the map
# by clicking the alert button
@app.callback(Output("alert-container", "hidden"), [Input("alert-button", "n_clicks")])
def alert_button(nclicks):
    if nclicks==None:
        return True
    elif (nclicks+3)%2==0:
        return False
    else:
        return True




'''
 Run Dash app Code
'''

# Run this code if running locally
if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port=8060, debug=False)

'''
#Run this code if publishing
if __name__ == "__main__":
    # Get port and debug mode from environment variables = os.environ.get('dash_port')
    debug = os.environ.get('dash_debug')=="False"
    app.run_server(debug=debug, host="0.0.0.0", port=port)
'''