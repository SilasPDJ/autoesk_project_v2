# from default import NewSetPaths, ExcelToData

from imports import EmailExecutor
from _new_set_json import MakeJson
import json


class SendDividas(EmailExecutor, MakeJson):
    def __init__(self, compt=None):
        """
        :param compt: mm-yyyy; mm/yyyy
        """
        import pandas as pd
        self.venc_boletos = self.vencimento_dividas()
        print('VENCIMENTO DÍVIDAS: ', self.venc_boletos)
        here_sh_names = ['_Dívidas']

        if compt is None:
            compt = super().get_compt_only()
        excel_file_name = super().excel_file_path()
        MakeJson.__init__(self, compt, excel_file_name, here_sh_names)
        EmailExecutor().__init__()

        for counter, each_dict in enumerate(self.read_from_json()):
            counter = str(counter)
            custom_values = list(each_dict.values())
            _cliente, _cnpj, _cpf, _ja_declared, _tipo_divida = self.any_to_str(*custom_values[:5])
            now_email = each_dict['email']
            _ja_foi_env = each_dict['envio'].upper().strip()
            _now_spreadsheet = each_dict["spreadsheet"]


            if _ja_declared in ['S', 'OK', 'FORA'] and _ja_foi_env not in ['S', 'OK']:
                print(now_email)
                # print(f'VALOR: {VALOR}')
                print(f'_cliente: {_cliente}')
                # input(self.set_compt_only(-11, 1, past_only=False))
                # FUNCIONA PRA CONTAR PRO MES Q VEM VALIDADO COM ANO

                dividas_pdf_files = self.files_get_anexos_v3("Dívidas_Simples_" + _cliente, file_type='pdf',
                                                             compt=compt, upload=False)
                qtd_arquivos = len(dividas_pdf_files)
                mail_header = f"com vencimento previsto para o dia: {self.venc_boletos.replace('-', '/')}"
                mail_header = f"Parcelamentos, {'boleto' if qtd_arquivos == 1 else 'boletos'} {mail_header}"
                print('titulo: ', mail_header)

                message = self.mail_dividas_msg(_cliente, _cnpj, len(dividas_pdf_files))
                # print(message)
                das_message = self.write_message(message)

                # # 'silsilinhas@gmail.com'
                now_email = 'silsilinhas@gmail.com'
                try:
                    # self.main_send_email(now_email, mail_header, das_message, dividas_pdf_files)
                    each_dict['envio'] = 'S'
                    for atualiza in self.dumps_from(_now_spreadsheet, get_instead=True):
                        atualiza['envio'][counter] = 'S'
                        self.dump_json(atualiza, self.dumps_from__now_path)
                        with open(self.dumps_from__now_path, encoding='utf-8') as dfnp:
                            data = dfnp.read()
                            data_save = json.loads(data,)
                            data_save = pd.DataFrame(data_save, dtype=str)

                            data_save.to_excel(f'pgdas_fiscal_oesk/data_clients_files/output-{_now_spreadsheet}.xlsx',
                                               encoding='utf-8-sig')
                    input('passou')

                except Exception as e:
                    raise e

                    # input('test')

                ""
                # ###########################
                # Vou registrar o each_dict no b
                # ###########################

                """a partir do terceiro argumento, só há mensagens attachedas"""

    def mail_dividas_msg(self, client, cnpj, main_anx_len=0):

        colours = self.zlist_colours_emails()
        red, blue, money, parc_style = \
            self.wcor(colours[114]), self.wcor('blue'), ' style="background-color:yellow; color:green"', \
            'style="background-color:yellow; color:red"'
        ntt = self.tag_text
        inso = self.inside_me_others
        # posso inso dentro de inso sem problema
        full_mensagem = f"""
{ntt('h1', f'{self.hora_mensagem()}, {client}!')}

{inso(ntt('h2', 'Seguem anexados:'), inso(ntt('p', '->'),ntt('span '+parc_style, f' {main_anx_len} Parcelamentos pendentes'), 
                                          ntt('h2', '-> A data de vencimento é igual para todos os boletos anexados')))
        if main_anx_len > 1 else inso(ntt('h2', 'Segue anexado:'), inso(ntt('p', '-> '),ntt('span'+red, 'Parcelamento pendente'))) 
        if main_anx_len > 0 else ntt('h3'+money, 'NÃO HÁ PARCELAMENTOS PENDENTES OU ANEXADOS')}


<div>
Este e-mail é automático. Por gentileza, cheque o nome e o CNPJ ({ntt('span'+red, cnpj)}) antes de pagar o documento.
<h4>Caso haja qualquer conflito, responda sem hesitar esta mensagem neste e-mail.</h4>
<h4>Todas as declarações são e continuarão sendo feitas minuciosamente.</h4>
</div>
{ntt('h2'+blue,'ATT, Oesk Contábil')}
        """
        return full_mensagem

    def get_dividas_vencimento(self, compt_setted=None):
        """
        :param compt_setted: from dividas, compt setted

        :return: data vencimento formato dia-mes-ano
        """

        mes, ano = compt_setted.split('-')
        mes, ano = int(mes), int(ano)
        # caso precise da compt setted
        venc_dividas_day = self.get_last_business_day_of_month()
        # é possível data

        venc = f'{venc_dividas_day:02d}-{self.m():02d}'
        return venc

    def dividas_mime_img(self, dividas_png_files: list):
        from email.mime.image import MIMEImage
        imgsimgs = []
        for png in dividas_png_files:
            print(png)
            with open(png, 'rb') as pf:
                img = MIMEImage(pf.read())
                imgsimgs.append(img)
        return imgsimgs
# depois o send email vai emglobar tudo que ta em package init_email... # no projeto final


SendDividas()
