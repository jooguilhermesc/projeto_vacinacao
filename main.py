import requests
from bs4 import BeautifulSoup
import pyodbc


def retorna_conexao_sql():
    """
    Realiza conexão com o banco de dados SQL Server
    :return:
    """
    server = "localhost\SQLEXPRESS"
    database = "teste_python"
    string_conexao = 'Driver={SQL Server Native Client 11.0};Server=' + server + ';Database=' + database + ';Trusted_Connection=yes;'
    conexao = pyodbc.connect(string_conexao)

    return conexao.cursor()

def extrair_infos(comando, cursor):
    """
    Extrai dados da tabela no banco de dados com informações e links antigos da página do vacinômetro
    :param comando:
    :param cursor:
    :return:
    """
    comando_extrair = comando
    cursor.execute(comando_extrair)

    rows = cursor.fetchall()

    return rows

def raspagem_content(infos):
    """
    Recebe informações extraídas da tabela com links antigos da página do vacinômetro
    :param infos:
    :return:
    """
    links = infos

    for link in links:
        url = link[0]
        data = link[1]
        pagina = requests.get(url)
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
            cursor.execute(comando_registro)
            cursor.commit()

cursor = retorna_conexao_sql()
comando_sql = "SELECT * FROM links_vacinacao"
infos = extrair_infos(comando_sql,cursor)
raspagem_content(infos)