from imports import EmailExecutor
# from smtp_project import *


class SendDividas(EmailExecutor):

    def __init__(self):
        import pandas as pd
        super().__init__()

        # self.compt_setted = self.get_compt_only(-11, 1, past_only=False)

        # venc_dividas = self.das_venc_data()[3]



        # self.venc_boletos = self.get_dividas_vencimento(self.compt_setted)
        self.venc_boletos = self.vencimento_dividas()

        print('VENCIMENTO DÍVIDAS: ', self.venc_boletos)

        sh_names = ['_Dívidas']

        excel_compt, excel_file_name = self.set_get_compt_file(-1)
        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path
            mshExcelFile = pd.ExcelFile(excel_file_name)
            # input(mshExcelFile.sheet_names)
            msh = mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = mshExcelFile.parse(sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            self.after_READ = self.readnew_lista(READ, False)
            after_READ = self.after_READ

            for i, CNPJ in enumerate(after_READ['CNPJ']):
                # ####################### A_Main INTELIGENCIA EXCEL ESTÁ SEM OS SEM MOVIMENTOS NO MOMENTO

                CLIENTE = after_READ['Razão Social'][i]
                JA_DECLARED = after_READ['Declarado'][i].upper().strip()
                # CodSim = after_READ['Código Simples'][i]
                # CPF = after_READ['CPF'][i]
                # icms_or_iss = sh_names[sh_names.index(sh_name)]
                JA_FOI_ENV = after_READ['envio'][i].upper().strip()
                now_email = after_READ['email'][i]

                if JA_DECLARED in ['S', 'OK', 'FORA'] and JA_FOI_ENV not in ['S', 'OK']:
                    print(now_email)
                    # print(f'VALOR: {VALOR}')
                    print(f'CLIENTE: {CLIENTE}')
                    # input(self.set_compt_only(-11, 1, past_only=False))
                    # FUNCIONA PRA CONTAR PRO MES Q VEM VALIDADO COM ANO

                    dividas_pdf_files = self.files_get_anexos_v3("Dívidas_Simples_" + CLIENTE, file_type='pdf',
                                                                 compt=(excel_compt, excel_file_name), upload=True)
                    # o arg do param em wexplorer_tup (0) significa o mes atual.
                    dividas_png_files = self.files_get_anexos_v3("Dívidas_Simples_" + CLIENTE, file_type='png',
                                                                 compt=(excel_compt, excel_file_name), upload=True)
                    # Na dúvida, melhor settar...
                    # após anexar...

                    qtd_arquivos = len(dividas_pdf_files)
                    mail_header = f"com vencimento previsto para o dia: {self.venc_boletos.replace('-', '/')}"
                    mail_header = f"Parcelamentos, {'boleto' if qtd_arquivos == 1 else 'boletos'} {mail_header}"
                    print('titulo: ', mail_header)

                    list_imgs = self.dividas_mime_img(dividas_png_files)
                    message = self.mail_dividas_msg(CLIENTE, CNPJ, len(dividas_pdf_files))
                    print(message)
                    das_message = self.write_message(message)

                    dividas_files = dividas_pdf_files + list_imgs
                    self.main_send_email(now_email, mail_header, das_message, dividas_pdf_files)
                    # 'silsilinhas@gmail.com'
                    # self.main_send_email('silsilinhas@gmail.com', mail_header, das_message, dividas_files)

                    """a partir do terceiro argumento, só há mensagens attachedas"""

    def mail_dividas_msg(self, client, cnpj, main_anx_len=0):

        colours = self.load_json('zlist_colours.json')
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
