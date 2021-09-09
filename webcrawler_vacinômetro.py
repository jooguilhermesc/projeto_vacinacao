import requests
from bs4 import BeautifulSoup
import pyodbc
from datetime import datetime

def retorna_conexao_sql():
    server = "localhost\SQLEXPRESS"
    database = "teste_python"
    string_conexao = 'Driver={SQL Server Native Client 11.0};Server=' + server + ';Database=' + database + ';Trusted_Connection=yes;'
    conexao = pyodbc.connect(string_conexao)

    return conexao.cursor()

cursor = retorna_conexao_sql()

link = "https://vacina.maceio.al.gov.br/#vacinometro"
data = datetime.today().strftime('%Y-%m-%d')
pagina = requests.get(link)
soup = BeautifulSoup(pagina.content, 'html.parser')

tablerows = soup.findAll('tr')

for tablerow in tablerows:
        infos = tablerow.findAll('td')
        grupo = infos[0].get_text()
        primeira_dose = int(infos[1].get_text().replace(".",""))
        segunda_dose = int(infos[2].get_text().replace(".",""))
        total = int(infos[3].get_text().replace(".",""))
        comando_registro = f"INSERT INTO infos_vacinacao VALUES ('{grupo}', '{primeira_dose}', '{segunda_dose}', '{total}', '{data}')"
        print(comando_registro)
        #cursor.execute(comando_registro)
        #cursor.commit()