# from default import NewSetPaths, ExcelToData

from imports import EmailExecutor
from _new_set_json import MakeJson


class PgDasmailSender(EmailExecutor, MakeJson):
    def __init__(self, fname, compt=None):
        """
        :param fname: nome do json
        :param compt: compt...
        """
        from default.interact import press_keys_b4, press_key_b4

        self.venc_das = self.vencimento_das()
        # sh_names = 'sem_mov', 'G5_ISS', 'G5_ICMS'
        if compt is None:
            compt = super().get_compt_only()
        excel_file_name = super().excel_file_path()
        MakeJson.__init__(self, compt, excel_file_name)

        mail_header = f"Fechamentos para apuração do imposto PGDAS, competência: {compt.replace('-', '/')}"
        print('titulo: ', mail_header)
        for each_dict in self.read_from_json():
            for k, v in each_dict.items():
                print(k, v)

            custom_values = list(each_dict.values())
            _cliente, _cnpj, _cpf, _cod_simples, _ja_declared = self.any_to_str(*custom_values[:5])
            print(_cliente, _cnpj, _cpf, _cod_simples, _ja_declared)
            _icms_or_iss = each_dict['spreadsheet']

            try:
                _valor = self.trata_money_excel(each_dict['Valor'])
            except KeyError:
                _valor = self.trata_money_excel('zerou')
            try:
                now_email = each_dict['email']
                _ja_foi_env = each_dict['envio'].upper().strip()
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

                    das_anx_files = self.files_get_anexos_v3(_cliente, file_type='pdf', compt=compt)
                    # self.main_send_email(now_email, mail_header, das_message, das_anx_files)
                    input('security, silsilinhas')
                    self.main_send_email('silsilinhas@gmail.com', mail_header, das_message, das_anx_files)
                    """a partir do terceiro argumento, só há mensagens attachedas"""

                    print('Enviado...')

    def mail_pgdas_msg(self, client, cnpj, tipo_das, valor):
        path_colours = os.path.dirname(__file__)
        path_colours = os.path.join(path_colours, 'default/data_treatment')
        colours = self.load_json(path_colours+'/zlist_colours.json')

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

import os
fname = f'{os.path.dirname(__file__)}/pgdas_fiscal_oesk/data_clients_files/example_iss.json'

PgDasmailSender(fname)
