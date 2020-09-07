import dash
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



# file upload and show file information


@app.callback(
    # the instant name and instant value
    [Output(component_id = 'fileinfo', component_property = 'children')],
    [Input('bearing_file_upload', 'contents')],
    [State('bearing_file_upload', 'filename'), State('bearing_file_upload', 'last_modified')])
def upload_file(contents, filename, filedates):
    global mainfile, Filename
    Filename = filename
    if filename is None:
        return [],
    elif filename.endswith('.npy') | filename.endswith('.csv') | filename.endswith('.xlsx'):
        pass
    else:
        print('Filetype Not Support')
        return None,
    


    fileinfo = [html.Li('Filename : {}'.format(filename)), 
                html.Li('Last Modified : {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(filedates)))), 
                html.Li('Data Size : {:.2f} MB'.format(os.stat('./Formal/'+filename)[-4]/1024/1024))]

    # print(len(contents))

    return fileinfo,

# 可以用state當input, 去取得某個物件的狀態



@app.callback(
    [
        Output(component_id = 'fig1', component_property = 'figure'),
        Output(component_id = 'fig2', component_property = 'figure'),
        Output(component_id = 'fig3', component_property = 'figure')],
    [Input('load_btn', 'n_clicks')]
)
def load_file(n_clicks):
    print("n clicks = ", n_clicks)
    if n_clicks == 0:
        return {},{},{}

    global mainfile, Filename
    if Filename is None:
        return {},{},{}
    elif Filename.endswith('.npy'):
        sourcefile = np.load('./Formal/'+Filename)
        print(sourcefile.shape)
    elif Filename.endswith('.csv'):
        sourcefile = pd.read_csv(Filename)
    elif Filename.endswith('.xlsx'):
        sourcefile = pd.read_excel(Filename)
    else:
        print('Filetype Not Support')
        # print('filename = ',filename)
        # print('option = ', opt)
        return None,
    
    mainfile = np.array(sourcefile).reshape(-1)

    fig1 = drawGraph(0)
    fig2 = drawGraph(1)
    fig3 = drawGraph(2)

    return fig1, fig2, fig3

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


def outlier_detect(data):
    data = data.copy()
    IF = IsolationForest()
    IF.fit(data.reshape(-1,1))
    outlier = IF.predict(data.reshape(-1,1))
    data = data[outlier==1]

    return data