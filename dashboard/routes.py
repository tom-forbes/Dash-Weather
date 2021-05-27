# Logic behind the Page structure and Menu 

#import dash
from dash.dependencies import Input, Output 
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
import live_map_database
import sidebars
# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on

LOGO = "https://upload.wikimedia.org/wikipedia/commons/3/37/Plotly-logo-01-square.png"


sidebar = html.Div(id='side',
        children=[
    html.Div(
    [   html.P(" ", className="display-4"),
        html.H2("My Dash App", className="display-4"),
        html.Hr(),
        html.P(
            "Contents", className="lead"
        ),
        dbc.Nav(
            [   
                dbc.NavLink("Live Map", href="/page-1", id="page-1-link"),
                dbc.NavLink("Page2", href="/page-2", id="page-2-link"),
                #dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
        html.P(" ", className="display-4"),
        html.Img(src=LOGO, height="80px")
    ],
    style=sidebars.SIDEBAR_STYLE,
)
])



'''
Callbacks related to page routing
'''


# Hide / Show the contents menu by clicking the menu button
@app.callback(Output("side", "hidden"), [Input("menu", "n_clicks")])
def input_click(n):
    if n==None:
        return True
    if (n+3)%2==0:
        return False
    else:# (nclick+3)%2==0:
        return True


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
#from routes import routes
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 3)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False#, False
    return [pathname == f"/page-{i}" for i in range(1, 3)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return live_map_database.live_map_layout
    elif pathname == "/page-2":
        return html.P(f"Hello World")
    #elif pathname == "/page-3":
    #    return html.P('Hi')#layout3
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
