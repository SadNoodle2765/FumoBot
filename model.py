import requests
import json
from collections import Counter

BASE_URL_FUMO = 'https://fumo-search.herokuapp.com/api/fumo/?fumoName='
BASE_URL_SAVED_FUMOS = 'https://fumo-search.herokuapp.com/api/savedfumos/'
BASE_URL_VOTE_FUMO = 'https://fumo-search.herokuapp.com/api/vote/'

def getFumos(fumoName=''):
    response = requests.get(BASE_URL_FUMO + fumoName)
    data = json.loads(response.text)

    data.sort(key=lambda fumo: fumo['buyoutPrice'] if fumo['buyoutPrice'] != 0 else fumo['price'])

    return data

def toggleSaveFumo(userName, buyLink, add) -> bool:
    response = requests.get(BASE_URL_SAVED_FUMOS+ '?userName=' + userName)
    data = json.loads(response.text)

    body = {'userName': userName, 'link': buyLink}

    if add:
        requests.post(BASE_URL_SAVED_FUMOS, json=body)
        return True

    else:
        requests.delete(BASE_URL_SAVED_FUMOS, json=body)
        return False

def voteForFumo(userName, fumo):
    body = {'userName': userName, 'fumo': fumo}
    requests.post(BASE_URL_VOTE_FUMO, json=body)

def getVotes():
    response = requests.get(BASE_URL_VOTE_FUMO)
    data = json.loads(response.text)

    voteCount = Counter(vote['fumo'] for vote in data)
    voteCount = sorted([(fumo, voteNum) for fumo, voteNum in voteCount.items()], key=lambda x: x[1], reverse=True)

    return voteCount



if __name__ == '__main__':
    print(getFumos('Reimu')[0])