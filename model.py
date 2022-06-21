import requests
import json
import os
import random
from dotenv import load_dotenv
from collections import Counter

load_dotenv()
TENOR_API_KEY = os.getenv('TENOR_API_KEY')

BASE_URL_FUMO = 'https://fumo-search.herokuapp.com/api/fumo/?fumoName='
BASE_URL_SAVED_FUMOS = 'https://fumo-search.herokuapp.com/api/savedfumos/'
BASE_URL_VOTE_FUMO = 'https://fumo-search.herokuapp.com/api/vote/'



def getFumos(fumoName='', tags=set()):
    data = {'fumoName': fumoName, 'tags[]': list(tags)}
    response = requests.get(BASE_URL_FUMO, params=data)
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

def getFumoGIF(fumo):
    lmt = 150
    search_term = f"fumo touhou {fumo}"

    r = requests.get(f'https://tenor.googleapis.com/v2/search?q={search_term}&key={TENOR_API_KEY}&client_key=FumoBot&limit={lmt}')

    banned_tags = set(['my beloved', 'sex'])

    tags = set(['fumo', 'touhou'])
    if fumo != '':
        tags.add(fumo)

    def hasAllTags(gif):
        for tag in tags:
            if tag.lower() not in gif['tags']:
                return False
        for tag in banned_tags:
            if tag.lower() in gif['tags']:
                return False
        
        return True


    if r.status_code == 200:
        top_gifs = json.loads(r.text)
        top_gifs = top_gifs['results']

        fumo_gifs = filter(hasAllTags, top_gifs)

        urls = [gif['media_formats']['tinygif']['url'] for gif in fumo_gifs]
        if len(urls) == 0:
            return ''
        return random.choice(urls)

    else:
        return ''



if __name__ == '__main__':
    print(getFumoGIF())