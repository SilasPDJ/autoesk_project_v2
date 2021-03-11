from imports import Dirs, Now, os, sys, types


class NewSetPaths(Dirs, Now):
    import os
    # __name__ is always without extension, could be "__main__"
    # __file__ prints file path
    main_path = os.path.dirname(os.path.realpath(__file__))
    main_path += '\with_titlePATH.txt'
    # Dirs.pathit

    @ classmethod
    def getset_folderspath(cls):
        """Seleciona onde estão as pastas e planihas

        Returns:
            [type]: [description]
        """
        # filepath = os.path.realpath(__file__)
        # os.path.dirname(filepath)
        returned = False
        try:
            with open(cls.main_path) as f:
                returned = f.read()
        except FileNotFoundError:
            FileExistsError('WITH TITLE PATH NOT EXISTENTE ')
            returned = cls.select_path_if_not_exists()
        finally:
            return returned

    def select_path_if_not_exists(self, some_message="SELECIONE ONDE ESTÃO SUAS PASTAS.", registrer=main_path):
        """[summary]
        Args:
            some_message (str, optional): []. Defaults to "SELECIONE ONDE ESTÃO SUAS PLANILHAS".
            register (str, optional): customizable, where to save the info
        Returns:
            [type]: [description]
        """
        from tkinter import Tk, filedialog, messagebox
        root = Tk()
        root.withdraw()
        root = Tk()
        root.withdraw()
        # sh_management = SheetPathManager(file_with_name)
        way = None
        while way is None:
            way = filedialog.askdirectory(title=some_message)
            if len(way) <= 0:
                way = None
                resp = messagebox.askokcancel(
                    'ATENÇÃO!', message='Favor, selecione uma pasta ou clique em CANCELAR.')
                if not resp:
                    return False
            else:
                wf = open(registrer, 'w')
                wf.write(way)
                root.quit()
                return way

    @ classmethod
    def get_compt_only(cls, m_cont=-1, y_cont=0, past_only=True, sep='-'):
        from datetime import date
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta
        month = cls.m()
        year = cls.y()

        now_date = date(year, month, 1)

        if past_only:
            m_cont = m_cont * (-1) if m_cont > 0 else m_cont
            y_cont = y_cont * (-1) if y_cont > 0 else y_cont
            # force to be negative

        now_date = now_date + relativedelta(months=m_cont)
        now_date = now_date + relativedelta(years=y_cont)
        month, year = now_date.month, now_date.year
        compt = f'{month:02d}{sep}{year}'
        return compt

    @ classmethod
    def files_path(cls, pasta_client, insyear=None, ano=None):
        from imports import relativedelta as du_rl
        from datetime import date

        """[summary]

        Args:
            pasta_client (str): client folder name
            insyear (str): inside year (competencia or whatever). Defaults then call cls.get_compt_only() as default
            ano (str,[optional]): year folder. Defaults to None.

        Returns:
            [type]: [description]
        """
        insyear = cls.get_compt_only() if insyear is None else insyear

        if ano is None:
            ano = ''.join([insyear[e+1:] for e in range(len(insyear)) if insyear[e] not in '0123456789'])
            try:
                int(ano)
            except ValueError:
                print(f'if ano is None split ainda não encontrado,\n    ano = ano mês anterior')
                ano = date(cls.y(), cls.m(), 1) - du_rl.relativedelta(months=1)
                # Se ele não achar o ano vindo do split...

        excel_file_name = cls.getset_folderspath()
        # print(insyear, excel_file_name)
        defis_path = excel_file_name

        defis_path_final = [*str(defis_path).split('\\'),
                            ano, insyear, pasta_client]
        salva_path = Dirs.pathit(*defis_path_final)
        return salva_path

    def excel_file_path(self, excelfolder='__EXCEL POR COMPETENCIAS__', fncompt=None, ext="xlsx"):
        """return excel path inside always self.getset_folderpath()

        Args:
            excelfolder (str, optional): excel folder. Defaults to '__EXCEL POR COMPETENCIAS__'.
            fncompt (str, optional): filename. Defaults to None (compt).
            ext (str, optional): filename suffix
        """
        if fncompt is None:
            fncompt = self.get_compt_only()
        fncompt = os.path.join(fncompt+"."+ext)

        main_path = self.getset_folderspath()
        this_path = self.pathit(main_path, excelfolder, fncompt)
        return this_path

