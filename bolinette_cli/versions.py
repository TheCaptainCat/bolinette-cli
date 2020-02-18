import requests

from bolinette_cli import paths


def read_version(path):
    try:
        with open(paths.join(path, '.version')) as f:
            for line in f:
                return line.strip().replace('\n', '')
    except FileNotFoundError:
        return None


def get_last_blnt_version():
    try:
        r = requests.get('https://pypi.org/pypi/Bolinette/json')
        releases = r.json()['releases']
        last = sorted(releases.keys(), reverse=True)
        return last[0]
    except Exception:
        return None
