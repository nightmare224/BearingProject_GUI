import dash
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.express as px
import pandas as pd
import numpy as np
import time
import os

# # outlier detect
# from sklearn.ensemble import IsolationForest
from app import app

from bearingData import bearingFileInfo

# file upload and show file information
app.config['suppress_callback_exceptions'] = True


# can't not add change tab here, or when change to tab2, here will be trigger too
# foo div did not trigger when change tab

@app.callback(
    [Output(component_id = 'timeSelect', component_property = 'options'), Output(component_id = 'timeSelect', component_property = 'disabled')],
    [Input('dateSelect', 'value')]
)
def filedate_select( filedate ):

    print('come date')
   

    if filedate == None:
        print('here')
        return [], True
    else:
        _, timedict = bearingFileInfo()
        timelist = []
        for time in timedict[filedate]:
            timelist.append({'label':time, 'value':time})

        return timelist, False


@app.callback(
    [Output(component_id = 'fileinfo', component_property = 'value'), Output(component_id = 'memory-output', component_property = 'data')],
    [Input('timeSelect', 'value')],
    [State('dateSelect', 'value')]
)
def filetime_select( filetime, filedate ):
    print('cometime = ', filedate, filetime)
    if filetime is None:
        return '', {}
    else:
        fileinfo = 'File Datatime : {}\n\nData Size : {:.2f} MB\n\n'.format( filedate + ' ' + filetime , 1.2)


    return fileinfo, {}


# @app.callback(
#     # the instant name and instant value
#     # [Output(component_id = 'fileinfo', component_property = 'children')],
#     [Output(component_id = 'fileinfo', component_property = 'value'), Output(component_id = 'memory-output', component_property = 'data')],
#     [Input('tab_change', 'children'), Input('bearing_file_upload', 'contents')],
#     [State('bearing_file_upload', 'filename'), State('bearing_file_upload', 'last_modified'), State(component_id = 'memory-output', component_property = 'data')]
# )
# def upload_file(foo, contents, filename, filedates, fileinfo_mem):
#     # print(foo, filename, fileinfo_mem)
#     # filename will be None when switch the tab
#     # fileinfo_mem will be None initially

#     if (filename is not None) and (filename.endswith('.npy') | filename.endswith('.csv') | filename.endswith('.xlsx')):
#         fileinfo_dict = {'Filename' : filename, 'Last Modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(filedates)),\
#         'Data Size' : os.stat('./Formal/'+filename)[-4]/1024/1024}
#     elif (fileinfo_mem != {}) & (fileinfo_mem is not None):
#         fileinfo_dict = fileinfo_mem
#     else:
#         # add new branceh : filetype not support in future
#         return '', {}


#     fileinfo = 'Filename : {}\n\nLast Modified : {}\n\nData Size : {:.2f} MB\n\n'.format(
#                 fileinfo_dict['Filename'], fileinfo_dict['Last Modified'], fileinfo_dict['Data Size'])



#     return fileinfo, fileinfo_dict






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
    [State('dateSelect', 'value'), State('timeSelect', 'value')]
)
def load_file(loadbtn_clicksno, filedate, filetime):

    if loadbtn_clicksno is None:
        return {}, {}, {}
    
    filename = filedate + '_' + filetime

    # read file
    # if filename is None:
    #     return {},{},{}
    # elif filename.endswith('.npy'):
    #     sourcefile = np.load('./Formal/'+filename)
    # elif filename.endswith('.csv'):
    #     sourcefile = pd.read_csv(filename)
    # elif filename.endswith('.xlsx'):
    #     sourcefile = pd.read_excel(filename)
    # else:
    #     print('Filetype Not Support')
    #     return None,
    
    # format file
    mainfile = np.array(sourcefile).reshape(-1)
    if outlier_detect_en:
        mainfile = drop_outlier(mainfile)

    # plot figure of the file
    fig1 = drawGraph(0, mainfile)
    fig2 = drawGraph(1, mainfile)
    fig3 = drawGraph(2, mainfile)


    #return fig1, fig2, fig3

    # get two plot

    return get_preprocess_plot([filename], [filename])

@app.callback(
    [Output(component_id = 'bearing_img', component_property = 'src')],
    [Input('classify_btn', 'n_clicks')],
    [State(component_id = 'memory-output', component_property = 'data')]
)
def classify(n_clicks, fileinfo_mem):
    if ( n_clicks != None ) & (fileinfo_mem != {}) & (fileinfo_mem is not None):
        # 暫時寫死, 考檔名分類, 之後要改成演算法
        return app.get_asset_url(fileinfo_mem['Filename'][:-4] + '.png'),
    else:
        return None,


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
        fig = px.scatter(x,y, title = 'Frequence Domain')
    # envelope
    elif opt == 2:
        data = data[:1000]
        fig = px.line(data, title = 'Envelope Curve')
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
    mask = []
    different = []
    datas = data.reshape(-1,128)
    for tmp in datas:
        different.append(abs(np.max(tmp)-np.min(tmp)))
    different = np.array(different)

    lower, upper = np.percentile(different, [10,90])
    mask = (different >= lower) & (different <= upper)
    datas = datas[mask]
    # data = data.copy()
    # IF = IsolationForest()
    # IF.fit(data.reshape(-1,1))
    # outlier = IF.predict(data.reshape(-1,1))
    # data = data[outlier==1]

    return datas.reshape(-1)
