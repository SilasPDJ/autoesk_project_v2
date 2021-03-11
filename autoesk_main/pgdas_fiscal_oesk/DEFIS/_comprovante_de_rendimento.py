import os
from default.settings import SetPaths
from default.data_treatment import ExcelToData
from default.data_treatment import transformers as tfms


class Defis(SetPaths, ExcelToData):
    def __init__(self, compt_file=None):
        """
        :param compt_file: from GUI

        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd

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

            for i, CNPJ in enumerate(after_READ['CNPJ']):
                # ####################### A INTELIGENCIA EXCEL ESTÁ SEM OS SEM MOVIMENTOS NO MOMENTO
                _cliente = after_READ['Razão Social'][i]
                _ja_declared = after_READ['Declarado'][i].upper().strip()
                _cod_sim = after_READ['Código Simples'][i]
                _cpf = after_READ['CPF'][i]
                _cert_or_login = after_READ['CERTORLOGIN'][i]

                # Dirfis exclusivos search
                _dirf_sch = after_READ['DIRF'][i]
                print(_dirf_sch)
                if _cliente == '':
                    break

                if _ja_declared not in ['S', 'OK', 'FORA']:
                    # ############################################################################################ ↓
                    # self.client_path = self._files_path_defis(_cliente, tup_path=(COMPT, excel_file_name))
                    if _dirf_sch == '-' or '-' in _dirf_sch or _dirf_sch.strip() == '':
                        pdf_dirf = False
                    else:
                        self.client_path = self._files_path_defis(_cliente, tup_path=(COMPT, excel_file_name))

                        pdf_dirf = self.os_walk__get_dirfs(_dirf_sch)
                        self.os_walk__get_dirfs(_dirf_sch)
                        __client_path = self.client_path
                        # print(pdf_dirf)
                        if pdf_dirf:
                            for img_file in tfms.pdf2jpg(pdf_dirf, self.client_path):
                                # input(__client_path)
                                dale = tfms.jpg2txt(img_file)
                                with open(img_file.replace('jpg', 'txt'), 'w') as ftext:
                                    ftext.write(dale)

                    # self.driver = pgdas_driver(__client_path)
                    # driver = self.driver
                    # super().__init__(driver)

    def os_walk__get_dirfs(self, searched_client, searched='Comprovante de rendimento.pdf'):
        """
        :param searched_client: searched_client_path
        :param searched:
        :return:
        """
        INITIAL_PATH = r'I:\OESK_CONTABIL'
        ano_dirf = str(self.y())

        for (dirpath, dirnames, filenames) in os.walk(INITIAL_PATH):
            if ano_dirf in dirnames:
                # get last part of folder name ↓↓↓
                the_client = os.path.basename(os.path.normpath(dirpath))
                if the_client == searched_client:

                    for (dp2, dn2, fn2) in os.walk(dirpath):
                        if ano_dirf in dp2:
                            for dp3, dn3, fn3 in os.walk(dp2):
                                if 'DIRF' in dp3:
                                    for file in os.listdir(dp3):
                                        if file == searched:
                                            # full_file_path
                                            returned = dp3 + f'\\{file}'
                                            break
                                    else:
                                        # full_file_path
                                        returned = False
                                    # now_command = f'explorer {dn2}'
                                    return returned


# input("\033[1;34mINPUT: FALTA LER O PDF AGORA, FAZENDO O SEU SCRAP\033[m")
Defis()
