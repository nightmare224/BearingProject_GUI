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

# add in persistence=True dcc to prevent refresh while switching https://dash.plotly.com/persistence


external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css','https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


mainfile = np.load('./Formal/Cage_Break.npy').reshape(-1)
fig1 = px.line(mainfile, title = 'Frequency Domain')
fig2 = px.line(mainfile, title = 'Envolope')
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

page1 =\
    html.Div(id = 'page1', children = [
        html.Div(children = [
            html.Div(children = [
                dcc.Upload(
                    id = 'bearing_file_upload',
                    children = html.Div( ['Drag and Drop or ', html.A('Select Files')], style =  {'position' : 'relative','top':'14px'} ),
                    multiple = False,
                    style = {
                        'position' : 'relative',
                        'top' : '40px',
                        'left' : '20px',
                        'width' : '250px',
                        'height' : '60px',
                        'textAlign': 'center',
                        'borderStyle' : 'dashed',
                        'background-color' : '#ffffff',
                        'font-style': 'italic',
                        'font-weight' : 'bold'
                    }
                ),
                html.Div(id = 'fileinfo', children = [
                    dcc.Markdown('''
                        #### Dash and Markdown

                        Dash supports [Markdown](http://commonmark.org/help).

                        Markdown is a simple way to write and format text.
                        It includes a syntax for things like **bold text** and *italics*,
                        [links](http://commonmark.org/help), inline `code` snippets, lists,
                        quotes, and more.
                    ''')],
                    style = {
                        'position' : 'relative',
                        'top' : '60px',
                        'background-color' : '#f0f0f5',
                        'width' : '280px',
                        'height' : '200px',
                        'left' : '15px',
                        # 'text-align' : 'center'
                    }
                ),


                html.Button('Load', 
                    id='button', 
                    style = {
                        'position' : 'relative',
                        'top' : '80px',
                        'left' : '200px',
                        'background-color' : 'white',
                        'height' : '80px'
                    }
                ),
                # dcc.RadioItems(
                #     options=[
                #         {'label': 'Origianl', 'value': '0'},
                #         {'label': 'Drop Outlier', 'value': '1'}
                #     ],
                #     value='0',
                #     labelStyle={'display': 'inline-block'},
                #     style = {
                #         'position' : 'relative',
                #         'top' : '30px',
                #         'left' : '10px'
                #     }
                # )
                # relative : compare with original position
                daq.BooleanSwitch(
                    id='outlier_detect',
                    label = 'Enable Outlier Detection',
                    labelPosition = 'top',
                    on=False,
                    style = {
                        'position' : 'relative',
                        'top' : '0px',
                        'right' : '50px'
                    }
                )

            ],
                
                style = {
                    # 'borderStyle' : 'dashed',
                    'background-color' : '#e1e1ea',
                    'height' : '450px',
                    # 'left' : '100px'
                },
                className = 'three columns'
            ),

            # the frequence domain file
            dcc.Graph(id='fig1',figure={}, className = 'nine columns')],
            className = 'row'
        ),

    
        # {'data' : ...., 'layout' : .....}
        html.Div(children = [
                # html.Div(children = dcc.Graph(figure=fig, className = 'four columns')), 
            dcc.Graph(id='fig2',figure={}, className = 'six columns'),
            dcc.Graph(id='fig3',figure={}, className = 'six columns')],
            className = 'row',
        ),

        html.Div(children = [
                    # html.Div(
            dcc.Dropdown(
                id = 'funcSelect',
                options = [
                    {'label':'Time Domain', 'value':0},
                    {'label':'Frequence Domain', 'value':1},
                    {'label':'Evenlope', 'value':2}
                ],
                multi = False,
                value = 0,
                style = {
                    'text-align' : 'center',
                    'position' : 'relative',
                    'top' : '40px',
                    # 'background-color' : '#FFD382',
                },
                persistence=True
        
            )],
            className = 'row',
        )]
    )

page2 =\
    html.Div(id = 'page2', children = [
        
    html.Div(children = [
        html.Div(children = [
            dcc.Dropdown(
                options=[
                    {'label': '500 RPM', 'value': '500'},
                    {'label': '1000 RPM', 'value': '1000'},
                    {'label': '2000 RPM', 'value': '2000'}
                ],
                value='500',
                style = {
                    'position' : 'relative',
                    'top' : '20px',
                    'left' : '20px',
                    'width' : '250px',
                    'height' : '60px',
                    'textAlign': 'center',
                    # 'background-color' : '#ffffff',
                }
            ),  

            html.Button('Classifly', id='button', 
                style = {
                    'position' : 'relative',
                    'top' : '250px',
                    'left' : '150px',
                    'background-color' : 'white',
                    'height' : '80px'
                    }
            )],

                
            style = {
                # 'borderStyle' : 'dashed',
                    'background-color' : '#e1e1ea',
                    'height' : '450px',
                    # 'left' : '100px'
                },
                className = 'three columns'
        ),
        # not fit layout
        # html.Div('',style = {
        #     'weight' : '10px',
        #     'height' : '600px',
        #     'background-color' : '#e6f3ff'
        # })
        ],
        # dcc.Graph(id='fig1',figure={}, className = 'nine columns')],

        className = 'row'
    )
])



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
    html.Div(id='pages_content', children = page1)

])




from dash.dependencies import Output, Input, State
@app.callback(
    # the instant name and instant value
    [
        Output(component_id = 'fig1', component_property = 'figure'),
        Output(component_id = 'fig2', component_property = 'figure'),
        Output(component_id = 'fig3', component_property = 'figure'),
        Output(component_id = 'fileinfo', component_property = 'children')],
    [Input(component_id = 'funcSelect', component_property = 'value'), Input('bearing_file_upload', 'contents')],
    [State('bearing_file_upload', 'filename'), State('bearing_file_upload', 'last_modified')])
def upload_file(opt, contents, filename, filedates):
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
        return page1
    elif tab == 'tab-2':
        return page2

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

