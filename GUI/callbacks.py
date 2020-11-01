import dash
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
import os
from joblib import load

from GUI.app import app
from GUI.bearingData import bearingFileInfo
from Alog.Header.data_access import DataAccess
import config


# can't not add change tab here, or when change to tab2, here will be trigger too
# foo div did not trigger when change tab


@app.callback(
    [Output(component_id = 'timeSelect', component_property = 'options'), Output(component_id = 'timeSelect', component_property = 'disabled')],
    [Input('dateSelect', 'value')]
)
def filedate_select( filedate ):
    if filedate == None:
        return [], True
    else:
        _, timedict = bearingFileInfo()
        timelist = []
        for time in timedict[filedate]:
            timelist.append({'label':time, 'value':time})

        return timelist, False


@app.callback(
    [
        Output(component_id = 'fileinfo', component_property = 'value'),
        Output(component_id = 'fileinfoMem', component_property = 'data')
    ],
    [Input('timeSelect', 'value')],
    [State('dateSelect', 'value')]
)
def filetime_select( filetime, filedate ):
    #print('cometime = ', filedate, filetime)
    if filetime is None:
        return '', {}
    else:
        fileinfo = 'File Datatime : {}\n\nData Size : {:.2f} MB\n\n'.format( filedate + ' ' + filetime , 1.2)

    return fileinfo, fileinfo




@app.callback(
    [
        Output(component_id = 'tmPlot', component_property = 'figure'),
        Output(component_id = 'freqPlot', component_property = 'figure'),
        Output(component_id = 'pwrPlot', component_property = 'figure'),
        Output(component_id = 'autoCorrPlot', component_property = 'figure'),
        Output(component_id = 'dataMem', component_property = 'data')
    ],
    [Input('load_btn', 'n_clicks')],
    [State('dateSelect', 'value'), State('timeSelect', 'value')]
)
def load_file(loadbtn_clicksno, filedate, filetime):

    if loadbtn_clicksno is None:
        return {}, {}, {}, {}, {}
    
    filename = filedate + '_' + filetime
    dataObj = DataAccess(config.maskFile)
    dataObj.read_file(config.DatabasePath + filename + '.npy')
    x_time, y_time, x_freq, y_freq, x_psd, y_psd, x_atc, y_atc = dataObj.get_data_for_ploty()

    
    # plot figure of the file
    tmPlot = drawTmPlot(x_time, y_time)
    freqPlot = drawFreqPlot(x_freq, y_freq)
    pwrPlot = drawPwrPlot(x_psd, y_psd)
    autoCorrPlot = drawAutoCorrPlot(x_atc, y_atc)
    
    # data for classify
    x = dataObj.get_data_for_classifier()

    return tmPlot, freqPlot, pwrPlot, autoCorrPlot, x

def drawTmPlot(xt, yt):
    fig = go.Figure( data = go.Scatter( x=xt, y=yt, mode='lines'))
    fig.update_layout(title='Time Domain', xaxis_title='t (sec)', yaxis_title='', showlegend=False)
    return fig

def drawFreqPlot(xf, yf):
    fig = go.Figure( data = go.Scatter( x=xf, y=yf, mode='lines'))
    fig.update_layout(title='Frequency Domain', xaxis_title='f (Hz)', yaxis_title='', showlegend=False)
     
    return fig

def drawPwrPlot(xp, yp):
    fig = go.Figure( data = go.Scatter( x=xp, y=yp, mode='lines'))
    fig.update_layout(title='Power Spetral Density', xaxis_title='f (Hz)', yaxis_title='', showlegend=False)

    return fig

def drawAutoCorrPlot(xa, ya):
    fig = go.Figure( data = go.Scatter( x=xa, y=ya, mode='lines'))
    fig.update_layout(title='Autocorrelation', xaxis_title='t (sec)', yaxis_title='', showlegend=False)

    return fig

@app.callback(
    [
        Output(component_id = 'bearing_img', component_property = 'src'),
        Output(component_id = 'faultTypeTxt', component_property = 'children'),
    ],
    [Input('classify_btn', 'n_clicks')],
    [State(component_id = 'dataMem', component_property = 'data')]
)
def classify(n_clicks, data):
    faultType = ['Inner_Break', 'Outer_Break', 'Cage_Break', 'Normal']
    if ( n_clicks is None ) or ( data == {} ) :

        return app.get_asset_url('NoImage.png'), 'Bearing Fault Type'
        
    # load model
    rfModel = load(config.ModelFile)
    result = rfModel.predict(data)
    #unq, cnt = np.unique(result, return_counts = True)
    #result = unq[np.argmax(cnt)]
    # choose first result
    result = result[0]
    # fault type name
    faultTypeTxt = faultType[result].replace('_', ' ')
    faultTypeTxt = 'Bearing Fault Type - {}'.format(faultTypeTxt)

    return app.get_asset_url(faultType[result] + '.png'), faultTypeTxt


@app.callback(
        [Output(component_id = 'selFileinfo', component_property = 'value')],
        [Input('tabs', 'value')],
        [
            State(component_id = 'dataMem', component_property = 'data'),
            State(component_id = 'fileinfoMem', component_property = 'data')
        ]
)
def updateFileinfo(foo, dataMem, fileinfo):
    # file not select yet
    if dataMem == {}:
        return 'Please select the file first',
    else:
        return fileinfo,

@app.callback(
        Output(component_id = 'confusMatrix', component_property = 'src'),
        Input('confusMatrix', 'id')
)
def uploadConfusMatrix(foo):
    return app.get_asset_url('confusionMatrix.png')
