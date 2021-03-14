from imports import HasJson
import pandas as pd

import os
import json


class MakeJson(HasJson):

    json_path = os.path.dirname(__file__)
    json_path += '/pgdas_fiscal_oesk/data_clients_files/'

    def __init__(self, compt, excel_file_name, shnames):
        from default.webdriver_utilities.pre_drivers import pgdas_driver
        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual
        self.compt = compt
        self.excel_file_name = excel_file_name
        self.__mshExcelFile = pd.ExcelFile(self.excel_file_name)
        self.__shnames = shnames



        """
        for each_dict in self.read_from_json():
            for k, v in each_dict.items():
                print(k, v)
        """
    def every_shexcel_read(self):
        for sh_name in self.__mshExcelFile.sheet_names:
            msh = self.__mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = self.__mshExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
            yield msh, sh_name

    def dumps_from(self, *many_searched, equal_to=True, get_instead=False):
        """
        :param many_searched: ]
        :param equal_to: True => if _ == shname; False => if _ in shname
        :param get_instead: True => returns the json str; False => dumps Json
        """
        for msh, shname in self.every_shexcel_read():

            self.dumps_from__now_path = self.json_path + f'-now-{shname}.json'
            now_path = self.dumps_from__now_path
            for _ in many_searched:
                if equal_to:
                    if _ == shname:
                        json_str = msh.to_json(force_ascii=False)
                        json_str = str(json_str).encode('utf8')
                        json_str = json.loads(json_str)
                        self.dump_json(json_str, now_path)
                        if get_instead:
                            yield json_str
                        else:
                            # self.dump_json(json_str, now_path)
                            self.dump_json(json_str, now_path)
                else:
                    if _ in shname:
                        json_str = msh.to_json(force_ascii=False)
                        json_str = str(json_str).encode('utf8')
                        json_str = json.loads(json_str)
                        self.dump_json(json_str, now_path)
                        if get_instead:
                            yield json_str
                        else:
                            self.dump_json(json_str, now_path)

    def get_as_dict(self):
        for sh_name_msh in self.__mshExcelFile.sheet_names:
            for sh_name in self.__shnames:
                if sh_name.strip() == sh_name_msh.strip():
                    now_path = self.json_path + f'-now-{sh_name}.json'
                    try:
                        with open(now_path) as fp:
                            finalmente = json.load(fp)

                    except (json.JSONDecodeError, FileNotFoundError):
                        pass
                    else:
                        self.dump_json(finalmente, now_path)
                        yield finalmente, sh_name

    def read_from_json(self):
        for dct, sh_name in self.get_as_dict():
            ir_len = [len(vv) for vv in list(dct.values())][0]

            new_client_dict = {}
            for cont in range(ir_len):
                for dict_dict, vals_dict in dct.items():
                    # dict_dict responsivo, pois não importa a ordem
                    for k, v in vals_dict.items():
                        k = int(k)
                        if k == cont:
                            new_client_dict[dict_dict] = str(v).strip()

                            # print(v)
                new_client_dict["spreadsheet"] = sh_name
                yield new_client_dict


    """
    def backup__read_b4save(self):
        for dct in self.get_as_dict():
            ir_len = [len(vv) for vv in list(dct.values())][0]
            for cont in range(ir_len):
                for dict_dict, vals_dict in dct.items():
                    # dict_dict responsivo, pois não importa a ordem
                    for k, v in vals_dict.items():
                        k = int(k)
                        if k == cont:
                            print(v)
    """
    """
    def backup__get_as_dict(self):
        for sh_name in self.__mshExcelFile.sheet_names:
            now_path = self.json_path + f'-now-{sh_name}.json'
            try:
                with open(now_path) as fp:
                    e = json.load(fp)
                    e = e.replace('\\', "")
                    null = ''
                    finalmente = eval(e)
                    yield finalmente, sh_name

            except FileNotFoundError:
                pass
    """
