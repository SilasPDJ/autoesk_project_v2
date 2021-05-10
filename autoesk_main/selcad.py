import pandas as pd
import json
# https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/
import os
import json
from itertools import count

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from random import randint, choice, sample

from selenium.common.exceptions import NoSuchElementException

import pickle

from selenium.webdriver.support.ui import Select

from time import sleep

# passwd = open('dados_json/passwd', 'r').read()
passwd = 'silassoueu123S'

path = os.path.dirname(__file__)

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('default/webdriver_utilities/Chromedriver/chromedriver.exe', options=chrome_options)
# driver.maximize_window()
driver.get('http://127.0.0.1:8000/admin/')
sleep(1.5)
print('dale1')


def login():
    driver.find_element_by_name('username').send_keys('silaspodejogar')
    driver.find_element_by_name('password').send_keys(passwd)
    driver.find_element_by_css_selector('input[type="submit"]').click()


login()

sleep(1.5)

try:
    excel = pd.read_excel(
        "/mnt/c/Users/Silas/OneDrive/_FISCAL-2021/__EXCEL POR COMPETENCIAS__/DEFIS-anual.xlsx"
    )
except FileNotFoundError:
    excel = pd.read_excel(
        "C:/Users/Silas/OneDrive/_FISCAL-2021/__EXCEL POR COMPETENCIAS__/DEFIS-anual.xlsx"
    )


socios_dict = pd.read_excel("C:/Users/Silas/OneDrive/_FISCAL-2021/__EXCEL POR COMPETENCIAS__/DEFIS-anual.xlsx", sheet_name=1).to_dict()

excel_dict = excel.to_dict()

the_keys = list(excel_dict.keys())

max_counter = 70
counter = 30 # Souza
lavida = 1
for counter in range(counter, max_counter):
    driver.get("http://127.0.0.1:8000/admin/cadastro/empresa/add/")

    rs = list(excel_dict[the_keys[0]].values())[counter]

    cnpj = list(excel_dict[the_keys[1]].values())[counter]
    cpf = list(excel_dict[the_keys[2]].values())[counter]
    cnae = list(excel_dict['CNAE'].values())[counter]
    desc = list(excel_dict['Descrição'].values())[counter]
    tipo_empresa, porte_empresa = list(excel_dict['TIPO'].values())[counter].rsplit(' ', 1)
    porte_empresa = porte_empresa.replace('.', '').replace('(', '').replace(')', '').strip()
    tipo_empresa = tipo_empresa.strip().title()

    ac = ActionChains(driver)
    print('sleeping')
    sleep(3)
    for dale in rs, rs, cnpj, cpf:
        print(dale)
        dale = str(dale)
        dale = dale.replace('.0', '') if dale.endswith('.0') else dale

        ac.send_keys(dale)
        ac.send_keys(Keys.TAB)

    # ac.click(driver.find_element_by_name("_save").click())
    [ac.send_keys(Keys.TAB) for i in range(3)]
    ac.pause(1)
    ac.perform()

    # ac = ActionChains(driver)
    # cia_typ = Select(driver.find_element_by_name('tipo_empresa'))
    # depois...

    # select cnaes
    select = Select(driver.find_element_by_name('cnaes_set-0-cnae'))
    if lavida == 1:
        all_values = [o.text for o in select.options]
        partial_all_values = [o.split()[0] for o in all_values]
        lavida = 0
        # lavida liga desliga pra não demorar muito
    ind_searched = partial_all_values.index(cnae)
    select.select_by_visible_text(all_values[ind_searched])

    select_tipo_empresa = Select(driver.find_element_by_id('id_tipo_empresa'))
    ste_opt = select_tipo_empresa.options
    # [print(f.text) for f in ste_opt]
    try:
        select_tipo_empresa.select_by_visible_text(tipo_empresa)
    except NoSuchElementException:
        select_tipo_empresa.select_by_visible_text(tipo_empresa.upper())
    select_porte_empresa = Select(driver.find_element_by_id('id_porte_empresa'))
    select_porte_empresa.select_by_value(porte_empresa)

    # input('b4 input')
    driver.find_element_by_name('_addanother').click()

print('Finish')
# Faz login
# 4520-0/01; 4751-2/01