import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html


import callbacks



loadfile_div = \
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