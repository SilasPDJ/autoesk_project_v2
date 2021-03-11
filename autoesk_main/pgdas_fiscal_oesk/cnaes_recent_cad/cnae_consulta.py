from selenium.webdriver.firefox import webdriver
# from selenium.webdriver.chrome import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4
import pandas as pd
import json



def part1():
    # 1. Pegar conteúdo HTML a partir da URL
    option = Options()
    option.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path='Chromedriver\\chromedriver.exe', options=option)
    driver.get('https://www.contabilizei.com.br/contabilidade-online/cnae/')
    elem = driver.find_element_by_xpath('//*[@id="wtr-content"]/div[2]/table[1]')
    html_content = elem.get_attribute('outerHTML')
    # 2. Parsear o conteúdo HTML a partir da URL
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    driver.quit()
    table = soup.find(name='table')

    # 3. Estruturar conteúdo em um Data Frame
    df_full = pd.read_html(str(table), encoding='utf8')[0]
    # df_full = pd.read_html(str(table), encoding='utf8')[0].head(10)
    # ele foi mais rápido do que com o head xD

    # 4. Transformar os Dados em um dicionário de dados próprio
    df = df_full[['Anexo', 'Código Cnae', 'Descrição', 'Fator R']]
    cnae_dict = {}
    cnae_dict['cnae'] = df.to_dict('records')

    # 5. Converter e salvar em um arquivo JSON

    with open("cnaes.json", "w") as fp:
        json.dump(cnae_dict, fp)  

# part1()


file = 'cnaes.json'
with open(file) as f:
    data = json.loads(f.read())
    
cnaes = data['cnae']

for valor in cnaes:
    # print(valor)
    # cod = valor['Código Cnae']
    # desc = valor['Descrição']
    anexo, cod, desc = valor.items()
    if anexo[1] == 'III':
        print(valor)
    # print(anexo)


