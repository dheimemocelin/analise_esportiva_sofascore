from fastapi import FastAPI, HTTPException
import requests

TEAM_ADDRESS_A = {
    'Botafogo': 'botafogo/1958',
    'Grêmio': 'gremio/5926',
    'Flamengo': 'flamengo/5981',
    'Palmeiras': 'palmeiras/1963',
    'Red Bull Bragantino': 'red-bull-bragantino/1999',
    'Fluminense': 'fluminense/1961',
    'sao paulo': 'sao-paulo/1981',
    'Internacional': 'internacional/1966',
    'Athletico': 'athletico/1967',
    'Atlético Mineiro': 'atletico-mineiro/1977',
    'Fortaleza': 'fortaleza/2020',
    'Cruzeiro': 'cruzeiro/1954',
    'Cuiabá': 'cuiaba/49202',
    'Santos': 'santos/1968',
    'Bahia': 'bahia/1955',
    'Corinthians': 'corinthians/1957',
    'Goiás': 'goias/1960',
    'Vasco': 'vasco/1974',
    'América Mineiro': 'america-mineiro/1973',
    'Coritiba': 'coritiba/1982'
}

BROWSERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

BASE_API = 'https://api.sofascore.com/api/v1/team/'
END_API = '/statistics/overall'

SEASONS = {
    2017: '13100',
    2018: '16183',
    2019: '22931',
    2020: '27591',
    2021: '36166',
    2022: '40557'
}

app = FastAPI()


def fetch_team_stats(team: str, division: str = 'A'):
    if division != 'A':
        raise ValueError('Only division A is supported')

    address = TEAM_ADDRESS_A.get(team)
    if not address:
        raise ValueError('Team not found')

    team_id = address.split('/')[-1]
    serie = '325'
    data = []

    for year, endpoint in SEASONS.items():
        url = f"{BASE_API}{team_id}/unique-tournament/{serie}/season/{endpoint}{END_API}"
        response = requests.get(url, headers=BROWSERS)
        if response.status_code != 200:
            continue
        json_data = response.json()
        if 'error' in json_data:
            continue
        stats = json_data['statistics']
        stats['ano'] = year
        data.append(stats)

    return data


@app.get('/stats/{team}')
def get_team_stats(team: str, division: str = 'A'):
    try:
        stats = fetch_team_stats(team, division)
        if not stats:
            raise HTTPException(status_code=404, detail='Statistics not found')
        return stats
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
