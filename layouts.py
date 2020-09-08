import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html

from datetime import datetime as dt

import callbacks

# fileinfo =  dcc.Textarea(
#     id='fileinfo',
#     value='Textarea content initialized\nwith multiple lines of text',
    
#     disabled = True,
#     style={
#         'width': '100%',
#         'height': 200,
#         'position' : 'relative',
#         'top' : '60px',
#         'background-color' : '#f0f0f5'
#     },
#     persistence = True
# )

fileinfo_mem = dcc.Store(id = 'memory-output')
tab_change = html.Div(id = 'tab_change', children = 'foo', style = {'display' : 'none'})

loadfile_div = \
    html.Div(children = [
######### Enable dateselect when database is done
        # dcc.DatePickerSingle(
        #     id='date-picker-single',
        #     date=dt(2020, 9, 1),
        #     style = {
        #         'font-family' : 'Courier New'
        #     }
        # ),
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
        # html.Div(id = 'fileinfo', children = [
        #     dcc.Markdown('''
        #         #### Dash and Markdown

        #         Dash supports [Markdown](http://commonmark.org/help).

        #         Markdown is a simple way to write and format text.
        #         It includes a syntax for things like **bold text** and *italics*,
        #         [links](http://commonmark.org/help), inline `code` snippets, lists,
        #         quotes, and more.
        #     ''')],
        #     style = {
        #         'position' : 'relative',
        #         'top' : '60px',
        #         'background-color' : '#f0f0f5',
        #         'width' : '280px',
        #         'height' : '200px',
        #         'left' : '15px',
        #         # 'font-family' : 'Courier New'
        #         # 'text-align' : 'center'
        #     }
        # ),
        dcc.Textarea(
            id='fileinfo',
            value='',
            
            disabled = True,
            style={
                'width': '100%',
                'height': 200,
                'position' : 'relative',
                'top' : '60px',
                'background-color' : '#f0f0f5'
            },
            persistence = True
        ),

        html.Button('Load', 
            id='load_btn', 
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
            persistence = True,
            style = {
                'position' : 'relative',
                'top' : '0px',
                'right' : '50px',
                # 'font-family' : 'Courier New'
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
    )

page1_div =\
    html.Div(id = 'page1', children = [
        html.Div(children = [ 
            loadfile_div,

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
        )]
    )


page2_div =\
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

            # html.Div(id = 'fileinfo_page2', children = [],
            #     style = {
            #         'position' : 'relative',
            #         'top' : '60px',
            #         'background-color' : '#f0f0f5',
            #         'width' : '280px',
            #         'height' : '200px',
            #         'left' : '15px',
            #         # 'font-family' : 'Courier New'
            #         # 'text-align' : 'center'
            #     }
            # ),
            dcc.Textarea(
                id='fileinfo',
                value='Textarea content initialized\nwith multiple lines of text',
                
                disabled = True,
                style={
                    'width': '100%',
                    'height': 200,
                    'position' : 'relative',
                    'top' : '60px',
                    'background-color' : '#f0f0f5'
                },
                persistence = True
            ),


            html.Button('Classify', id='button', 
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
        # foo
        dcc.Upload(
            id = 'bearing_file_upload',
            style = {'display' : 'none'}
        )
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

# intermediate_div = html.Div(id = 'intermediate', style = {'display' : 'none'})