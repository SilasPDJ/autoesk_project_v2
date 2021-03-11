class SheetPathManager:

    modificador_file = r'C:\_SIMPLES\MEXENDO.xlsx'

    def new_xlsxcompt_from_padrao_if_not_exists(self, compt_and_filename):
        """
        :return: CREATE XLSX FILE IF NOT EXISTS
        """
        compt, excel_file_name = compt_and_filename
        from pandas import read_excel

        def gen_or_read_plan():
            try:
                read_excel(excel_file_name)
            except FileNotFoundError:
                from shutil import copy2

                copy2(default_file, excel_file_name)
                copy2(default_file, self.modificador_file)

        plan = 'default_oesk'

        default_file = excel_file_name.replace('\\', '/')
        default_file = default_file.split('/')[:-1]
        default_file = '/'.join(default_file) + f'/{plan}.xlsx'

        try:
            read_excel(default_file)
            gen_or_read_plan()
        except FileNotFoundError:
            raise FileNotFoundError(f'plan="{plan}" file não existente')
        except PermissionError:
            # somente o file default, caso eu esteja editando algo...
            gen_or_read_plan()

    @classmethod
    def save_after_changes(cls, the_famous_tup):
        from shutil import copy2
        import os

        compt, excel_file_name = the_famous_tup

        os.system(cls.modificador_file)

        copy2(cls.modificador_file, excel_file_name)
        print(f'{excel_file_name} atualizando por {cls.modificador_file}')
