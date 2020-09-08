import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.express as px
import pandas as pd
import numpy as np
import time
import os

# outlier detect
from sklearn.ensemble import IsolationForest

from app import app
from layouts import page1_div, page2_div, fileinfo_mem, tab_change

mainfile = np.load('./Formal/Cage_Break.npy').reshape(-1)
fig1 = px.line(mainfile, title = 'Frequency Domain')
fig2 = px.line(mainfile, title = 'Envolope')
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.config['suppress_callback_exceptions'] = True


app.layout = html.Div(children=[
    html.Div(html.H1(children='Bearing Fault Dashboard'), className = 'row'),

    # the style here is internal CSS style
    # example : <h1 style="text-align:center;color:red">......</h1> 
    # html.Div(children=' Dash: A web application framework for Python.', 
            # style = {'text-align':'center','color':'red'}, className = 'row'),

    tab_change,
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Load Data and Draw', value='tab-1'),
        dcc.Tab(label='Classification', value='tab-2')
    ]),
    html.Div(id='pages_content', children = page1_div),
    # a html.Div
    fileinfo_mem,

    # just for notify tab is changing
    

])




@app.callback(
    [Output('pages_content', 'children'), Output('tab_change', 'children')],
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return page1_div,'foo1'
    elif tab == 'tab-2':
        print('page2 here')
        return page2_div, 'foo2'



        


if __name__ == '__main__':
    #app.run_server(host = '', debug=True)
    app.run_server(debug=True)
