import pandas as pd 
import plotly.graph_objs as go

class Repo:
    def __init__(self, name, dfCommits):
        self.name = name
        self.commitsRepo = dfCommits[dfCommits.repo==name]
        self.nCommits = len(self.commitsRepo)
        self.nBranches = len(self.commitsRepo.branch.unique())
        self.createByAuthorDistribution()
        self.createCommitsByDay()


    def createByAuthorDistribution(self):
        byAuthor = self.commitsRepo.groupby(by=["login"]).count()
        byAuthor.sort_values(by="author", ascending=False,inplace=True)
        byAuthor.drop(byAuthor.columns[1:], axis=1, inplace=True)
        byAuthor.columns = ["numCommits"]
        self.authors = list(byAuthor.index.values)
        data = []
        
        for author in self.authors:
            trace = go.Bar(
                x = [self.name],
                y = [byAuthor.loc[author,"numCommits"]],# Número de commits
                name = author,
                hoverinfo = "text+y",
                text = "{}: {} commits".format(author,byAuthor.loc[author,"numCommits"]),
                width = 0.5,
                visible = True
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
        self.figAuthorDistribution = go.Figure(data=data, layout=layout)   

    def createCommitsByDay(self):
        data = []
        for author in self.authors:
            byDay = self.commitsRepo[self.commitsRepo.login==author].resample('D').count()

            trace1 = go.Bar(
                x = byDay.index,
                y = byDay.author,
                name=author,
                visible = True
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
        self.figCommitsByDay =  go.Figure(data=data, layout=layout)
    def selectAll(self):
        for trace in self.figCommitsByDay.data:
            trace.visible = True

    def selectAuthor (self,authorName):
        for trace in self.figCommitsByDay.data:
            trace.visible = False
        authorIndex = self.authors.index(authorName)
        self.figCommitsByDay.data[authorIndex].visible = True
