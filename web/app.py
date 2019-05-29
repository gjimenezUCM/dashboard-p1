import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
import model

external_stylesheets = ['/assets/style.css']
server = Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                server=server)

selectedRepo = "Proyecto1G06"

app.layout = html.Div(children=[
    html.H1(children='Proyectos 1'),
    html.Div([ 
        dcc.Dropdown(
            id='dropdown-repo',
            options=model.repoOptions(),
            value = selectedRepo
        ),
        dcc.Dropdown(
            id='dropdown-author',
            options=model.authorOptions(selectedRepo),
            value = "Todos"
        ),
    ],className="four columns"),
    html.Div([ 
        html.Div(
            id='div-ncommits'
        ),
        html.Div(
            id='div-nbranches'
        ),
    ],className="four columns"),

    html.Div([ 
        html.Div([ 
                dcc.Graph(
                    id='repo_overall'
                )
            ],className="four columns"
        ),
        html.Div([ 
                dcc.Graph(
                    id='repo_time'
                ),
            ],className="eight columns")
    ],className="twelve columns")
])

@app.callback(
    [Output(component_id='repo_overall', component_property='figure'),
     Output(component_id='repo_time', component_property='figure'),
     Output(component_id='dropdown-author', component_property='options'),
     Output(component_id='div-ncommits', component_property='children'),
     Output(component_id='div-nbranches', component_property='children'),],
    [Input('dropdown-repo', 'value'),
    Input('dropdown-author', 'value')]
)
def update_RepoName(repo_input_value, author_input_value):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if input_id == 'dropdown-repo':
        model.selectAll(repo_input_value)
    else:
        if author_input_value == "Todos":
            model.selectAll(repo_input_value)
        else:
            model.selectAuthor(repo_input_value,author_input_value)
    sNcommits = "Número de commits: {}".format(model.nCommits(repo_input_value))
    sNbranches = "Número de ramas: {}".format(model.nBranches(repo_input_value))
    return model.figAuthorDistribution(repo_input_value),model.commitsByDay(repo_input_value), model.authorOptions(repo_input_value),sNcommits,sNbranches
"""
@app.callback(
    Output(component_id='repo_time', component_property='figure'),
    [Input('dropdown-author', 'value')]
)
def update_FigAuthor(input_value):
    model.selectAuthor(selectedRepo,input_value)
    return model.commitsByDay(selectedRepo)
"""



if __name__ == '__main__':
    app.run_server(dev_tools_ui=True)