from default.data_treatment import ExcelToData
from _new_set_paths import NewSetPaths


class Fantasia(NewSetPaths, ExcelToData):

    def __init__(self, compt=None):
        """
        :param compt: from GUI

        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        from default.webdriver_utilities.pre_drivers import pgdas_driver
        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual

        sh_names = 'sem_mov', 'G5_ISS', 'G5_ICMS'
        if compt is None:
            compt = super().get_compt_only()

        excel_file_name = super().excel_file_path()



        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path
            mshExcelFile = pd.ExcelFile(excel_file_name)

            msh = mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = mshExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            self.after_READ = self.readnew_lista(READ, False)
            after_READ = self.after_READ
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


