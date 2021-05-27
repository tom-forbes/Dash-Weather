# %%
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

weather_bar = html.Div([
        
        html.Div(id = 'weather-div', children=[
            html.Div([
                dcc.Dropdown(id='weather-dropdown',
                    options=[{'label':catchment,'value':catchment} for catchment in ['CE']],#sorted(data.catchments)+['NE']],
                value='CE',#sorted(data.catchments)[0]
                            ),
                dcc.Dropdown(id='weather-dropdown2'),
                dbc.Label(id='weather-slider-label'),
                ], style={'width':'20rem',"position": "fixed", "top": 550,"bottom": 60,"left": 100, 'zIndex':5}),
        html.Div([
            dcc.Slider(id='weather-slider',
                                            min=1,
                                            max=96,
                                            step=1,#None
                                            value=1,
                                            #updatemode='drag',
                                            #vertical=True,
                                            #verticalHeight=740
                                        ), 
        ],    style={'width':'75rem',"position": "fixed", "top": 650,"bottom": 10,"left": 100, "right": 100, 'zIndex':4}),
        ]),
    ],style={"position": "fixed", "top": 0,"left": 0, 'zIndex':7})

        

# %%

live_map_layout = html.Div(children=[
    html.Div(children=[
        dcc.Graph(id='plotly-map'),
         ]),
        weather_bar 
        ])

# %%
