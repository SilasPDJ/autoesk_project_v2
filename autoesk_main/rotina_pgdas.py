# dale
from imports import Keys, By, WebDriverWait, expected_conditions
from imports import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from imports import activate_window, press_key_b4

from imports import WDShorcuts, ExcelToData
from _new_set_paths import NewSetPaths
from imports import sleep, press_keys_b4

import pyautogui as pygui

import pandas as pd
from default.webdriver_utilities.pre_drivers import pgdas_driver

class PgdasAnyCompt(WDShorcuts, NewSetPaths, ExcelToData):

    def __init__(self):
        """
        :param compt_file: from GUI

        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd

        from autoesk_main.pgdas_fiscal_oesk.relacao_nfs import tres_valores_faturados
        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual


        sh_names = 'sem_mov', 'G5_ISS', 'G5_ICMS'


        intelligence_existence = self.intelligence_existence_done(
            'CERT_vs_LOGIN.xlsx')
        inteligence_db = {'CLIENT': [],
                          'CERT x LOGIN': []
                          }
        client_db_name = inteligence_db['CLIENT']
        cert_x_login = inteligence_db['CERT x LOGIN']
        cont_inteligence = -1

        compt = super().get_compt_only().replace('-', '/')
        excel_file_name = super().excel_file_path()

        for sh_name in sh_names:
            # agora eu posso fazer downloalds sem me preocupar tendo a variável path
            mshExcelFile = pd.ExcelFile(excel_file_name)

            msh = mshExcelFile.parse(sheet_name=str(sh_name))
            col_str_dic = {column: str for column in list(msh)}
            msh = mshExcelFile.parse(
                sheet_name=str(sh_name), dtype=col_str_dic)
            READ = self.le_excel_each_one(msh)
            self.after_READ = self.readnew_lista(READ, False)
            after_READ = self.after_READ

            # if sh_name not in 'sem_mov':
            print(cont_inteligence)
            print(f'cont inteligence plan {sh_name}')
            for i, CNPJ in enumerate(after_READ['CNPJ']):
                if 'G5' in sh_name:
                    cont_inteligence += 1
                # ####################### A INTELIGENCIA EXCEL ESTÁ SEM OS SEM MOVIMENTOS NO MOMENTO
                CLIENTE = after_READ['Razão Social'][i]
                JA_DECLARED = after_READ['Declarado'][i].upper().strip()
                CodSim = after_READ['Código Simples'][i]
                CPF = after_READ['CPF'][i]
                cont_ret_n_ret = i
                if CLIENTE == '':
                    break
                self.now_person = CLIENTE
                self.client_path = self.files_pathit(CLIENTE)


                # if not existe o arquivo my_wised_check_path_file -> no momento atual, existe
                def cria_inteligence():
                    print('Intelligence does not exist')
                    self.driver = pgdas_driver(self.client_path)

                    self.loga_cert()

                    # driver.set_window_position(-1055, 0)

                    # muda o client, no ECAC, é apenas uma função teste
                    element = self.intelligence_cnpj_test_element(CNPJ)

                    if element != '':

                        client_db_name.append(CLIENTE)
                        cert_x_login.append('loginComCodSim')
                        self.loga_simples(CNPJ, CPF, CodSim, CLIENTE)

                        print(f'Não preciso logar (if element != "") p/ criar inteligence. \n{CLIENTE}, '
                              f'por isso, break')

                        """
                        print(f'PRESSIONE ENTER P/ PROSSEGUIR, {CLIENTE}')
                        press_key_b4('enter')
                        while True:
                            try:
                                driver.implicitly_wait(5)
                                submit = driver.find_element_by_xpath("//input[@type='submit']").click()
                                break
                            except (NoSuchElementException, ElementClickInterceptedException):
                                print('sleeping, line 167. Cadê o submit?')
                                driver.refresh()

                        driver.implicitly_wait(5)
                        # implicitly_wait -> if element was already appeared, it'll not wait.
                        """

                    else:
                        client_db_name.append(CLIENTE)
                        cert_x_login.append('certificado')

                        print('SUCESSO, CERTIFICADO, ', CLIENTE)

                    # checa se a inteligencia não existe

                    try:
                        # driver.set_window_position(initial['x'], initial['y'])
                        driver.close()
                        # está ok o unbound me ajuda
                    except UnboundLocalError:
                        pass

                if isinstance(intelligence_existence, list) and JA_DECLARED not in ['S', 'OK', 'FORA'] and cont_inteligence >= 0:

                    __client_path = self.client_path
                    self.driver = pgdas_driver(__client_path)
                    driver = self.driver
                    super().__init__(driver)

                    driver.implicitly_wait(2)
                    # initial = driver.get_window_position()

                    driver.get('https://www.google.com.br')

                    print('ecac_or_simples')
                    try:
                        ecac_or_simples = intelligence_existence[cont_inteligence][1]
                    except IndexError:
                        print('FINISH')
                        break
                    # input(intelligence_existence[cont_inteligence][0]) # -> O NOME DO CLIENTE
                    my_new_3valores = tres_valores_faturados(self.client_path)
                    print(my_new_3valores, '----> my_new_3valores')

                    def return_valor():
                        if sh_names.index(sh_name) != 0:
                            if sh_names.index(sh_name) == 1:
                                if my_new_3valores:
                                    print(my_new_3valores[0])
                                    VALOR = [
                                        v for v in my_new_3valores[0].values()][0]
                                else:
                                    VALOR = after_READ['Valor'][i]
                                    if VALOR == '0':
                                        # or VALOR == '':
                                        VALOR = ''
                                        return VALOR

                            else:

                                VALOR = after_READ['Valor'][i]
                                if VALOR == '0':  # or VALOR == '':
                                    VALOR = ''
                                    return VALOR
                            if 'zerou' in str(VALOR).lower():
                                VALOR = ''
                            else:
                                if '.' not in str(VALOR):
                                    VALOR = f'{VALOR},00'
                                elif VALOR != '':
                                    VALOR = f'{float(VALOR):.2f}'
                                    VALOR = self.trata_money_excel(VALOR)
                                else:
                                    self.icms_prossegue = False  # não está em uso ainda

                        else:
                            VALOR = ''

                        print('VALOR BEFORE RETURN', VALOR)
                        return VALOR

                    VALOR = return_valor()

                    # Tratei o que dá pra fazer no certificado e o que não dá
                    if ecac_or_simples == 'certificado':
                        self.loga_cert()
                        # loga ECAC, Insere CNPJ
                        self.change_ecac_client(CNPJ)

                        self.current_url = driver.current_url
                        self.opta_script() if self.m() == 12 else None

                    else:

                        self.loga_simples(CNPJ, CPF, CodSim, CLIENTE)
                        self.current_url = driver.current_url
                        self.opta_script() if self.m() == 12 else None

                    # faz outras declaracoes se necessarias
                    """NÃO FUNCIONANDO CORRETAMENTE AINDA"""
                    # if self.check_make_pendencies():

                    self.compt_typist(compt)

                    self.DECLARA(compt, sh_names.index(sh_name),
                                 VALOR, my_new_3valores, cont_ret_n_ret)

                    print('CLOSE DRIVE EM 5 SEGS')
                    sleep(5)
                    driver.close()

                elif cont_inteligence == -1:
                    if JA_DECLARED not in ['S', 'OK']:

                        print('estou em sem movimento, vou arrumar ainda')

                        __client_path = self.client_path
                        self.driver = pgdas_driver(__client_path)
                        driver = self.driver
                        super().__init__(self.driver)
                        if CodSim != '-' and CodSim != '':

                            # Código simples existe # SEM MOVIMENTO
                            self.loga_simples(CNPJ, CPF, CodSim, CLIENTE)
                        else:

                            # Código sim inexistente
                            self.loga_cert()
                            self.change_ecac_client(CNPJ)
                        self.current_url = driver.current_url
                        self.opta_script() if self.m() == 12 else None

                        VALOR = 'zerou'
                        print('!!!ZEROU!!!')

                        self.compt_typist(compt)
                        # faz outras declaracoes se necessarias
                        if self.check_make_pendencies():
                            for compt_p2 in self.check_make_pendencies():
                                print(compt_p2, 'compt_p2')
                                self.compt_typist(
                                    compt_p2, '/'.join(driver.current_url.split('/')[:-1]))
                                self.DECLARA(compt_p2, sh_names.index(sh_name), '', False,
                                             cont_ret_n_ret)
                            self.compt_typist(
                                compt, '/'.join(driver.current_url.split('/')[:-1]))
                        else:
                            self.compt_typist(compt)

                        self.DECLARA(compt, sh_names.index(sh_name),
                                     VALOR, 'zerou', cont_ret_n_ret)

                elif not intelligence_existence:
                    # se não existir vai criar.
                    cria_inteligence()

                else:
                    print(
                        f'{CLIENTE} \nJA DECLARADO: {JA_DECLARED}\n-----------------')


    def intelligence_existence_done(self, file: str):
        """:param file: path_file_name, excel"""
        import os
        try:
            compt = super().get_compt_only()
            excel_file_name = super().excel_file_path()

            path_name = os.path.dirname(excel_file_name)
            path_name = os.path.join(path_name, file)

            inteligence_done = pd.read_excel(path_name, dtype=str)

            df = inteligence_done.to_numpy().tolist()
            for value in df:
                # print(value)
                pass
            return df
        except FileNotFoundError:

            print('intelligence will be done')
            return False

    def intelligence_cnpj_test_element(self, CNPJ):
        """:return: element

        create_inteligence, somente
        """
        driver = self.driver

        def elem_with_text(elem, searched):
            _tag = driver.find_element_by_xpath(
                f"//{elem}[contains(text(),'{searched.rstrip()}')]")
            return _tag

        self.tags_wait('html', 'span')
        sleep(5)
        # nextcl = elem_with_text("span", "Alterar perfil de acesso")
        # nextcl.click()
        driver.find_element_by_id('btnPerfil').click()
        # altera perfil e manda o cnpj
        self.tags_wait('label')

        cnpj = elem_with_text("label", "Procurador de pessoa jurídica - CNPJ")
        cnpj.click()
        sleep(.5)
        self.send_keys_anywhere(CNPJ)
        sleep(1)
        self.send_keys_anywhere(Keys.TAB)
        self.send_keys_anywhere(Keys.ENTER)
        sleep(1)
        # driver.find_element_by_class_name('access-button').click()
        # sleep(10)
        antigo = driver.current_url

        """I GOT IT"""
        # switch_to.frame...

        element = driver.find_element_by_class_name('mensagemErro').text
        element = element.strip()

        print(element)
        driver.get(
            'https://sinac.cav.receita.fazenda.gov.br/simplesnacional/aplicacoes/atspo/pgdasd2018.app/')
        return element

    def loga_simples(self, CNPJ, CPF, CodSim, CLIENTE):
        driver = self.driver
        driver.get(
            'https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')

        driver.get(
            'https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')
        while str(driver.current_url.strip()).endswith('id=60'):

            self.tags_wait('body')
            self.tags_wait('html')
            self.tags_wait('input')

            # driver.find_elements_by_xpath("//*[contains(text(), 'CNPJ:')]")[0].click()
            # pygui.hotkey('tab', interval=0.5)
            cpcp = driver.find_element_by_name(
                'ctl00$ContentPlaceHolder$txtCNPJ')
            cpcp.clear()
            cpcp.send_keys(CNPJ)

            cpfcpf = driver.find_element_by_name(
                'ctl00$ContentPlaceHolder$txtCPFResponsavel')
            cpfcpf.clear()
            cpfcpf.send_keys(CPF)

            cod = driver.find_element_by_name(
                'ctl00$ContentPlaceHolder$txtCodigoAcesso')
            cod.clear()
            cod.send_keys(CodSim)

            cod_caract = driver.find_element_by_id(
                'txtTexto_captcha_serpro_gov_br')
            btn_som = driver.find_element_by_id(
                'btnTocarSom_captcha_serpro_gov_br')
            sleep(2.5)
            btn_som.click()
            sleep(.5)
            cod_caract.click()
            print(f'PRESSIONE ENTER P/ PROSSEGUIR, {CLIENTE}')
            press_key_b4('enter')
            while True:
                try:
                    submit = driver.find_element_by_xpath(
                        "//input[@type='submit']").click()
                    break
                except (NoSuchElementException, ElementClickInterceptedException):
                    print('sleepin'
                          'g, line 167. Cadê o submit?')
                    driver.refresh()
                    sleep(5)
            sleep(5)

    def change_ecac_client(self, CNPJ):
        """:return: vai até ao site de declaração do ECAC."""
        driver = self.driver

        def elem_with_text(elem, searched):
            _tag = driver.find_element_by_xpath(
                f"//{elem}[contains(text(),'{searched.rstrip()}')]")
            return _tag

        self.tags_wait('html', 'span')
        sleep(5)
        # nextcl = elem_with_text("span", "Alterar perfil de acesso")
        # nextcl.click()
        btn_perfil = WebDriverWait(self.driver, 20).until(
            expected_conditions.presence_of_element_located((By.ID, 'btnPerfil')))
        self.click_ac_elementors(btn_perfil)
        # altera perfil e manda o cnpj
        self.tags_wait('label')

        cnpj = elem_with_text("label", "Procurador de pessoa jurídica - CNPJ")
        cnpj.click()
        sleep(.5)
        self.send_keys_anywhere(CNPJ)
        sleep(1)
        self.send_keys_anywhere(Keys.TAB)
        self.send_keys_anywhere(Keys.ENTER)
        sleep(1)
        # driver.find_element_by_class_name('access-button').click()
        # sleep(10)
        antigo = driver.current_url

        """I GOT IT"""
        # switch_to.frame...

        sleep(5)
        driver.get(
            'https://sinac.cav.receita.fazenda.gov.br/simplesnacional/aplicacoes/atspo/pgdasd2018.app/')
        sleep(2.5)
        driver.get(antigo)
        driver.get(
            'https://cav.receita.fazenda.gov.br/ecac/Aplicacao.aspx?id=10009&origem=menu')
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        sleep(2)
        while True:
            try:
                driver.find_element_by_xpath(
                    '//span[@class="glyphicon glyphicon-off"]').click()
                driver.refresh()
                break
            except ElementClickInterceptedException:
                print('---> PRESSIONE ESC PARA CONTINUAR <--- glyphicon-off intercepted')
                press_key_b4('esc')
            except NoSuchElementException:
                print('---> PRESSIONE ESC PARA CONTINUAR NoSuchElement glyphicon-off')
                press_key_b4('esc')
                driver.get(
                    'https://sinac.cav.receita.fazenda.gov.br/simplesnacional/aplicacoes/atspo/pgdasd2018.app/')
                driver.implicitly_wait(5)
                break
        sleep(3)
        driver.switch_to.default_content()
        """I GOT IT"""
        # chegou em todo mundo...

        driver.get(
            'https://sinac.cav.receita.fazenda.gov.br/simplesnacional/aplicacoes/atspo/pgdasd2018.app/')
        driver.implicitly_wait(5)

    def compt_typist(self, compt, came_from=None):
        """
        :param compt: competência, format: 'MM-YYYY'
        :param came_from: link where it comes from (multiples DECLARAÇÕES)
        :return: the unica declaração
        """
        driver = self.driver
        print('ÚNICA DECLARACAO')
        print('JA_DECLARED não -> prossegue')
        onlif = 'declaracao'
        if came_from:
            came_from = came_from.replace(
                came_from[0], '') if came_from[0] == '/' else came_from
            driver.get(came_from+'/'+onlif)
        else:
            if onlif not in driver.current_url:
                driver.execute_script(
                    f"""window.location.href += '{onlif}?clear=1'""")
        self.tags_wait('body', 'input')
        driver.implicitly_wait(10)
        try:
            periodo = self.webdriverwait_by_id('pa', 20)
            periodo.send_keys(compt)
            self.find_submit_form()

        except TimeoutException:
            pass

    def check_make_pendencies(self):
        driver = self.driver
        try:
            error_msg = driver.find_elements_by_class_name('errorMsg')
            if len(error_msg) == 2:
                compt_pendencias = error_msg[0].text
                # tam_ano = len(str(self.y()))
                compt_pendencias = compt_pendencias.split(':')
                compt_pendencias = ''.join(compt_pendencias).split(',')
                compt_pendencias = ''.join(compt_pendencias).split('.')
                compt_pendencias = ''.join(compt_pendencias).split(' ')
                compt_pendencias = [vv for vv in compt_pendencias if '/' in vv]
                compt_pendencias = [vv.replace('/', '-')
                                    for vv in compt_pendencias]
                print(compt_pendencias)

                if len(compt_pendencias) <= 11:
                    print(
                        '\033[1;31mPOR PADRÃO, check_make_pendencies irá zerar o valor...\033[m')
                    return compt_pendencias
                else:
                    return False
                    # raise IOError('FAZER COMPETÊNCIAS PASSADAS...')

        except NoSuchElementException as e:
            raise e

    def DECLARA(self, compt, sheet_id, valor_declarado, my_new_3valores, cont_ret_n_ret):
        driver = self.driver
        after_READ = self.after_READ
        declara_client = self.now_person
        try:
            js_confirm = driver.find_element_by_id('jsMsgBoxConfirm')
            """
            tk_msg('F2 para somente gerar os últimos 3 arquivos de declarações.\n F4 para RETIFICAR'
                   '\nF10 p/ consolidar para ultima data do mês\n\n'
                   '\nF11 Para passar para o próximo cliente \n\n'
                   'Espere ou clique OK', 10)
            """
            # não consegui callback em mensagem
            which_one = press_keys_b4('f2', 'f4', 'f10', 'f11')
            print(type(which_one))
            print(which_one)

            if which_one == 'f2':
                # consultar declarações, baixar arquivos
                self.simples_and_ecac_utilities(2, compt)

            elif which_one == 'f4':
                print('RETIFICA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                driver.execute_script("""
                window.location.href = '/SimplesNacional/Aplicacoes/ATSPO/pgdasd2018.app/Pa/Retificar'""")
                # raise vai fazer a ratificação
                raise NoSuchElementException
            elif which_one == 'f10':
                self.simples_and_ecac_utilities(1, compt)
                # F10 p/ consolidar para ultima data do mês
            elif which_one == 'f11':
                pass

        except NoSuchElementException:
            print('ALREADY FALSE')
            sleep(2.5)
            inp = driver.find_elements_by_tag_name('input')[0]
            sleep(3)
            print('R$', valor_declarado)

            inp = driver.find_elements_by_tag_name('input')[0]
            inp.clear()
            inp.send_keys(valor_declarado)
            for i in range(2):
                inp.send_keys(Keys.TAB)
            self.find_submit_form()
            sleep(3)
            print(f'{valor_declarado}, olha o valor aqui')

            if sheet_id == 0 or valor_declarado == '':
                for i in range(2):
                    self.tags_wait('form')
                    sleep(3)
                    try:
                        self.find_submit_form()
                    except NoSuchElementException:
                        driver.find_elements_by_class_name(
                            'btn-success')[1].click()
                    # em teste

            # ISS, index 1
            elif sheet_id == 1:
                def trata_retencoes(v):
                    try:
                        if float(eval(str(v).replace(',', '.'))) == 0:
                            v = ''
                    except SyntaxError:
                        # return v
                        v = v
                    finally:
                        return v

                if not my_new_3valores:
                    """
                    SemRetencao = self.trata_money_excel(after_READ['NÃO RETIDO'][cont_ret_n_ret])
                    ComRetencao = self.trata_money_excel(after_READ['RETIDO'][cont_ret_n_ret])
                    # padronizar essa parte
                    """
                    SemRetencao = self.trata_money_excel(
                        after_READ['Sem Retenção'][cont_ret_n_ret])
                    ComRetencao = self.trata_money_excel(
                        after_READ['Com Retenção'][cont_ret_n_ret])
                    # input('if not')
                else:
                    SemRetencao = self.trata_money_excel(
                        [v for v in my_new_3valores[2].values()][0])
                    ComRetencao = self.trata_money_excel(
                        [v for v in my_new_3valores[1].values()][0])
                    # input('else')
                print('~~~~~~~~~~~~' * 30)
                print(f'ANTES, Com Retenção: {ComRetencao}, Sem:{SemRetencao}')

                ComRetencao = trata_retencoes(ComRetencao)
                SemRetencao = trata_retencoes(SemRetencao)
                print('~~~~~~~~~~~~' * 30)
                print(f'Com Retenção: {ComRetencao}, Sem:{SemRetencao}')
                # input('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                print('~~~~~~~~~~~~' * 30)
                self.tags_wait('a')
                prestacao_serv = driver.find_element_by_id('btn-exibe-todos')
                prestacao_serv.click()
                sleep(2.5)

                if SemRetencao != '' and ComRetencao == '':
                    print('Só teve SEM RETENÇÃO')
                    self.send_keys_anywhere(Keys.TAB, 17 + 1)
                    self.send_keys_anywhere(Keys.ENTER)
                    self.find_submit_form()  # SUBMITA retenções s/ valor ainda
                    sleep(2.5)
                    self.send_keys_anywhere(valor_declarado)
                    self.send_keys_anywhere(Keys.ENTER)  # submita o valor
                    sleep(2.5)

                    self.send_keys_anywhere(Keys.ENTER)  # calcular
                    sleep(3)
                    self.find_submit_form()
                    sleep(2)
                elif SemRetencao != '' and ComRetencao != '':
                    print('Retido e não retido.')
                    self.send_keys_anywhere(Keys.TAB, 17 + 1)
                    self.send_keys_anywhere(Keys.ENTER)
                    self.send_keys_anywhere(Keys.TAB, 1)
                    self.send_keys_anywhere(Keys.ENTER)
                    self.find_submit_form()  # SUBMITA retenções s/ valor ainda
                    sleep(2)
                    self.send_keys_anywhere(SemRetencao)
                    self.send_keys_anywhere(Keys.TAB, 9)
                    self.send_keys_anywhere(ComRetencao)
                    self.send_keys_anywhere(Keys.ENTER)  # calcular
                    sleep(3)
                    self.find_submit_form()
                    sleep(2)

                elif SemRetencao == '' and ComRetencao != '':
                    print('\033[1;33mSó teve COM RETENÇÃO\033[m')
                    self.send_keys_anywhere(Keys.TAB, 17 + 2)
                    # +2 é COM retenção
                    self.send_keys_anywhere(Keys.ENTER)
                    self.find_submit_form()  # SUBMITA retenções s/ valor ainda
                    sleep(2.5)

                    self.send_keys_anywhere(valor_declarado)
                    self.send_keys_anywhere(Keys.ENTER)  # submita o valor
                    sleep(2.5)

                    self.send_keys_anywhere(Keys.ENTER)  # calcular
                    sleep(3)
                    self.find_submit_form()
                    sleep(2)
                # o valor já tá sendo tratado acima no IF master, mas ok
                if valor_declarado != '':
                    sleep(.5)
                    driver.find_elements_by_class_name(
                        'btn-success')[1].click()
                    # self.GERA_PGDAS2 acima
                    sleep(3.5)
                    driver.implicitly_wait(5)
                    try:
                        self.find_submit_form()
                    except NoSuchElementException:
                        driver.find_elements_by_class_name(
                            'btn-success')[1].click()

                    # DOWNLOAD feito pois já está setado nos argumentos do driver

            elif sheet_id == 2:
                # ICMS
                cont_vrv = cont_ret_n_ret

                VRV = after_READ['Venda ou Revenda'][cont_vrv]
                print(f'Venda ou revenda: {VRV}')
                vrv = VRV.lower().strip()
                self.tags_wait('a')
                prestacao_serv = driver.find_element_by_id('btn-exibe-todos')
                prestacao_serv.click()
                sleep(2.5)

                if vrv == 'revenda':
                    self.send_keys_anywhere(Keys.TAB, 3)
                    self.send_keys_anywhere(Keys.ENTER)

                elif vrv == 'venda':
                    self.send_keys_anywhere(Keys.TAB, 7)
                    self.send_keys_anywhere(Keys.ENTER)

                # o valor já tá sendo tratado acima no IF master, mas ok
                if valor_declarado != '':
                    sleep(2)
                    self.find_submit_form()
                    self.tags_wait('body', 'input', 'form')
                    sleep(1.5)
                    self.send_keys_anywhere(valor_declarado)
                    sleep(1.5)
                    self.send_keys_anywhere(Keys.ENTER)  # calcular
                    sleep(2.5)
                    self.tags_wait('body', 'input', 'form')
                    self.send_keys_anywhere(Keys.ENTER)  # transmitir
                    sleep(2)
                    self.find_submit_form()

                    sleep(.5)
                    driver.find_elements_by_class_name(
                        'btn-success')[1].click()
                    sleep(2.5)
                    self.find_submit_form()
                    # gerou

            # ~~~~~~~~~~~~~SEM-RETENÇÃO-universal~~~~~~~~~~~~~#
            print('AFTER IFs')
            # engloba
            add = '-SemMovimento' if valor_declarado == '' else ''
            save = self.certif_feito(self.client_path, add=add)
            driver.save_screenshot(save)

            self.simples_and_ecac_utilities(2, compt)
            # gera protocolos de todo mundo

            # ######################################################
        # print('Esperando pressionar DOWN no excel...')
        # press_key_b4('down')

    def simples_and_ecac_utilities(self, option, compt):
        """
        :param int option: somente de 1 a 2, sendo
        :param str compt: competência
        1 -> Gerar Das somente se for consolidar para outra DATA
        2 -> Gerar Protocolos
        :return:
        """
        # estou na "declaração", aqui faço o que quiser
        from datetime import datetime
        now_year = str(datetime.now().year)
        compt = ''.join(v for v in compt if v.isdigit())
        month_compt = compt[:2]
        year_compt = compt[2:]

        driver = self.driver
        current_url = self.current_url
        link_gera_das, download_protocolos_das = 'Das/PorPa', '/Consulta'

        if option == 2:

            self.get_sub_site(download_protocolos_das, current_url)
            driver.implicitly_wait(5)

            if now_year != year_compt:
                self.send_keys_anywhere(year_compt)
                self.find_submit_form()
                sleep(3.5)

            comp_clic = driver.find_elements_by_class_name('pa')
            lenc = len(comp_clic) - 1
            comp_clic[lenc].click()
            for i in range(3):
                sleep(2)
                self.send_keys_anywhere(Keys.TAB)
                self.send_keys_anywhere(Keys.ENTER)

        elif option == 1:
            # gera das
            venc_month_compt = int(month_compt) + 1
            venc = self.get_last_business_day_of_month(
                venc_month_compt, int(year_compt))
            retifica_p_dia = f'{venc}{venc_month_compt:02d}{year_compt}'
            self.get_sub_site(link_gera_das, current_url)
            self.tags_wait('input')
            driver.implicitly_wait(10)
            periodo = driver.find_element_by_id('pa')
            periodo.send_keys(compt)
            self.find_submit_form()
            sleep(2.5)
            # if  len(driver.find_elements_by_id('msgBox')) == 0 # CASO NÃO EXISTA O DAS
            consolida = driver.find_element_by_id('btnConsolidarOutraData')
            consolida.click()
            sleep(2.5)

            validade_id = 'txtDataValidade'
            driver.execute_script(
                f"document.getElementById('{validade_id}').focus();")
            validade_change = driver.find_element_by_id(validade_id)
            for e, val in enumerate(retifica_p_dia):
                validade_change.send_keys(val)
                if e == 0:
                    sleep(.25)

            sleep(1)
            driver.find_element_by_id('btnDataValidade').click()
            # coloquei a validade
            # gerei das
            driver.implicitly_wait(5)
            self.find_submit_form()
            # GERAR DAS
        else:
            return False

    def opta_script(self):
        driver = self.driver
        try:
            # #################################################### opta
            self.get_sub_site('/RegimeApuracao/Optar', self.current_url)
            # driver.execute_script("""window.location.href += '/RegimeApuracao/Optar'""")

            from selenium.webdriver.support.ui import Select
            anocalendario = Select(driver.find_element_by_id('anocalendario'))

            anocalendario.select_by_value('2021')
            self.find_submit_form()

            # competencia
            competencia, caixa = '0', '1'

            driver.find_element_by_css_selector(
                f"input[type='radio'][value='{competencia}']").click()
            self.find_submit_form()
            sleep(2.5)
            # driver.find_element_by_id('btnSimConfirm').click()

            try:
                driver.implicitly_wait(10)
                self.click_ac_elementors(
                    driver.find_element_by_class_name('glyphicon-save'))
            except NoSuchElementException:
                input('input Não consegui')
            else:
                print('Não fui exceptado')
            # ########################################################
        except NoSuchElementException:
            pass
        finally:
            driver.get(self.current_url)
            driver.execute_script(
                """window.location.href += '/declaracao?clear=1'""")
            sleep(2.5)

    def certif_feito(self, save_path, add=''):
        """
        certificado de que está feito
        :param save_path: nome da pasta vinda de _files_path_v2
        :param add: um adicional no nome do arquivo
        :return: caminho+ nome_arquivo jpeg
        """
        client_name = save_path[save_path.index('-')-2: save_path.index('-')+2]
        type_arquivo = 'png'
        try:
            save = r'{}\\{}-SimplesNacionalDeclarado.{}'.format(save_path, add, type_arquivo)
            print(save, '---------> SAVE')
            return save
        except FileNotFoundError:
            print('NÃO CONSEGUI RETORNAR SAVE')


PgdasAnyCompt()