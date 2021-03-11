from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from default.webdriver_utilities import *
from default.interact import press_keys_b4, press_key_b4
from default.settings import SetPaths
from default.data_treatment import ExcelToData

from default.webdriver_utilities.pre_drivers import webdriver
import default.interact as interact


import pyautogui as pygui
from time import sleep
# import pywinauto as pwin
import pandas as pd

weblink = 'https://portal.gissonline.com.br/login/index.html'

link = "ChromeDriver/chromedriver.exe"
# ...

sh_name = 'GISS'


# self.pyautogui
class GissGui(WDShorcuts, SetPaths, ExcelToData):
    from selenium.webdriver.common.by import By

    def __init__(self, fname, compt_file=None):
        from os import chdir, path, getcwd
        from time import sleep
        from smtp_project.init_email import JsonDateWithImprove as Jj

        if compt_file is None:
            # compt, excel_file_name = self.get_atual_compt_set(1)
            compt_file = self.set_get_compt_file(1)

        json_file = Jj.load_json(fname)
        # input(len(after_READ['CNPJ']))
        for eid in json_file.keys():
            print('~'*30)
            print(eid)
            print('~' * 30)
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'*10)
            # print(list_with_dict)
            list_with_dic = json_file[eid]

            values = [v.values() for v in list_with_dic[:]]
            _cliente, _feito, _logar, self._construcao, _notes = self.any_to_str(*values[:5])

            client_path = self._files_path_v3(_cliente, wexplorer_tup=compt_file)
            self.client_path = client_path
            self.volta = getcwd()

            os.chdir(path.realpath('\\'.join(__file__.split('\\')[:-1])))
            with open('data_clients_files/giss_passwords.txt') as f:
                __senhas = f.read().split(',')
            os.chdir(volta)

            [print(s) for s in __senhas]
            print('~'*30, 'SENHAS')

            # if _feito not in ["checkar", "ok"]:
            self.driver = webdriver.Chrome(link)
            self.driver.minimize_window()
            super().__init__(self.driver)
            driver = self.driver
            driver.get(weblink)
            chrome = driver
            cont_senha = 0
            while True:
                # TxtIdent
                driver.find_element_by_xpath('//input[@name="TxtIdent"]').send_keys(_logar)
                driver.find_element_by_xpath('//input[@name="TxtSenha"]').send_keys(__senhas[cont_senha])
                print(f'Senha: {__senhas[cont_senha]}', end=' ')
                cont_senha += 1
                driver.find_element_by_link_text("Acessar").click()
                try:
                    WebDriverWait(chrome, 5).until(expected_conditions.alert_is_present(),
                                                   'Timed out waiting for PA creation ' +
                                                   'confirmation popup to appear.')
                    alert = chrome.switch_to.alert
                    alert.accept()
                    print("estou no try")
                    driver.execute_script("window.history.go(-1)")
                except TimeoutException:
                    print("no alert, sem alerta, exceptado")
                    break
                    # holy
            iframe = driver.find_element_by_xpath("//iframe[@name='header']")
            driver.switch_to.frame(iframe)
            if self._construcao.lower().strip() != 'sim':
                driver.find_element_by_xpath("//img[contains(@src,'images/bt_menu__05_off.jpg')]").click()

            else:
                print('Construção Civil?')
                self.constr_civil()
            driver.switch_to.default_content()
            sleep(3.5)
            if self._construcao.lower() == 'sim':
                self.fazendo_principal(True)
            else:
                self.fazendo_principal()
        print('GISS encerrado!')

    def readnew_lista(self, READ, print_values=False):
        """ TRANSFORMO EM DICIONÁRIO, CONTINUAR"""
        get_all = {}
        new_lista = []
        for k, lista in READ.items():
            for v in lista:
                v = str(v)
                v = v.replace(u'\xa0', u' ')
                v = v.strip()
                if str(v) == 'nan':
                    v = ''
                new_lista.append(v)
            get_all[k] = new_lista[:]
            new_lista.clear()
        if print_values:
            for k, v in get_all.items():
                print(f'\033[1;32m{k}')
                for vv in v:
                    print(f'\033[m{vv}')
        return get_all

    def fazendo_principal(self, constr=False):
        """
        o click do prestador está no init
        :return:
        """

        driver = self.driver
        if not constr:
            self.write_date()
        try:
            driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[4]/a').click()
            # driver.find_elements_by_xpath("//*[contains(text(), 'Encerrar Escrituração ')]")[0].click()
            try:
                sleep(2)
                driver.find_elements_by_xpath("//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                # PrintScreenFinal(clien)

            except (NoSuchElementException, IndexError):
                print('Provavelmente já foi declarada... Ou tem que encerrar sem movimento')
                # .................
        except NoSuchElementException:
            print('Exception line 140, sem PRESTADOR')
            # print("BACKEI. Aqui vai ser a parte 2")
        driver.switch_to.default_content()
        iframe = driver.find_element_by_xpath("//iframe[@name='header']")
        sleep(2.5)
        driver.switch_to.frame(iframe)
        driver.find_element_by_xpath('//img[contains(@src,"bt_menu__06_off.jpg")]').click()
        driver.switch_to.default_content()
        iframe = driver.find_element_by_xpath("//iframe[@name='principal']")
        driver.switch_to.frame(iframe)

        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TOMADOR """
        cont = 0
        for i in range(2):
            sleep(3)
            a = driver.find_elements_by_tag_name('a')
            print(len(a))

            a[4].click()
            sleep(1.5)
            try:
                driver.find_elements_by_xpath("//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                break
            except IndexError:
                try:
                    driver.find_element_by_link_text('Menu Principal').click()
                except NoSuchElementException:
                    driver.find_element_by_link_text('OK').click()
            # test

            """Se eu quiser reacessar lá, vou precisar desse código abaixo e dar refresh"""
            """
            driver.refresh()
            sleep(2)
            iframe = driver.find_element_by_xpath("//iframe[@name='header']")
            driver.switch_to.frame(iframe)
            driver.find_element_by_xpath('//img[contains(@src,"bt_menu__06_off.jpg")]').click()
            driver.switch_to.default_content()
            sleep(2.5)
            iframe = driver.find_element_by_xpath("//iframe[@name='principal']")
            driver.switch_to.frame(iframe)
            a = driver.find_elements_by_tag_name('a')
            a[4].click()
            """
        """~~~~~~~~~~~~~~~~~"""
        print('ESC p/ continuar')
        # WINDOW_MANAGEMENT.continua()
        """~~~~~~~~~~~~~~~~"""
        # pressione "ESC" para continuar

    def constr_civil(self):
        # parei nessa belezinha aqui, tomador e prestador tão ok
        XPATH = "//*[contains(text(), '- Serviço da Construção Civil')]", "//*[contains(text(), '- Demais Serviços')]"

        driver = self.driver
        driver.find_element_by_xpath('//img[contains(@src,"bt_menu__06_off.jpg")]').click()
        sleep(2)
        driver.switch_to.default_content()
        self.write_date()
        for contX in range(len(XPATH)):
            driver.switch_to.default_content()
            sleep(2)

            iframe = driver.find_element_by_xpath("//iframe[@name='header']")
            driver.switch_to.frame(iframe)
            construcao = self._construcao
            driver.find_element_by_xpath('//img[contains(@src,"bt_menu__07_off.jpg")]').click()

            driver.switch_to.default_content()
            sleep(2)
            iframe = driver.find_element_by_xpath("//iframe[@name='principal']")
            driver.switch_to.frame(iframe)

            driver.find_element_by_xpath(XPATH[contX]).click()
            # XPATH
            # input("faça os processos daqui pra baixo")

            if contX == 0:
                ttt = 5.0
                for i in range(2):
                    sleep(ttt)
                    ttt -= 2.5
                    driver.find_element_by_xpath("//*[contains(text(), 'Encerrar Competência')]").click()
                try:
                    WebDriverWait(driver, 3).until(expected_conditions.alert_is_present(),
                                                   'Timed out waiting for PA creation ' +
                                                   'confirmation popup to appear.')
                    # ENCERRADO
                    driver.switch_to.alert.accept()
                    sleep(5)
                except (NoAlertPresentException, TimeoutException):
                    print('no alert')


                driver.refresh()
                # input('drive refresh')
            elif contX == 1:
                driver.find_element_by_xpath("//*[contains(text(), 'Encerrar Escrituração')]").click()
                driver.find_elements_by_xpath("//*[contains(text(), 'CLIQUE AQUI')]")[0].click()
                # ENCERRADO
                sleep(5)

    def write_date(self):
        from datetime import datetime, date
        from dateutil.relativedelta import relativedelta
        # from datetime import timedelta

        mes = datetime.now().month
        ano = datetime.now().year
        driver = self.driver
        datageral = date(ano, mes, 1) - relativedelta(months=1)
        mes = str(datageral.month)
        ano = str(datageral.year)
        sleep(5)
        iframe = driver.find_element_by_xpath("//iframe[@name='principal']")
        driver.switch_to.frame(iframe)
        self.tag_wait(driver, 'input')
        driver.find_element_by_xpath('//input[@name="mes"]').send_keys(mes)
        driver.find_element_by_xpath('//input[@name="ano"]').send_keys(ano)

    def tag_wait(self, driver, tag):
        delay = 10
        try:
            my_elem = WebDriverWait(driver, delay).until(expected_conditions.presence_of_element_located((self.By.TAG_NAME, tag)))
            print(f"\033[1;31m{tag.upper()}\033[m is ready!")
        except TimeoutException:
            input("Loading took too much time!")
