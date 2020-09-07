import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html

import plotly.express as px
import pandas as pd
import numpy as np
import time
import os

# outlier detect
from sklearn.ensemble import IsolationForest

from layouts import page1_div, page2_div

# add in persistence=True dcc to prevent refresh while switching https://dash.plotly.com/persistence


external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css','https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


mainfile = np.load('./Formal/Cage_Break.npy').reshape(-1)
fig1 = px.line(mainfile, title = 'Frequency Domain')
fig2 = px.line(mainfile, title = 'Envolope')
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")







app.layout = html.Div(children=[
    html.Div(html.H1(children='Dashboard'), className = 'row'),

    # the style here is internal CSS style
    # example : <h1 style="text-align:center;color:red">......</h1> 
    # html.Div(children=' Dash: A web application framework for Python.', 
            # style = {'text-align':'center','color':'red'}, className = 'row'),

   
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Load Data and Draw', value='tab-1'),
        dcc.Tab(label='Classification', value='tab-2')
    ]),
    html.Div(id='pages_content', children = page1_div)

])




from dash.dependencies import Output, Input, State
@app.callback(
    # the instant name and instant value
    [
        Output(component_id = 'fig1', component_property = 'figure'),
        Output(component_id = 'fig2', component_property = 'figure'),
        Output(component_id = 'fig3', component_property = 'figure'),
        Output(component_id = 'fileinfo', component_property = 'children')],
    [Input('bearing_file_upload', 'contents')],
    [State('bearing_file_upload', 'filename'), State('bearing_file_upload', 'last_modified')])
def upload_file(contents, filename, filedates):
    global mainfile
    if filename is None:
        return {},{},{},[]
    elif filename.endswith('.npy'):
        sourcefile = np.load('./Formal/'+filename)
        print(sourcefile.shape)
    elif filename.endswith('.csv'):
        sourcefile = pd.read_csv(filename)
    elif filename.endswith('.xlsx'):
        sourcefile = pd.read_excel(filename)
    else:
        print('Filetype Not Support')
        # print('filename = ',filename)
        # print('option = ', opt)
        return None,
    
    mainfile = np.array(sourcefile).reshape(-1)
    # always outlier detect
    mainfile = outlier_detect(mainfile)

    # fig = drawGraph(opt)
    fig1 = drawGraph(0)
    fig2 = drawGraph(1)
    fig3 = drawGraph(2)

    fileinfo = [html.Li('Filename : {}'.format(filename)), 
                html.Li('Last Modified : {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(filedates)))), 
                html.Li('Data Size : {:.2f} MB'.format(os.stat('./Formal/'+filename)[-4]/1024/1024))]



    # print(len(contents))

    return fig1, fig2, fig3, fileinfo

def drawGraph(opt):
    data = mainfile.copy()
    print(mainfile.shape)
    # time domain
    if opt == 0:
        data = data[:4096]
        fig = px.line(data, title = 'Time Domain')
    # frquence domain
    elif opt == 1:
        # data = data[:2000]
        fdata = np.fft.fft(data)
        x = fdata.real
        y = abs(fdata)
        fig = px.scatter(x,y)
    # envelope
    elif opt == 2:
        data = data[:1000]
        fig = px.line(data)
    # print(data)

    # must add comma, to be an tuple
    return fig

@app.callback(Output('pages_content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return page1_div
    elif tab == 'tab-2':
        return page2_div

def outlier_detect(data):
    data = data.copy()
    IF = IsolationForest()
    IF.fit(data.reshape(-1,1))
    outlier = IF.predict(data.reshape(-1,1))
    data = data[outlier==1]

    return data

        


if __name__ == '__main__':
    #app.run_server(host = '', debug=True)
    app.run_server(debug=True)

