from imports import Dirs, Now, os, sys, types


class NewSetPaths(Dirs, Now):
    import os
    # __name__ is always without extension, could be "__main__"
    # __file__ prints file path
    main_path = os.path.dirname(os.path.realpath(__file__))
    main_path += '\with_titlePATH.txt'
    # Dirs.pathit

    @classmethod
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
            returned = cls.select_path_if_not_exists(self=NewSetPaths)
        finally:
            return returned

    def select_path_if_not_exists(self, some_message="SELECIONE ONDE ESTÃO SUAS PASTAS.", savit=main_path):
        """[summary]
        Args:
            some_message (str, optional): []. Defaults to "SELECIONE ONDE ESTÃO SUAS PLANILHAS".
            savit (str, optional): customizable, where to save the info
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
                wf = open(savit, 'w')
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

    @ classmethod
    def files_pathit(cls, pasta_client, insyear=None, ano=None):
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
        compt = insyear
        if ano is None:
            # ano = ''.join([insyear[e+1:] for e in range(len(insyear)) if insyear[e] not in '0123456789'])
            ill_split = ''.join([v for v in compt if v not in '0123456789'])
            mes, ano = compt.split(ill_split)
            try:
                int(ano)
            except ValueError:
                print(f'if ano is None split ainda não encontrado,\n    ano = ano mês anterior')
                ano = date(cls.y(), cls.m(), 1) - du_rl.relativedelta(months=1)
                # Se ele não achar o ano vindo do split...

        excel_file_name = cls.getset_folderspath()
        # print(insyear, excel_file_name)
        __path = excel_file_name
        path_final = [*str(__path).split('\\'),
                      ano, insyear, pasta_client]
        salva_path = Dirs.pathit(*path_final)
        return salva_path

    def first_and_last_day_compt(self, insyear=None, sep='/'):
        """
        ELE JÁ PEGA O ANTERIOR MAIS PROX
        :param str insyear:(competencia or whatever). Defaults then call cls.get_compt_only() as default
        :param sep: separates month/year
        # É necessario o will_be pois antes dele é botado ao contrário
        # tipo: 20200430
        # ano 2020, mes 04, dia 30... (exemplo)
        :return: ÚLTIMO DIA DO MES
        """
        from datetime import date, timedelta
        from dateutil.relativedelta import relativedelta

        if insyear is None:
            insyear = self.get_compt_only()

        compt = insyear
        ill_split = ''.join([v for v in compt if v not in '0123456789'])
        mes, ano = compt.split(ill_split)

        mes, ano = int(mes), int(ano)
        #  - timedelta(days=1)
        # + relativedelta(months=1)

        last_now = date(ano, mes, 1) + relativedelta(months=1)
        last_now -= timedelta(days=1)
        first_now = date(ano, mes, 1)

        z, a = last_now, first_now
        br1st = f'{a.day:02d}{sep}{a.month:02d}{sep}{a.year}'
        brlast = f'{z.day:02d}{sep}{z.month:02d}{sep}{z.year}'
        print(br1st, brlast)
        return br1st, brlast

    def files_get_anexos_v3(self, client, file_type='pdf', compt=None, upload=False):
        """
        :param client: nome da pasta onde estão os arquivos organizados por data dd-mm-yyyy
        :param file_type: file annexed type
        :param compt: 10-2020; 02-2019 etc
        :param upload: False -> email it! True: upload it!
        :return: pdf_files or whatever

        # _files_path
        """
        from email.mime.application import MIMEApplication
        if compt is None:
            compt = self.get_compt_only()
        path = self.files_pathit(client, compt)
        pdf_files = list()
        # Lucas Restaurante

        dir_searched_now = path
        list_checked_returned = [os.path.join(dir_searched_now, fname)
                                 for fname in os.listdir(dir_searched_now) if fname.lower().endswith(file_type)]

        for fname in list_checked_returned:
            if upload:
                file_opened = MIMEApplication(open(fname, 'rb').read())
                file_opened.add_header('Content-Disposition', 'attachment', filename=fname)
                pdf_files.append(file_opened)
            else:
                pdf_files.append(f'{fname}')
        return pdf_files

    @staticmethod
    def get_last_business_day_of_month(month=None, year=None):
        from calendar import monthrange
        from datetime import datetime
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year

        init = monthrange(year, month)
        ultimo_day = init[1]
        business_date = datetime(year, month, ultimo_day)

        weekday = business_date.weekday()
        while weekday > 4:
            now_day = business_date.day
            business_date = business_date.replace(day=now_day - 1)
            weekday = business_date.weekday()
        returned = business_date.day

        returned -= 1 if month == 12 else returned
        return returned

# NewSetPaths().files_get_anexos_v3(r'Dívidas_Simples_CRB', compt='01-2021')
