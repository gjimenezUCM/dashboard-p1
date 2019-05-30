import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
from model import CommitModel,DiscordModel

external_stylesheets = ['/assets/style.css']
server = Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                server=server)

selectedRepo = "Proyecto1G06"
githubModel = CommitModel()

commitPanel = [
    html.Div([ 
        html.H2(children='Commits en Github'),
        html.Div([ 
            dcc.Dropdown(
                id='dropdown-repo',
                options=githubModel.repoOptions(),
                value = selectedRepo
            ),
            dcc.Dropdown(
                id='dropdown-author',
                options=githubModel.authorOptions(selectedRepo),
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
        ],className="eight columns"),

        html.Div([ 
            html.Div([ 
                    dcc.Graph(
                        id='repo_overall'
                    )
                ],className="five columns"
            ),
            html.Div([ 
                    dcc.Graph(
                        id='repo_time'
                    ),
                ],className="seven columns")
        ],className="twelve columns")
    ],className="twelve columns")
    ]

discordModel = DiscordModel()
selectedChannel = "grupo06"
MsgPanel = [
    html.Div([ 
        html.H2(children='Mensajes en Discord'),
        html.Div([ 
            dcc.Dropdown(
                id='dropdown-discord',
                options=discordModel.channelOptions(),
                value = selectedChannel
            ),
            dcc.Dropdown(
                id='dropdown-authordiscord',
                options=discordModel.authorOptions(selectedChannel),
                value = "Todos"
            ),
        ],className="four columns"),
        html.Div([ 
            html.Div(
                id='div-nmsgs'
            ),
        ],className="four columns"),

        html.Div([ 
            html.Div([ 
                    dcc.Graph(
                        id='discordgroup_overall'
                    )
                ],className="five columns"
            ),
            html.Div([ 
                    dcc.Graph(
                        id='discordgroup_time'
                    ),
                ],className="seven columns")
        ],className="twelve columns")
    ],className="twelve columns")
    ]

layoutChildren  = [
    html.H1(children='Proyectos 1')
]
layoutChildren.extend(commitPanel)
layoutChildren.extend(MsgPanel)
app.layout = html.Div(children=layoutChildren)


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
        githubModel.selectAll(repo_input_value)
    else:
        if author_input_value == "Todos":
            githubModel.selectAll(repo_input_value)
        else:
            githubModel.selectAuthor(repo_input_value,author_input_value)
    sNcommits = "Número de commits: {}".format(githubModel.nCommits(repo_input_value))
    sNbranches = "Número de ramas: {}".format(githubModel.nBranches(repo_input_value))
    return githubModel.figAuthorDistribution(repo_input_value),githubModel.commitsByDay(repo_input_value), githubModel.authorOptions(repo_input_value),sNcommits,sNbranches

@app.callback(
    [Output(component_id='discordgroup_overall', component_property='figure'),
     Output(component_id='discordgroup_time', component_property='figure'),
     Output(component_id='dropdown-authordiscord', component_property='options'),
     Output(component_id='div-nmsgs', component_property='children')],
    [Input('dropdown-discord', 'value'),
    Input('dropdown-authordiscord', 'value')]
)
def update_ChannelName(channel_input_value, author_input_value):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if input_id == 'dropdown-discord':
        discordModel.selectAll(channel_input_value)
    else:
        if author_input_value == "Todos":
            discordModel.selectAll(channel_input_value)
        else:
            discordModel.selectAuthor(channel_input_value,author_input_value)
    sNmsgs = "Número de mensajes: {}".format(discordModel.nMsgs(channel_input_value))
    return discordModel.figAuthorDistribution(channel_input_value),discordModel.msgsByDay(channel_input_value), discordModel.authorOptions(channel_input_value),sNmsgs




if __name__ == '__main__':
    app.run_server(dev_tools_ui=True)