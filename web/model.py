import pandas as pd 
import plotly.graph_objs as go
from repo import Repo
from discord import Discord

COMMITS_FILENAME = 'data/commits.csv'
DISCORD_FILENAME = 'data/discord.csv'

class CommitModel:
    def __init__(self):
        self.dfCommits = pd.read_csv(COMMITS_FILENAME)
        self.dfCommits.date = pd.to_datetime(self.dfCommits.date)
        self.dfCommits.set_index("date", inplace=True)

        byRepo = self.dfCommits.groupby(by=["repo"]).count()
        byRepo.sort_values(by="author", ascending=False)

        self.repos = byRepo.index.values

        self.repoFigures = {}
        for repoName in self.repos:
            self.repoFigures[repoName] = Repo(repoName, self.dfCommits)


    def repoOptions(self):
        return [{'label': repo, 'value': repo} for repo in self.repos]


    def authorOptions(self,repoName):
        repoInfo = self.repoFigures[repoName]
        options = [{'label': author, 'value': author} for author in repoInfo.authors]
        options.append({'label': 'Todos', 'value': 'Todos'})
        return options

    def figAuthorDistribution(self,repoName):
        return self.repoFigures[repoName].figAuthorDistribution

    def commitsByDay(self,repoName):
        return self.repoFigures[repoName].figCommitsByDay

    def selectAll(self,repoName):
        self.repoFigures[repoName].selectAll()

    def selectAuthor(self,repoName,authorName):
        self.repoFigures[repoName].selectAuthor(authorName)

    def nCommits(self,repoName):
        return self.repoFigures[repoName].nCommits   

    def nBranches(self,repoName):
        return self.repoFigures[repoName].nBranches 


class DiscordModel:
    def __init__(self):
        self.dfMsgs = pd.read_csv(DISCORD_FILENAME)
        self.dfMsgs["date"] = pd.to_datetime(self.dfMsgs.ts)
        self.dfMsgs.set_index("date", inplace=True)

        byChannel = self.dfMsgs.groupby(by=["channelName"]).count()
        byChannel.sort_values(by="authorname", ascending=False)

        self.channels = byChannel.index.values

        self.channelFigures = {}
        for channelName in self.channels:
            self.channelFigures[channelName] = Discord(channelName, self.dfMsgs)


    def channelOptions(self):
        return [{'label': repo, 'value': repo} for repo in self.channels]


    def authorOptions(self,channelName):
        repoInfo = self.channelFigures[channelName]
        options = [{'label': author, 'value': author} for author in repoInfo.authors]
        options.append({'label': 'Todos', 'value': 'Todos'})
        return options

    def figAuthorDistribution(self,channelName):
        return self.channelFigures[channelName].figAuthorDistribution

    def msgsByDay(self,channelName):
        return self.channelFigures[channelName].figMsgsByDay

    def selectAll(self,channelName):
        self.channelFigures[channelName].selectAll()

    def selectAuthor(self,channelName,authorName):
        self.channelFigures[channelName].selectAuthor(authorName)

    def nMsgs(self,channelName):
        return self.channelFigures[channelName].nMsgs  
