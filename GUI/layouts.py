import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

from GUI.bearingData import bearingFileInfo

class Layout:
    def __init__(self):
        self.mainPage = html.Div(id = 'mainPage')
        self.tabOne = html.Div(id = 'tabOne')
        self.tabTwo = html.Div(id = 'tabTwo')
        self.dateOpt = []
        self.timeOpt = []
    def setMainPage(self):
        #fileinfo_mem = dcc.Store(iid = 'memory-output')
        #tab_change = html.Div(id = 'tab_change', children = 'foo', style = {'display' : 'none'})
        self.mainPage = html.Div( children = [
            html.Div(html.H1(children='Bearing Fault Dashboard'), className = 'row'),

            #tab_change,
            dcc.Tabs(id="tabs", value='tab1', children=[
                dcc.Tab(label = 'Load Data and Draw', value = 'tab1'),
                dcc.Tab(label = 'Classification', value = 'tab2'),
            ]),
            html.Div(id='pages_content', children = self.tabOne),
            dcc.Store(id = 'dataMem'),
            dcc.Store(id = 'fileinfoMem')
            #fileinfo_mem # A space to store something
        ] )
    def setTabOne(self):
        self.dateOpt,_ = bearingFileInfo()
        loadfileDiv = html.Div(children = [
            dcc.Dropdown(
                id = 'dateSelect',
                options = self.dateOpt,
                value=None,
                persistence=True,
                placeholder = 'Select File Date',
                style={
                    'position' : 'relative',
                    'top' : '10px',
                    #'font-size': '30px',
                    'text-align' : 'center'
                }
            ),

            dcc.Dropdown(
                id = 'timeSelect',
                options=self.timeOpt,
                value=None,
                persistence=True,
                disabled = True,
                placeholder = 'Select File Time',
                style={
                    'position' : 'relative',
                    'top' : '10px',
                    #'font-size': '30px',
                    'text-align' : 'center'
                }
            ),
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
            html.Button(
                'Load',
                id='load_btn',
                style = {
                    'position' : 'relative',
                    'top' : '80px',
                    'left' : '100px',
                    'background-color' : 'white',
                    'height' : '80px'
                }
            ),
        ],
            style = {
                # 'borderStyle' : 'dashed',
                'background-color' : '#e1e1ea',
                'height' : '450px',
                # 'left' : '100px'
            },
            className = 'three columns'
        )

        self.tabOne = html.Div(id = 'tabOne', children = [
            html.Div(children = [
                loadfileDiv,
                # the frequence domain file
                dcc.Graph(id='tmPlot',figure={}, className = 'nine columns')],
                className = 'row'
            ),

            html.Div(children = [
                dcc.Graph(id='freqPlot',figure={}),
                dcc.Graph(id='pwrPlot',figure={}),
                dcc.Graph(id='autoCorrPlot',figure={})],
                className = 'row',
            )
        ])
    def setTabTwo(self):
        self.tabTwo = html.Div(id = 'tabTwo', children = [
            html.Div(children = [
                dcc.Textarea(
                    id='selFileinfo',
                    value='Please select the file first',
                    disabled = True,
                    style={
                        'width': '100%',
                        'height': 200,
                        'position' : 'relative',
                        'top' : '60px',
                        'background-color' : '#f0f0f5'
                        # 'font-family' : 'Courier New'
                    },
                    persistence = True
                ),
                html.Button(
                    'Classify', 
                    id='classify_btn',
                    style = {
                        'position' : 'relative',
                        'top' : '110px',
                        'left' : '100px',
                        'background-color' : 'white',
                        'height' : '80px'
                    }
                )],
                style = {
                    'background-color' : '#e1e1ea',
                    'height' : '450px',
                },
                className = 'three columns'),
            html.Div( children = [
                html.Div(
                    id='faultTypeTxt',
                    children = 'Bearing Fault Type',
                    style = {
                        'font-size': '26px',
                        #'text-align': 'center'
                    }
                ),
                html.Img(
                    id='bearing_img',
                    src='',
                    style = {
                        'height' : '300px',
                        'width' : '300px',
                        #'position' : 'relative',
                        #'left' : '50px',
                        #'top' : '120px'
                    })
                ],
                style = {
                    'position': 'relative',
                    'top': '80px'
                },
                className = 'four columns'),
            html.Div( children = [
                html.Div(
                    children = ''
                ),
                html.Img(
                    id='confusMatrix',
                    src='/home/thl/Documents/Main/GUI/assets/Normal.png',
                    style = {
                        'height' : '500px',
                        'width' : '500px',
                        'position' : 'relative',
                        #'left' : '150px',
                        'top' : '20px'
                    })
                ],
                className = 'five columns')
        ],
            className = 'row')

