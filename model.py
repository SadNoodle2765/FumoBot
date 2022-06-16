import requests
import json

BASE_URL_FUMO = 'https://fumo-search.herokuapp.com/api/fumo/?fumoName='

def getFumos(fumoName=''):
    response = requests.get(BASE_URL_FUMO + fumoName)
    data = json.loads(response.text)

    data.sort(key=lambda fumo: fumo['buyoutPrice'] if fumo['buyoutPrice'] != 0 else fumo['price'])

    return data


if __name__ == '__main__':
    print(getFumos('Reimu')[0])