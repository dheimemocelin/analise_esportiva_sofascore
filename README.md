# analise_esportiva_sofascore #

## Descrição ##
Este script em Python permite comparar estatísticas de dois times de futebol ao longo de diferentes anos e criar um gráfico de barras usando a biblioteca Plotly.

## Requisitos ##

Para executar o script, você precisa ter as seguintes bibliotecas instaladas:

    requests
    lxml
    BeautifulSoup
    pandas
    plotly

 ## Faça importação das bibliotecas necessárias:##

import requests
from lxml import html
from bs4 import BeautifulSoup, Comment
import pandas as pd
import plotly.graph_objects as go

Defina o dicionário team_adress_A com os endereços dos times de futebol. Certifique-se de que os endereços estão corretos e atualizados.

Defina o dicionário browsers com as configurações do User-Agent. Você pode personalizá-lo conforme necessário.

Defina as variáveis base_api e end_api com as URLs base e final da API que será utilizada para obter as estatísticas dos times.

Implemente a função choose_team(time:str) para selecionar o time e a divisão (A ou B) desejados. Essa função retornará uma lista com as estatísticas do time ao longo dos anos.

Implemente a função build_dataframe(time:str) para construir um DataFrame com as estatísticas dos times. Essa função receberá o nome do time como argumento e retornará o DataFrame.

Implemente a função build_chart(metric:str, time1:str, time2:str) para criar um gráfico de barras comparando as estatísticas dos dois times. Essa função receberá a métrica desejada, bem como os nomes dos dois times, e criará o gráfico usando a biblioteca Plotly.

## Execute o script, chamando as funções conforme necessário para obter os resultados desejados. ##

time1 = 'Flamengo'
time2 = 'Palmeiras'
metric = 'Gols'

build_chart(metric, time1, time2)


## Contribuição

Sinta-se à vontade para contribuir com melhorias para este script, abrindo uma issue ou enviando um pull request.
