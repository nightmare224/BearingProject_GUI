from GUI.gui import GUI
from GUI import callbacks
from GUI.app import app

from dash.dependencies import Output, Input, State


## create the GUI
gui = GUI()


## ugly part..., for rendering the tab content,
## because there is no other part can get layout instant, 
## so put this callback func here###
@app.callback(
    [Output('pages_content', 'children')],
    [Input('tabs', 'value')]
)
def renderContent(tab):
    if tab == 'tab1':
        return gui.layout.tabOne,
    else:
        return gui.layout.tabTwo,


if __name__ == '__main__':
    gui.app.run_server(host = '0.0.0.0', debug = False)




