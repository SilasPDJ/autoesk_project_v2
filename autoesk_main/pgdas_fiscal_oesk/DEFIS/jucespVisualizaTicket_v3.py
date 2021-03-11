import os
from time import sleep
from default.settings import SetPaths
from default.data_treatment import ExcelToData

from default.data_treatment import transformers as tfms


# pdf2jpg()
# jpg2txt()


class VisualizaTicket(SetPaths, ExcelToData):
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

            for i, CNPJ in enumerate(after_READ['CNPJ']):
                # ####################### A INTELIGENCIA EXCEL ESTÁ SEM OS SEM MOVIMENTOS NO MOMENTO
                _cliente = after_READ['Razão Social'][i]
                _ja_declared = after_READ['Declarado'][i].upper().strip()
                _cod_sim = after_READ['Código Simples'][i]
                _cpf = after_READ['CPF'][i]
                _cert_or_login = after_READ['CERTORLOGIN'][i]

                # Dirfis exclusivos search
                _dirf_sch = after_READ['DIRF'][i]

                self.dirf_nome = _dirf_sch if _dirf_sch != '-' else _cliente

                if _cliente == '':
                    break

                if _ja_declared not in ['S', 'OK', 'FORA']:
                    # ############################################################################################ ↓
                    # self.client_path = self._files_path_defis(_cliente, tup_path=(COMPT, excel_file_name))
                    self.client_path = self._files_path_defis(_cliente, tup_path=(COMPT, excel_file_name))

                    file_pdf = 'VisualizaTicket.pdf'

                    dir_searched_now = self.client_path
                    file_src = ''.join([os.path.join(dir_searched_now, fname) for fname in os.listdir(dir_searched_now) if
                                        fname == file_pdf])
                    #  file_searched = os.path.basename(os.path.normpath(file_searched_path))
                    if file_src != '':
                        now_txts = tfms.pdf2txt(file_src)
                        # Consegui finalmente essa maravilha...
                        self.here_scrap(now_txts)



    def here_scrap(self, __txt):

        palavras_valiosas_socios = ['TITULAR / SÓCIOS / DIRETORIA', '5 ÚLTIMOS ARQUIVAMENTOS', 'FIM DAS INFORMAÇÕES PARA NIRE']
        PVS = palavras_valiosas_socios.copy()

        USED = __txt
        try:
            final = USED.index(PVS[1])
        except ValueError:
            final = USED.index(PVS[2])

        inicio = USED.index(PVS[0])

        if inicio > final:
            # print(f'\033[1;31m{inicio}:{final}\033[m')
            final *= 2
        USED = USED[inicio: final]

        # ############################################## caças responsivas
        # ####### caça CPFs
        cpfs = []
        for e, _valor in enumerate(USED.split()):

            cpf = self.str_with_mask(_valor, '000.000.000-00')
            if cpf:
                cpfs.append(cpf)
        cotas = []
        for v1, v2 in zip(range(0, len(USED)), range(20, len(USED))):
            if v2 == len(USED):
                break
            if '$'.lower() in USED[v1].lower():
                val = USED[v1:v2]
                val = val[:val.index(',')+3]

                # cotas.add(val)
                cotas.append(val)
        ######### caça nome

        elif1 = [f.split()[1] for f in cotas]
        elif1 = [f.replace('.', '').replace(',', '.') for f in elif1]
        elif1 = [float(f) for f in elif1]

        if not cotas or not cpfs:
            """
            print('\033[1;31mNot Cotas\033[m')
            cpfs = []
            for e, cpf in enumerate(__txt.split()):
                cpf = self.str_with_mask(cpf, '000.000.000-00')
                if cpf:
                    cpfs.append(cpf)

            cpfs = list(dict.fromkeys(cpfs))
            input(cpfs)
            """
        elif '5' in str(sum(elif1)):
            # print(f'\033[1;33m A cota de {self.dirf_nome} está errada, pois a soma é: {sum(elif1)}\033[m')
            pass
        else:
            print(self.dirf_nome)
            input(USED.split('\n\n')[1])
            print(cotas)
            print(cpfs)
        print('-'*30)
        # input(socios)
        # input(cotas)


VisualizaTicket()
