from imports import WDShorcuts, ExcelToData
from imports import Keys, By, WebDriverWait, expected_conditions
from imports import TimeoutException, ElementClickInterceptedException, NoSuchElementException, NoAlertPresentException
from imports import activate_window, press_key_b4, foritab
from imports import contmatic_select_by_name
from imports import pgdas_driver


from _new_set_paths import NewSetPaths

import pyautogui as pygui
from time import sleep
# import pywinauto as pwin
import pandas as pd
import os

link = "ChromeDriver/chromedriver.exe"
possible = ['GIA']


class GIA(WDShorcuts, NewSetPaths, ExcelToData):

    def __init__(self):
        menuX, menuY = 20, 27
        self.compt_used = super().get_compt_only()
        excel_file_name = super().excel_file_path()

        mshExcelFile = pd.ExcelFile(excel_file_name)

        def fecha_janela_contribuintes_gia():
            sleep(1)
            pygui.click(1322, 333, duration=.5)
            pygui.hotkey('left', 'enter')
        # self.GIA()

        #
        # mudei do for pra ca
        self.abre_programa(self.get_env_for_path('\\Desktop\\GIA.exe'), path=True)
        for sh_name in possible:
            msh = mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = mshExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            after_READ = self.readnew_lista(READ, False)
            # input(len(after_READ['CNPJ']))

            from os import getcwd, chdir

            volta = getcwd()
            for i, valor in enumerate(after_READ['login']):

                login = after_READ['login'][i]
                senha = after_READ['senha'][i]
                r_social = after_READ['Razão Social'][i]
                transmitida = after_READ['transmitida'][i]
                feita = after_READ['GIA'][i]
                ie = after_READ['CNPJ'][i]
                my_print = login
                print(my_print)
                # pygui.hotkey('alt', 'tab')
                print(ie)
                #
                self._client_path = self.files_pathit('GIA_' + r_social)
                _client_path = self._client_path

                if 'sim' != feita.strip().lower() != 'ok':
                    try:
                        fecha_janela_contribuintes_gia()
                    except IndexError:
                        print('Não precisei fechar')
                    self.pt1_gia_software(ie, self.compt_used)

                    pygui.doubleClick(menuX+35, menuY)
                    # consistir
                    sleep(3)
                    pygui.click(menuX, menuY)
                    sleep(.5)
                    foritab(2, 'up')
                    pygui.hotkey('enter')
                    pygui.click(x=836, y=394)
                    foritab(7, 'tab')
                    pygui.hotkey('enter', 'enter', interval=.25)
                    pygui.hotkey('enter')
                    self.save_novagia_pdf()

                if 'sim' != transmitida.strip().lower() != 'ok':

                    self.driver = pgdas_driver(_client_path)
                    driver = self.driver
                    super().__init__(self.driver)
                    driver.get('https://www3.fazenda.sp.gov.br/CAWEB/Account/Login.aspx')
                    llg = driver.find_element_by_id('ConteudoPagina_txtUsuario')
                    llg.clear()
                    llg.send_keys(login)

                    ssn = driver.find_element_by_xpath("//input[@type='password']")
                    ssn.clear()
                    ssn.send_keys(senha)

                    self.send_keys_anywhere(Keys.TAB)
                    self.send_keys_anywhere(Keys.ENTER)
                    print('pressione f7 p/ continuar após captcha')
                    press_key_b4('f8')
                    # self.find_submit_form()
                    # enter entrar
                    sleep(5)
                    driver.find_element_by_link_text('Nova GIA').click()
                    sleep(3)
                    driver.find_element_by_partial_link_text('Documentos Fiscais (Normal, Substit. e Coligida)').click()
                    sleep(2)
                    driver_clicks = driver.find_elements_by_xpath("//input[@type='file']")

                    driver_clicks[0].send_keys(self.clieninput_filepath())
                    driver.find_elements_by_xpath("//input[@type='button']")[0].click()
                    try:
                        driver.switch_to.alert.accept()
                    except NoAlertPresentException:
                        print('Sem alerta')
                    sleep(5)
                    """
                    bt_imprime = driver.find_element_by_css_selector('[alt="Imprimir"]')
                    self.exec_list(click=bt_imprime, enter=pygui)
                    print('Glória a Deus f7 p continuar')
                    press_key_b4('f7')
                    """
                    self.save_save_img2pdf()
                    driver.close()
                    sleep(5)
                    # pygui.hotkey('enter')
                    # ############################################ parei daqui

    def save_save_img2pdf(self):
        from PIL import Image
        path1 = f'{self._client_path}/GiaScreenShoot.png'
        path2 = f'{self._client_path}/Recibo_{self.compt_used}.pdf'
        self.driver.save_screenshot(path1)
        image1 = Image.open(path1)
        try:
            im1 = image1.convert('RGB')
        except ValueError:
            im1 = image1
        im1.save(path2)

    def save_novagia_pdf(self):
        from shutil import copy
        pathinit = r'C:\Users\user\Documents\SEFAZ\GIA\TNormal'
        pathinit += f'\\{os.listdir(pathinit)[0]}'
        # copy(r"C:\Users\User\Documents\SEFAZ\GIA\TNormal\{}".format(os.listdir(r"C:\Users\User\Documents\SEFAZ\GIA\TNormal")[0]), r"C:\Users\user\OneDrive\_FISCAL-2021\2021\01-2021\GIA_Tharles Marli")
        copy(pathinit, self._client_path)

    def pt1_gia_software(self, ie, cpt_write):
        cpt_write = "".join(cpt_write.split('-'))
        print(cpt_write
              )
        menuX, menuY = 20, 27
        [pygui.click(menuX, menuY, duration=2.5) for i in range(1)]
        sleep(2)
        pygui.hotkey('tab', 'enter', interval=.25)
        foritab(2, 'tab')
        pygui.write(ie, interval=.1)
        foritab(2, 'tab', 'enter')
        pygui.hotkey('tab', 'tab', 'enter')
        sleep(.2)
        pygui.write(cpt_write)
        sleep(.5)
        pygui.hotkey('tab', 'enter')
        sleep(.2)
        pygui.hotkey('left', 'enter', 'enter', 'tab', 'enter', interval=.25)

    def clieninput_filepath(self, filetype='sfz'):

        dir_searched_now = self._client_path
        file = [os.path.join(dir_searched_now, fname) for fname in os.listdir(dir_searched_now) if fname.lower().endswith(filetype)]

        return file[0] if len(file)==1 else False

    def exec_list(self, **args):
        """
        :param args: somente dicionarios
        :return:
        """
        from time import sleep
        import pyautogui as pygui
        from concurrent.futures import ThreadPoolExecutor
        executors_list = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            for key, vs in args.items():
                if key == 'click':
                    executors_list.append(executor.submit(vs.click))
                else:
                    executors_list.append(executor.submit(pygui.hotkey, str(key)))
                    print('else')
                sleep(2)
                print('sleeping')

    def abre_programa(self, name, path=False):
        """
        :param name: path/to/nameProgram
        :param path: False => contmatic, True => any path
        :return: winleft+r open
        """
        if path is False:
            programa = contmatic_select_by_name(name)
        else:
            programa = name

        senha = '240588140217'
        sleep(1)
        pygui.hotkey('winleft', 'r')
        # pesquisador
        sleep(1)
        pygui.write(programa)
        sleep(1)
        pygui.hotkey('enter')

        sleep(10)

        # p.write(senha)
        # p.hotkey('tab', 'enter', interval=.5)

        pygui.sleep(5)
        # pygui.click(x=1508, y=195) # fecha a janela inicial no G5

    def get_env_for_path(self, path='\\Desktop\\GIA.exe'):

        p1path = os.getenv('APPDATA')
        p1path = os.path.abspath(os.path.join(os.path.dirname(p1path), '..'))
        p1path += path
        return p1path

        # CONTMATIC_PATH = p1path + r'\Microsoft\Windows\Start Menu\Programs\Contmatic Phoenix'
