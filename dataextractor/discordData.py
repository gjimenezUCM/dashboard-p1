import requests
import json
import pandas as pd
import time

# Ayuda para la implementación: 
# https://github.com/b1naryth1ef/disco/blob/master/disco/api/http.py
# https://discordapp.com/developers/docs/reference

## TODO: Llevar todo esto a fichero de configuración
## Configurar Token de Discord y el Id del servidor
TOKEN = ""
SERVER_ID = ""
BASE = "https://discordapp.com/api/v7"

CHANNELS_GET = "/guilds/{}/channels"
MESSAGES_GET = "/channels/{}/messages"
MEMBERS_GET = "/guilds/{}/members"
QP_LIMIT="limit={}"
QP_NEXT="before={}"
MAX_LIMIT = 100
header = dict(authorization=TOKEN)


def collectChannelInfo():
    url = BASE+CHANNELS_GET.format(SERVER_ID)
    reqChannels = requests.get(url,headers=header)
    resp = reqChannels.json()
    channelInfo = {}
    for channel in resp:
        if channel['parent_id'] != None:
            channelInfo[channel['id']] = channel['name']
    return channelInfo

def collectUserInfo():
    url = BASE+MEMBERS_GET.format(SERVER_ID)+"?limit=100"
    reqUsers = requests.get(url,headers=header)
    users = reqUsers.json()
    userDict = {}
    for user in users:
        nickname = user['nick']
        if user['nick']==None:
            nickname = user['user']['username']
        userDict[user['user']['id']] = nickname
    return userDict

def requestMessages(channelId, last=0):
    url = BASE+MESSAGES_GET.format(channelId)+"?"
    url += QP_LIMIT.format(MAX_LIMIT)
    if last!=0:
        url += "&"+QP_NEXT.format(last)
    reqMsgs = requests.get(url,headers=header)
    respMsgs = json.loads(reqMsgs.text)
    return respMsgs

def CollectAllMessages(channelId, channelName, userDict):
    msgCol = []
    iterate = True
    last = 0

    while iterate:
        respMsgs = requestMessages(channelId, last)
        for msg in respMsgs:
            nickname = userDict[msg['author']['id']]
            if nickname == None:
                nickname=msg['author']['username']
            msgInfo = dict(channelId=channelId,
                           channelName=channelName,
                           ts=msg['timestamp'],
                           authorid=msg['author']['id'],
                           authorname=nickname, 
                           contentLength=len(msg['content']))
            msgCol.append(msgInfo)
        if len(respMsgs)< MAX_LIMIT:
            iterate = False
        else:
            last = respMsgs[-1]['id']
   
    return msgCol


def main():

    channelInfo = collectChannelInfo()
    userDict = collectUserInfo()
    # Extracción de mensajes
    allMessages = []
    for channelId, channelName in channelInfo.items():
        print("Collecting from channel",channelName)
        channelMsgs = CollectAllMessages(channelId,channelName, userDict)
        allMessages.extend(channelMsgs)

    # Limpieza y transformación
    df = pd.DataFrame(allMessages)  
        
    # Guardado a disco
    df.to_csv("../web/data/discord2.csv", index = False)

if __name__ == "__main__":
    main()