import pandas as pd 
import plotly.graph_objs as go
from repo import Repo

dfCommits = pd.read_csv("data/commits_P1_20190520.csv")
dfCommits.date = pd.to_datetime(dfCommits.date)
dfCommits.set_index("date", inplace=True)

byRepo = dfCommits.groupby(by=["repo"]).count()
byRepo.sort_values(by="author", ascending=False)

"""
byAuthor = dfCommits.groupby(by=["repo","login"]).count()
byAuthor.reset_index(inplace=True)
byAuthor.drop(byAuthor.columns[4:], axis=1, inplace=True)
byAuthor.columns = ["repo", "author", "numCommits", "Ratio in repo"]
byAuthor["Ratio in repo"] = byAuthor.apply(lambda row: row.numCommits/ byRepo.loc[row.repo], axis=1)
byAuthor.sort_values(by="Ratio in repo", ascending=False)
"""
repos = byRepo.index.values

repoFigures = {}
for repoName in repos:
    repoFigures[repoName] = Repo(repoName, dfCommits)

print("loaded")

def repoOptions():
    return [{'label': repo, 'value': repo} for repo in repos]


def authorOptions(repoName):
    repoInfo = repoFigures[repoName]
    options = [{'label': author, 'value': author} for author in repoInfo.authors]
    options.append({'label': 'Todos', 'value': 'Todos'})
    return options

def figAuthorDistribution(repoName):
    return repoFigures[repoName].figAuthorDistribution

def commitsByDay(repoName):
    return repoFigures[repoName].figCommitsByDay

def selectAll(repoName):
    repoFigures[repoName].selectAll()

def selectAuthor(repoName,authorName):
    repoFigures[repoName].selectAuthor(authorName)

def nCommits(repoName):
    return repoFigures[repoName].nCommits   

def nBranches(repoName):
    return repoFigures[repoName].nBranches 
"""
def commitsByDay(repoName):
    data = []
    commitsRepo = dfCommits[dfCommits.repo==repoName]
    for author in commitsRepo.login.unique():
        byDay = commitsRepo[commitsRepo.login==author].resample('D').count()

        trace1 = go.Bar(
            x = byDay.index,
            y = byDay.author,
            name=author
        )
        data.append(trace1)

    layout = dict(
                title='Distribución de commits por días',
                barmode='stack',
                annotations = [
                dict(
                    text= "Hito 1",
                    xref = "x",
                    yref = "y",
                    x = pd.to_datetime('2019/3/13'),
                    y = 0,
                    xanchor = "center",
                    yanchor = "top",
                    ax = 0,
                    ay = 10,
                    bgcolor = "lightblue",
                ),
                dict(
                    text= "Guerrilla",
                    xref = "x",
                    yref = "y",
                    x = pd.to_datetime('2019/4/26'),
                    y = 0,
                    xanchor = "center",
                    yanchor = "top",
                    ax = 0,
                    ay = 10,
                    bgcolor = "lightblue",
                ),
                dict(
                    text= "Hito 2",
                    xref = "x",
                    yref = "y",
                    x = pd.to_datetime('2019/4/10'),
                    y = 0,
                    xanchor = "center",
                    yanchor = "top",
                    ax = 0,
                    ay = 10,
                    bgcolor = "lightblue",
                ),
                dict(
                    text= "Hito 3",
                    xref = "x",
                    yref = "y",
                    x = pd.to_datetime('2019/5/17'),
                    y = 0,
                    xanchor = "center",
                    yanchor = "top",
                    ax = 0,
                    ay = 10,
                    bgcolor = "lightblue",
                )
            ]
            )
    return go.Figure(data=data, layout=layout)

def figAuthorsByRepo(repoName, df=byAuthor):
    byRepoAuthor = df[df.repo == repoName]

    data = []
    byRepoAuthor.sort_values(by=["numCommits"], ascending=False, inplace=True)

    for author in byRepoAuthor.author.unique():
        trace = go.Bar(
            x = byRepoAuthor.repo,
            y = byRepoAuthor[byRepoAuthor.author==author].numCommits,
            name = author,
            hoverinfo = "text+y",
            text = "{}: {} commits".format(author,byRepoAuthor[byRepoAuthor.author==author].numCommits.values[0]),
            width = 0.5
        )
        data.append(trace)

    layout = dict(
                title='Porcentaje de commits de cada usuario del repositorio',
                # Indicamos que dibujaremos un gráfico de barras apiladas.
                barmode='stack',
                barnorm="percent",
                yaxis = dict(
                    title="Porcentaje de commits",
                    ticksuffix="%"
                ),
                hovermode = "closest",
                hoverdistance = 10,

             )
    fig = go.Figure(data=data, layout=layout)
    return fig
"""