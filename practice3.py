import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css','https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


mainfile = np.load('/Users/nicole/Downloads/Formal/Cage_Break.npy').reshape(-1)
fig1 = px.line(mainfile, title = 'Frequency Domain')
fig2 = px.line(mainfile, title = 'Envolope')
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

page1 =\
    html.Div(id = 'page1', children = [
        html.Div(children = [
            html.Div(children = [
                dcc.Upload(
                    id = 'D25file',
                    children = html.Div( ['Drag and Drop or ', html.A('Select Files')], style =  {'position' : 'relative','top':'14px'} ),
                    multiple = True,
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
                html.Div(children = [html.Li('Filename : ball.npy'), html.Li('Data Size : 1.6 MB'), html.Li('Date : July 30, 2020 at 10:37 PM')],
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
                dcc.RadioItems(
                    options=[
                        {'label': 'No Filter', 'value': '0'},
                        {'label': 'With Filter', 'value': '1'}
                    ],
                    value='0',
                    labelStyle={'display': 'inline-block'},
                    style = {
                        'position' : 'relative',
                        'top' : '30px',
                        'left' : '10px'
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

                
            dcc.Graph(id='fig1',figure={}, className = 'nine columns')],
            className = 'row'
        ),

    
        # {'data' : ...., 'layout' : .....}
        html.Div(children = [
                # html.Div(children = dcc.Graph(figure=fig, className = 'four columns')), 
            dcc.Graph(id='fig2',figure=fig1, className = 'six columns'),
            dcc.Graph(id='fig3',figure=fig2, className = 'six columns')],
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
                }
        
            )],
            className = 'row',
        )
    ])

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

    # 這裡的style是internel css style
    # <h1 style="text-align:center;color:red">......</h1> 的概念
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
    [Output(component_id = 'fig1', component_property = 'figure')],
    [Input(component_id = 'funcSelect', component_property = 'value')]
)
def drawGraph(opt):
    data = mainfile.copy()
    # time domain
    if opt == 0:
        # data = data[:4096]
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
    # print(data)

    # 要加逗號, 需要是tuple型態
    return fig,

@app.callback(Output('pages_content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return page1
    elif tab == 'tab-2':
        return page2



if __name__ == '__main__':
    app.run_server(debug=True)