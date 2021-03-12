import pyautogui as pygui
from time import sleep

from default.interact import *

from imports import ExcelToData
from _new_set_paths import NewSetPaths

from pgdas_fiscal_oesk.relacao_nfs import tres_valores_faturados, NfCanceled
from pyperclip import paste
# from default.webdriver_utilities import *

"""
from LE_NF_CANCELADAS_cor import main as nf_canceled
import ATIVA_EMPRESA
import PROGRAMA_REQUIRED
import NEEDED_PANDAS
from datetime import datetime
import os
"""

possible = ['G5_ISS', 'G5_ICMS']
# um por um?
# vai p/ NEEDED_PANDAS


class Fantasia(NewSetPaths, ExcelToData):

    def __init__(self):
        """
        :param compt_file: from GUI

        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        from default.webdriver_utilities.pre_drivers import pgdas_driver
        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual

        sh_names = possible
        compt_file = super().get_compt_only()
        excel_file_name = super().excel_file_path()

        # ###############################
        self.abre_programa('G5')
        # ###############################
        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path
            mshExcelFile = pd.ExcelFile(excel_file_name)

            msh = mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = mshExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            self.after_READ = self.readnew_lista(READ, False)
            after_READ = self.after_READ
            for i, CNPJ in enumerate(after_READ['CNPJ']):

                # ####################### A INTELIGENCIA EXCEL ESTÁ SEM OS SEM MOVIMENTOS NO MOMENTO
                CLIENTE = after_READ['Razão Social'][i]
                JA_DECLARED = after_READ['Declarado'][i].upper().strip()
                CodSim = after_READ['Código Simples'][i]
                CPF = after_READ['CPF'][i]
                cont_ret_n_ret = i

                datageral = self.first_and_last_day_compt('/')[1]
                # print(datageral)
                if CLIENTE == '':
                    break

                if sh_name == 'G5_ICMS' and sh_name in possible:
                    pass

                elif sh_name == 'G5_ISS' and sh_name in possible:
                    self.client_path = self.files_pathit(CLIENTE)
                    meus_3_valores_atuais = tres_valores_faturados(self.client_path)
                    # Se tem 3valores[excel], tem XML. Se não tem, não tem
                    # (pois o xml e excel vem do ginfess_download)....

                    registronta = self.registronta(CLIENTE, compt_file)
                    print(CLIENTE)
                    if meus_3_valores_atuais and registronta:
                        all_xls_inside = self.files_get_anexos_v3(CLIENTE, file_type='xlsx', compt=compt_file)
                        relacao_notas = all_xls_inside[0] if len(all_xls_inside) == 1 else IndexError()
                        self.activating_client(self.formatar_cnpj(CNPJ))
                        # Agora vai ser por cnpj...
                        self.start_walk_menu()

                        # access ISS lançamento
                        pygui.hotkey('right', 'down', 'enter', 'up', 'up', 'enter', interval=.1)
                        sleep(3.5)

                        foritab(2, 'down')
                        # busca XML
                        pygui.write(self.get_xml(CLIENTE))

                        """IMPORTA ITENS OU NÃO"""
                        if 'Exatitec' in CLIENTE:
                            # aqui mais pra frente irei validar melhor SE IMPORTA ITEMS OU NÃO
                            w = pygui.getActiveWindow()
                            pygui.click(w.center)
                            pygui.move(-210, 80) # Importar itens window 1
                            pygui.click()
                            foritab(2, 'tab')
                            pygui.hotkey('enter')

                            # window 2, mt legal
                            sleep(2)
                            w2 = pygui.getActiveWindow()
                            pygui.click(w2.center, clicks=0)
                            pygui.move(65, -160)# Copiar configuração da nota...?
                            pygui.click()
                            pygui.hotkey('tab', 'enter')
                            sleep(1)
                            pygui.write('1')
                            pygui.hotkey('enter')
                            foritab(15, 'tab')
                            print('Sleeping 2.5 pra enter, enter')
                            sleep(2.5)
                            foritab(2, 'enter', 1)
                            sleep(1)
                            pygui.hotkey('alt', 'f4')

                        nfcanceladas = NfCanceled(relacao_notas)

                        print('SLEEPING PARA IMPORTAR')
                        self.importa_nfs()
                        try:
                            qtd_els = nfcanceladas.conta_qtd_nfs()
                            sleep(qtd_els)
                        except TypeError:
                            sleep(5.5)
                        pygui.hotkey('enter')

                        # vai sleepar dependendo da quantidade de notas, programar ainda isso

                        # #### recente
                        sleep(1)
                        pygui.keyDown('shift')
                        foritab(2, 'tab')
                        pygui.keyUp('shift')

                        pygui.hotkey('enter')
                        sleep(2)
                        #####
                        """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LE_NF_CANCELADAS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
                        self.start_walk_menu()
                        print('right down enter enter')
                        pygui.hotkey('right', 'down', 'enter', 'enter', interval=.5)
                        sleep(2)
                        print('NF canceled')

                        nfcanceladas.action()
                        # Cancela

                        # p.hotkey('alt', 'tab')
                        print('NF canceled FORA')

                        sleep(1)
                        # generate PDF relat. Prestados 51
                        self.start_walk_menu()
                        foritab(3, 'right')
                        foritab(6, 'down')

                        foritab(5, 'enter', interval=.25)
                        # generate pdf
                        sleep(5)
                        # self.most_recent_file()
                        print('estou contando com o Adobe, pois o PDF do G5 é aberto nele...')

                        all_keys('ctrl', 'shift', 's')
                        sleep(6)
                        all_keys('enter')
                        sleep(1)
                        all_keys('ctrl', 'x')
                        [(pygui.hotkey('alt', 'f4'), sleep(1)) for i in range(2)]
                        path_file_temp_file = f"C:\\tmp\\{paste()}"
                        sleep(2)
                        filenewname = f'{self.client_path}\\Registro_ISS-{CNPJ}.pdf'
                        self.move_file(path_file_temp_file, filenewname)

                        """save in adobe"""

    def get_xml(self, cliente):
        b = self.files_get_anexos_v3(cliente, file_type='xml', upload=False)
        b = b[0]
        b = b.split('\\')
        file = f'\\\\{b[-1]}'
        final = '\\'.join(b[:-1]) + file
        return final

    def formatar_cnpj(self, cnpj):
        cnpj = str(cnpj)
        if len(cnpj) < 14:
            cnpj = cnpj.zfill(11)
        cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        print(cnpj)  # 123.456.789-00
        return cnpj

    def registronta(self, client, compt_file):
        """
        :param client: CLIENTE
        :param compt_file: compt_file
        :return: se tiver pdf que tem ISS e REGISTRO
        """
        registronta = False
        for f in self.files_get_anexos_v3(client, file_type='pdf', compt=compt_file):
            if 'ISS' in f.upper():
                registronta = False
                break
            else:
                registronta = True
        return registronta

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

    def activating_client(self, client_cnpj):
        x, y = 30, 60
        sleep(2)
        pygui.click(x, y)
        sleep(.7)
        # ativa empresa

        comp = self.first_and_last_day_compt('')[1]
        pygui.write(comp)

        foritab(6, 'tab') # PESQUISA
        pygui.hotkey('enter')
        sleep(1.5)
        all_keys('shift', 'tab')
        sleep(1)
        foritab(6, 'down') # PESQUISAR POR CGC[CNPJ]
        sleep(.5)
        foritab(1, 'tab') # Digite a frase contida no texto
        all_keys(client_cnpj)
        print(f'{client_cnpj}:^~30')

        all_keys('ctrl', 'down')
        foritab(2, 'enter', interval=1)
        sleep(1)

        pygui.hotkey('tab', 'enter', interval=1)
        # Caso apareça aquela mensagem chata

        # ##################################################### PAREUI DAQUI, SELECIONEI JÁ... MAS TESTAR...
        # sleep(20)

    def importa_nfs(self):
        sleep(2.5)
        w3 = pygui.getActiveWindow()
        pygui.click(w3.center, clicks=0)
        pygui.move(0, 150)
        pygui.click()

    def start_walk_menu(self):
        x, y = 30, 30
        pygui.click(x, y)

Fantasia()