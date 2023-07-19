import requests
from lxml import html
from bs4 import BeautifulSoup, Comment
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

team_adress_A = {
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

brouwsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

base_api = 'https://api.sofascore.com/api/v1/team/'
end_api = '/statistics/overall'


def choose_team(time:str):
    
    data_list = []
    cont_url_list = 0
    cont_data_list = 0
    
    division = input(str('Em qual divisão está o time?')).upper()
    
    
    if division == 'A':
        serie = '325'
        id_time = team_adress_A[time.lower()][-4:]
        enpoint_17 = '13100'
        enpoint_18 = '16183'
        enpoint_19 = '22931'
        enpoint_20 = '27591'
        enpoint_21 = '36166'
        enpoint_22 = '40557'
        enpoint_23 = '48982'
        
    middle_api = f'/unique-tournament/{serie}/season/'

    url_17 = base_api + id_time + middle_api + enpoint_17 + end_api
    url_18 = base_api + id_time + middle_api + enpoint_18 + end_api
    url_19 = base_api + id_time + middle_api + enpoint_19 + end_api
    url_20 = base_api + id_time + middle_api + enpoint_20 + end_api
    url_21 = base_api + id_time + middle_api + enpoint_21 + end_api
    url_22 = base_api + id_time + middle_api + enpoint_22 + end_api

    urls_list = [url_17, url_18, url_19, url_20, url_21, url_22]
    

    for url in urls_list:
        api_link = requests.get(url, headers = brouwsers).json()
        if not 'error' in api_link:
            data_list.append(api_link['statistics'])
            if urls_list.index(urls_list[cont_url_list]) == 0:
                data_list[cont_data_list]['ano'] = 2017
            elif urls_list.index(urls_list[cont_url_list]) == 1:
                data_list[cont_data_list]['ano'] = 2018
            elif urls_list.index(urls_list[cont_url_list]) == 2:
                data_list[cont_data_list]['ano'] = 2019
            elif urls_list.index(urls_list[cont_url_list]) == 3:
                data_list[cont_data_list]['ano'] = 2020
            elif urls_list.index(urls_list[cont_url_list]) == 4:
                data_list[cont_data_list]['ano'] = 2021
            elif urls_list.index(urls_list[cont_url_list]) == 5:
                data_list[cont_data_list]['ano'] = 2022
            cont_data_list+=1
        cont_url_list+=1

    return data_list
