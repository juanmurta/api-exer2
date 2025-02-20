import requests
import pandas as pd
import pprint

link = "https://olinda.bcb.gov.br/olinda/servico/mecir_dinheiro_em_circulacao/versao/v1/odata/informacoes_diarias?$top=10000&$orderby=Data%20desc&$format=json"

requisicao = requests.get(link)
informacoes = requisicao.json()


tabela = pd.DataFrame(informacoes["value"])
tabela["Valor"] = tabela["Valor"].map("R${:,.2f}".format)


# pegar todas as informacoes com várias requisiçoes

tabela_final = pd.DataFrame()
pular_indice = 0

while True:
    link = f'https://olinda.bcb.gov.br/olinda/servico/mecir_dinheiro_em_circulacao/versao/v1/odata/informacoes_diarias?$top=10000&$skip={pular_indice}&$orderby=Data%20desc&$format=json'
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    tabela = pd.DataFrame(informacoes["value"])
    if len(informacoes['value']) < 1:
        break
    tabela_final = pd.concat([tabela_final, tabela])
    pular_indice += 10000

print(tabela_final)