import pandas as pd 
import plotly.graph_objs as go
from repo import Repo

COMMITS_FILENAME = 'data/commits.csv'

dfCommits = pd.read_csv(COMMITS_FILENAME)
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