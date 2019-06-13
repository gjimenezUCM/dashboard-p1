import requests
from datetime import datetime
import pandas as pd

## TODO: Llevar todo esto a fichero de configuración

## Necesario un token de Github para extraer la información
token = ''

#
# PONER AQUÍ LA LISTA DE REPOSITORIOS
#
repoList =[""]


rootApi = 'https://api.github.com'
MAX_PER_PAGE = "per_page=100"
headers = {'Authorization': 'token ' + token}

## Creación de un diccionario con todas las ramas que hay en un repositorio
def createBranchesDict(user, repo):
    urlAPIBranches = rootApi + "/repos/{}/{}/branches?".format(user,repo,MAX_PER_PAGE)    
    branchesDict = {}
    while True:
        req = requests.get(urlAPIBranches, headers = headers)
        respBranches = req.json()
        for b in respBranches:
            branchesDict[b['commit']['sha']] = b['name']
        if "next" in req.links:
            urlAPIBranches = req.links["next"]['url']
            print(urlAPIBranches)
        else:
            break

    return branchesDict

## Extracción de los commits de todas las ramas de un repositorio
def commitsFromBranches(user, repo, branchesDict):
    commits = []

    for sha,branchName in branchesDict.items():
        urlAPICommits = rootApi+"/repos/{}/{}/commits?per_page=100&sha={}".format(user,repo,sha)
        print("   Branch:",branchName)
        while True:
            req = requests.get(urlAPICommits, headers = headers)
            if req.status_code == 403:
                print(req.status_code, req.reason)
                break
            respCommits = req.json()
            for commitInfo in respCommits:
                thisCommit = { "repo": repo, "branch":branchName } 
                thisCommit['author'] = commitInfo['commit']['committer']['name']
                thisCommit['email'] = commitInfo['commit']['committer']['email']
                thisCommit['date'] = commitInfo['commit']['committer']['date']
                if commitInfo["author"] is None:
                    thisCommit['login'] = ""
                else:
                    thisCommit['login'] = commitInfo['author']['login']  
                strMessage = commitInfo['commit']['message']
                strMessage = strMessage.replace("\r\n", ".")
                thisCommit['message'] = strMessage.replace("\n", ".")
                thisCommit['url'] = commitInfo['html_url']
                commits.append(thisCommit)
            if "next" in req.links:
                urlAPICommits = req.links["next"]['url']
            else:
                break

    return commits

def main():
    commits = []
    # Extracción de commits
    for i in range(len(repoList)):

        splitUrl = repoList[i].split('/') # pos 3 y 4
        user = splitUrl[3]
        repo = splitUrl[4]
        
        print(user,repo)
        branchesDict = createBranchesDict(user, repo)
        commitsFromRepo = commitsFromBranches(user, repo, branchesDict)
        commits.extend(commitsFromRepo)

    # Carga del dataframe para transformación y limpieza
    df = pd.DataFrame(commits)
    df.date = pd.to_datetime(df.date)
    df.login = df.apply(lambda row: row.author if row.login == "" else row.login, axis=1)

    ## Limpieza de Logins duplicados detectados

    ## Ejemplo
    ## df.login.replace("Sebaaaaas", "Sebas", inplace=True)


    ## Eliminar usuarios desconocidos

    ## Ejemplo
    ## unknowkUsers = df[df["login"].isin(["albcor01", "unknown"])]
    ## df.drop(unknowkUsers.index, axis=0, inplace=True)

    # Limpieza de comillas dobles y saltos de línea en comentarios
    df.message = df.message.apply(lambda x: x.replace('""',''))
    df.message = df.message.apply(lambda x: x.replace('\r\n',''))
    df.message = df.message.apply(lambda x: x.replace('\n',''))

    # Guardado a disco
    df.to_csv("../web/data/commits.csv", index=False)

if __name__ == "__main__":
    main()