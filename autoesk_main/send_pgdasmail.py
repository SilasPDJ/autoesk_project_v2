from smtp_project import EmailExecutor
from default import SetPaths, ExcelToData
# from smtp_project import *



class PgDasmailSender(EmailExecutor):

    def __init__(self, fname, compt_file: tuple):
        """
        :param fname: nome do json
        :param compt_file: compt_file...
        """
        from smtp_project.init_email import JsonDateWithImprove as Jj
        from default.interact import press_keys_b4, press_key_b4
        super().__init__()

        self.venc_das = self.vencimento_das()
        # sh_names = 'sem_mov', 'G5_ISS', 'G5_ICMS'

        if compt_file is None:
            # compt, excel_file_name = self.get_atual_compt_set(1)
            compt_file = self.compt_and_filename()
            compt, excel_file_name = compt_file
        else:
            compt, excel_file_name = compt_file
        # posso mudar os argumentos de get_atual_competencia, ele já tem padrão, mas coloquei pra lembrar
        mail_header = f"Fechamentos para apuração do imposto PGDAS, competência: {compt.replace('-', '/')}"
        print('titulo: ', mail_header)
        # é o meu teste
        json_file = Jj.load_json(fname)
        # for eid in range(len(json_file.keys()))
        for eid in json_file.keys():
            after_json = self.readnew_lista_v_atual(json_file[eid])
            # input(after_json)
            custom_values = [v.values() for v in json_file[eid]]
            _cliente, _cnpj, _cpf, _cod_simples, _ja_declared = self.any_to_str(*custom_values[:5])

            _icms_or_iss = after_json['spreadsheet']
            try:
                _valor = self.trata_money_excel(after_json['Valor'])
            except KeyError:
                _valor = self.trata_money_excel('zerou')
            try:
                now_email = after_json['email']
                _ja_foi_env = after_json['envio'].upper().strip()
            except KeyError:
                print(f'CLIENTE {_cliente}\033[1;31m NÃO\033[m tem email')
                _ja_foi_env = 'OK'
            else:
                if now_email == '':
                    print('wtf')
                elif _ja_declared in ['S', 'FORA'] and _ja_foi_env not in ['S', 'OK']:
                    print(now_email)
                    print(f'VALOR: {_valor}')
                    print(f'CLIENTE: {_cliente}')
                    message = self.mail_pgdas_msg(_cliente, _cnpj, _icms_or_iss, _valor)
                    # input(message)
                    das_message = self.write_message(message)

                    das_anx_files = self.files_get_anexos(_cliente)
                    self.main_send_email(now_email, mail_header, das_message, das_anx_files)
                    # self.main_send_email('silsilinhas@gmail.com', mail_header, das_message, das_anx_files)
                    """a partir do terceiro argumento, só há mensagens attachedas"""

                    print('Enviado...')

    def mail_pgdas_msg(self, client, cnpj, tipo_das, valor):

        colours = self.load_json('zlist_colours.json')
        red, blue, money = self.wcor(colours[114]), self.wcor('blue'), 'style="background-color:yellow; color:green"'
        ntt = self.tag_text
        inso = self.inside_me_others
        inside_me = ntt(f'strong'+blue, 'inside meeeeeeeee')
        # {inso(ntt('h2'+blue, f"{self.hora_mensagem()}, "), ntt("span"+blue,f"{client}!"))}
        # {inso(ntt('h3' + blue, f'CNPJ: '), ntt('span' + red, cnpj))}
        # {ntt('h3', f'CNPJ: {cnpj}')}
        full_mensagem = f"""
{ntt('h2', f'{self.hora_mensagem()}, {client}!')}
{ntt('h3', 'Seguem anexados:')}
<h3> 
-> DAS ({ntt('span'+blue,'ISS' if 'ISS' in tipo_das.upper() else 'ICMS')})
sobre faturamento de {ntt('span style="background-color:yellow; color:green"', 'R$ '+valor)}
</h3>

<h3> 
    -> Protocolos e demonstrativos respectivos
            {
    f'''
    <h3>
        -> A data de vencimento do boleto é: {ntt('span' + red, self.venc_das)}
    </h3>
    <h4> 
        -> O arquivo do boleto contém as iniciais "{ntt('span'+red,'PGDASD-DAS')}"
    </h4>
    '''
            if valor != 'SEM VALOR DECLARADO' else f"<h3>{ntt('span'+red,'NÃO')} há boleto a pagar.</h3>"
            }
<hr>
</h3> 


<div>
Este e-mail é automático. Por gentileza, cheque o nome e o CNPJ ({ntt('span'+red, cnpj)}) antes de pagar o documento.
<h4>Caso haja qualquer conflito, responda sem hesitar esta mensagem neste e-mail.</h4>
<h4>Todas as declarações são e continuarão sendo feitas minuciosamente.</h4>
</div>
{ntt('h2'+blue,'ATT, Oesk Contábil')}

        """
        return full_mensagem
