import requests
from requests import RequestException


def get_last_blnt_version():
    try:
        r = requests.get('https://pypi.org/pypi/Bolinette/json')
        releases = r.json()['releases']
        last = sorted(releases.keys(), reverse=True)
        return last[0]
    except RequestException:
        return None
