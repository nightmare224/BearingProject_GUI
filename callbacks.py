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
app.config['suppress_callback_exceptions'] = True


# can't not add change tab here, or when change to tab2, here will be trigger too
# foo div did not trigger when change tab


@app.callback(
    # the instant name and instant value
    # [Output(component_id = 'fileinfo', component_property = 'children')],
    [Output(component_id = 'fileinfo', component_property = 'value'), Output(component_id = 'memory-output', component_property = 'data')],
    [Input('tab_change', 'children'), Input('bearing_file_upload', 'contents')],
    [State('bearing_file_upload', 'filename'), State('bearing_file_upload', 'last_modified'), State(component_id = 'memory-output', component_property = 'data')]
)
def upload_file(foo, contents, filename, filedates, fileinfo_mem):
    print(foo, filename, fileinfo_mem)
    # filename will be None when switch the tab
    # fileinfo_mem will be None initially
    if (fileinfo_mem != {}) & (fileinfo_mem is not None):
        fileinfo_dict = fileinfo_mem
    elif (filename is not None) and (filename.endswith('.npy') | filename.endswith('.csv') | filename.endswith('.xlsx')):
        fileinfo_dict = {'Filename' : filename, 'Last Modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(filedates)),\
                    'Data Size' : os.stat('./Formal/'+filename)[-4]/1024/1024}
    else:
        # add new branceh : filetype not support in future
        return '', {}


    fileinfo = 'Filename : {}\n\nLast Modified : {}\n\nData Size : {:.2f} MB\n\n'.format(
                fileinfo_dict['Filename'], fileinfo_dict['Last Modified'], fileinfo_dict['Data Size'])



    return fileinfo, fileinfo_dict

# 可以用state當input, 去取得某個物件的狀態



# @app.callback(
#     [Output(component_id = 'fileinfo_page2', component_property = 'value')],
#     [Input('memory-output', 'data')],
# )
# def update_page2(fileinfo_dict):
#     # print(data)

#     fileinfo = 'Filename : {}\n\nLast Modified : {}\n\nData Size : {:.2f} MB\n\n'.format(
#                 fileinfo_dict['Filename'], fileinfo_dict['Last Modified'], fileinfo_dict['Data Size'])

#     return fileinfo,


@app.callback(
    [
        Output(component_id = 'fig1', component_property = 'figure'),
        Output(component_id = 'fig2', component_property = 'figure'),
        Output(component_id = 'fig3', component_property = 'figure')],
    [Input('load_btn', 'n_clicks')],
    [State('bearing_file_upload', 'filename'), State('outlier_detect', 'on')]
)
def load_file(n_clicks, filename, outlier_detect_en):
    # print(filename)
    # print("n clicks = ", n_clicks)
    # print("outlier toggle = ", outlier_detect_en)
    # print('state : ', State('bearing_file_upload', 'filename'))


    # read file
    if filename is None:
        return {},{},{}
    elif filename.endswith('.npy'):
        sourcefile = np.load('./Formal/'+filename)
        print(sourcefile.shape)
    elif filename.endswith('.csv'):
        sourcefile = pd.read_csv(filename)
    elif filename.endswith('.xlsx'):
        sourcefile = pd.read_excel(filename)
    else:
        print('Filetype Not Support')
        return None,
    
    # format file
    mainfile = np.array(sourcefile).reshape(-1)
    if outlier_detect_en:
        mainfile = drop_outlier(mainfile)

    # plot figure of the file
    fig1 = drawGraph(0, mainfile)
    fig2 = drawGraph(1, mainfile)
    fig3 = drawGraph(2, mainfile)

    return fig1, fig2, fig3

def drawGraph(opt, mainfile):
    data = mainfile.copy()
    # print(mainfile.shape)
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


# @app.callback(
#     [
#         Output(component_id = 'fig1', component_property = 'figure'),
#         Output(component_id = 'fig2', component_property = 'figure'),
#         Output(component_id = 'fig3', component_property = 'figure')]
#     [Input('bearing_file_upload', 'contents')],
#     [State('bearing_file_upload', 'filename'), State('bearing_file_upload', 'last_modified')])
# )
# def update_figs():
#     return {}, {}, {}


def drop_outlier(data):
    data = data.copy()
    IF = IsolationForest()
    IF.fit(data.reshape(-1,1))
    outlier = IF.predict(data.reshape(-1,1))
    data = data[outlier==1]

    return data


