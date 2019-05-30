import pandas as pd 
import plotly.graph_objs as go

class Discord:
    def __init__(self, name, dfDiscord):
        self.name = name
        self.msgsChannel = dfDiscord[dfDiscord.channelName==name]
        self.nMsgs = len(self.msgsChannel)
        self.createByAuthorDistribution()
        self.createMsgsByDay()


    def createByAuthorDistribution(self):
        byAuthor = self.msgsChannel.groupby(by=["authorname"]).count()
        byAuthor.drop(byAuthor.columns[1:], axis=1, inplace=True)
        byAuthor.columns = ["numMsgs"]
        byAuthor.sort_values(by="numMsgs", ascending=False,inplace=True)
        self.authors = list(byAuthor.index.values)
        data = []
        
        for author in self.authors:
            trace = go.Bar(
                x = [self.name],
                y = [byAuthor.loc[author,"numMsgs"]],# Número de numMsgs
                name = author,
                hoverinfo = "text+y",
                text = "{}: {} Mensajes".format(author,byAuthor.loc[author,"numMsgs"]),
                width = 0.5,
                visible = True
            )
            data.append(trace)

        layout = dict(
                    title='Porcentaje de mensajes de cada miembro',
                    # Indicamos que dibujaremos un gráfico de barras apiladas.
                    barmode='stack',
                    barnorm="percent",
                    yaxis = dict(
                        title="Porcentaje de mensajes",
                        ticksuffix="%"
                    ),
                    hovermode = "closest",
                    hoverdistance = 10,

                )
        self.figAuthorDistribution = go.Figure(data=data, layout=layout)   

    def createMsgsByDay(self):
        data = []
        for author in self.authors:
            byDay = self.msgsChannel[self.msgsChannel.authorname==author].resample('D').count()

            trace1 = go.Bar(
                x = byDay.index,
                y = byDay.authorname,
                name=author,
                visible = True
            )
            data.append(trace1)

        layout = dict(
                title='Distribución de mensajes por días',
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
        self.figMsgsByDay =  go.Figure(data=data, layout=layout)
    def selectAll(self):
        for trace in self.figMsgsByDay.data:
            trace.visible = True

    def selectAuthor (self,authorName):
        for trace in self.figMsgsByDay.data:
            trace.visible = False
        authorIndex = self.authors.index(authorName)
        self.figMsgsByDay.data[authorIndex].visible = True
