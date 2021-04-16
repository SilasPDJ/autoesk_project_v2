from imports import WDShorcuts, ExcelToData
from _new_set_paths import NewSetPaths
from imports import sleep, press_keys_b4

import pyautogui as pygui

import pandas as pd
from default.webdriver_utilities.pre_drivers import pgdas_driver

class CriaTodasPastas(NewSetPaths, ExcelToData):

    def __init__(self):
        """
        :param compt_file: from GUI

        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd

        from autoesk_main.pgdas_fiscal_oesk.relacao_nfs import tres_valores_faturados
        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual

        sh_names = 'sem_mov', 'G5_ISS', 'G5_ICMS'
        compt = super().get_compt_only().replace('-', '/')
        excel_file_name = super().excel_file_path()

        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path
            mshExcelFile = pd.ExcelFile(excel_file_name)

            msh = mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = mshExcelFile.parse(
                sheet_name=str(sh_name), dtype=col_str_dic)
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
                if CLIENTE == '':
                    break
                self.now_person = CLIENTE
                self.client_path = self.files_pathit(CLIENTE)
                print(CLIENTE)

# CriaTodasPastas()