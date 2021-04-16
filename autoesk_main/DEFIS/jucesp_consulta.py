import os

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from default.webdriver_utilities import *
from default.interact import press_keys_b4, press_key_b4
from default.settings import SetPaths
from default.data_treatment import ExcelToData

from default.interact import *

from default.webdriver_utilities.pre_drivers import pgdas_driver
JUCESP = 'https://www.jucesponline.sp.gov.br/Default.aspx'


class ConsultaJucesp(WDShorcuts, SetPaths, ExcelToData):
    def __init__(self, compt_file=None):
        """
        :param compt_file: from GUI

        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        from default.webdriver_utilities.pre_drivers import pgdas_driver

        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual

        sh_names = ['DEFIS']
        if compt_file is None:
            compt_file = self.compt_and_filename()
            compt, excel_file_name = compt_file
        else:
            compt, excel_file_name = compt_file

        COMPT = compt = f"DEFIS_{self.y()}"
        # transcrevendo compt para que não seja 02/2021

        # excel_file_name = '/'.join(excel_file_name.split('/')[:-1])
        excel_file_name = os.path.dirname(excel_file_name)
        excel_file_name += f'/DEFIS-anual.xlsx'
        pdExcelFile = pd.ExcelFile(excel_file_name)

        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path

            msh = pdExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}

            msh = pdExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            self.after_READ = self.readnew_lista(READ, False)
            after_READ = self.after_READ

            # self.client_path
            """
            self.driver = jucesp_driver(self.client_path, self._files_path_defis('__SeleniumThisProfille',
                                                                   tup_path=(COMPT, excel_file_name)))
            """
            self.driver = jucesp_simple_driver()
            st1time = True
            # first time login certificado
            for i, _cnpj in enumerate(after_READ['CNPJ']):
                # ####################### A INTELIGENCIA EXCEL ESTÁ SEM OS SEM MOVIMENTOS NO MOMENTO

                _cliente = after_READ['Razão Social'][i]
                _ja_declared = after_READ['Declarado'][i].upper().strip()
                _cod_sim = after_READ['Código Simples'][i]
                _cpf = after_READ['CPF'][i]
                _cert_or_login = after_READ['CERTORLOGIN'][i]

                # Dirfis exclusivos search
                _dirf_sch = after_READ['DIRF'][i]
                print(_dirf_sch)

                from pyperclip import copy
                a = copy(_cliente)

                if _cliente == '':
                    break

                if _ja_declared not in ['S', 'OK', 'FORA'] and i==8:
                    print(_cliente, '-->', {i})
                    # ############################################################################################ ↓
                    # self.client_path = self._files_path_defis(_cliente, tup_path=(COMPT, excel_file_name))
                    if _dirf_sch == '-' or '-' in _dirf_sch or _dirf_sch.strip() == '':
                        pass
                        # pdf_dirf = False
                    else:
                        pass
                    self.client_path = self._files_path_defis(_cliente, tup_path=(COMPT, excel_file_name))

                    driver = self.driver
                    super().__init__(driver)
                    driver.get(JUCESP)
                    print(self.client_path)
                    if st1time:
                        st1time = False
                        self.jucesp_loga_cert()

                    el_search = driver.find_element_by_name('ctl00$cphContent$frmBuscaSimples$txtPalavraChave')
                    el_search.clear()
                    el_search.send_keys(_cliente)
                    driver.find_element_by_id('ctl00_cphContent_frmBuscaSimples_btPesquisar').click()

                    driver.implicitly_wait(10)
                    while True:
                        try:
                            self.tag_with_text('label', 'Digite o código da imagem').click()
                            print('\033[1;31mENTER p/ prosseguir\033[m')
                            press_keys_b4('enter')
                            self.send_keys_anywhere(Keys.TAB)
                            self.send_keys_anywhere(Keys.ENTER)
                        except NoSuchElementException:
                            break
                        finally:
                            try:
                                driver.switch_to_window(driver.window_handles[1])
                                driver.close()
                                driver.switch_to_window(driver.window_handles[0])
                                break
                            except (NoSuchWindowException, IndexError):
                                pass
                                break
                    while True:
                        try:
                            driver.find_element_by_id('ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl02_lbtSelecionar').click()
                            driver.implicitly_wait(10)

                            self.enable_download_in_headless_chrome(self.client_path)
                            driver.find_element_by_name('ctl00$cphContent$frmPreVisualiza$btnEmitir').click()
                            break
                        except NoSuchElementException:
                            try:
                                self.enable_download_in_headless_chrome(self.client_path)
                                driver.find_element_by_name('ctl00$cphContent$frmPreVisualiza$btnEmitir').click()
                                break
                            except NoSuchElementException:
                                print('Não foi possível...\n033[1;36m f9 após encontrar\033[m')
                                press_keys_b4('f9')
        [(sleep(1), print(f'Sleeping and closing - {cont}')) for cont in range(5)]

    def jucesp_loga_cert(self):
        """
        jucesp only ##################################
        """

        from pyautogui import hotkey
        driver = self.driver
        cert_id = 'ctl00_frmLogin_lbtAcessoCertificado'
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, cert_id)))
        driver.find_element_by_id(cert_id).click()
        self.start_thread(sleep(2.5))

        # B4 enter, ir pra baixo por causa do certificado do castilho
        #self.start_thread(hotkey('down'))
        self.start_thread(sleep(2))
        self.start_thread(hotkey('enter'))

    @staticmethod
    def start_thread(target):
        from threading import Thread
        # self.refresh()
        Thread(target=target).start()

    def enable_download_in_headless_chrome(self, download_dir):
        """
        criado aqui, sobrescrevido...
        :param download_dir:
        :return:
        """
        driver = self.driver
        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)


ConsultaJucesp()
