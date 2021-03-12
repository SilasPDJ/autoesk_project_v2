# dale
from imports import Keys, By, WebDriverWait, expected_conditions
from imports import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from imports import activate_window, press_key_b4

from imports import WDShorcuts, ExcelToData
from _new_set_paths import NewSetPaths
from imports import sleep


class Dividas(WDShorcuts, NewSetPaths, ExcelToData):
    def __init__(self):
        print('filespathteste')
        """
        :param compt_file: from GUI

        # remember past_only arg from self.get_atual_competencia
        """
        import pandas as pd
        from default.webdriver_utilities.pre_drivers import pgdas_driver

        # O vencimento DAS(seja pra qual for a compt) está certo, haja vista que se trata do mes atual

        sh_names = ['_Dívidas']
        compt = super().get_compt_only()
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

            for i, CNPJ in enumerate(after_READ['CNPJ']):
                CLIENTE = after_READ['Razão Social'][i]
                JA_DECLARED = after_READ['Declarado'][i]
                simples_or_ativa = after_READ['tipo'][i]

                if JA_DECLARED not in ['S', 'OK', 'FORA']:

                    self.client_path = self.files_pathit('Dívidas_Simples_' + CLIENTE, compt)
                    __client_path = self.client_path

                    self.driver = pgdas_driver(__client_path)
                    super().__init__(self.driver)
                    driver = self.driver

                    self.loga_cert()
                    self.change_ecac_client(CNPJ)

                    driver.find_element_by_id('linkHome').click()

                    if simples_or_ativa == 'simples nacional':
                        driver.find_element_by_link_text(
                            'Simples Nacional').click()
                        driver.find_element_by_link_text(
                            'Solicitar, acompanhar e emitir DAS de parcelamento').click()

                        driver.implicitly_wait(10)

                        driver.switch_to.frame(
                            driver.find_element_by_id('frmApp'))

                        empel = driver.find_element_by_id(
                            'ctl00_contentPlaceH_linkButtonEmitirDAS')
                        empel.click()
                        WebDriverWait(self.driver, 20).until(
                            expected_conditions.presence_of_element_located((By.XPATH, '//input[@value="Continuar"]'))
                        ).click()

                        imprimires = WebDriverWait(self.driver, 20).until(
                            expected_conditions.presence_of_all_elements_located((By.LINK_TEXT, 'Imprimir')))
                        for imprimir in imprimires:
                            imprimir.click()
                        # Imprimir
                        driver.switch_to.default_content()
                    elif simples_or_ativa == 'dívida ativa':

                        driver.find_element_by_link_text(
                            'Dívida Ativa da União').click()
                        driver.find_element_by_link_text(
                            'Débitos Inscritos em Dívida Ativa da União').click()

                        driver.switch_to.window(driver.window_handles[1])
                        driver.implicitly_wait(10)

                        sispar_url = f"{'/'.join(driver.current_url.split('/')[:-1])}/sispar"
                        driver.get(sispar_url)
                        try:
                            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'button')))
                            self.tag_with_text(
                                'button', 'Acessar o SISPAR').click()
                        except NoSuchElementException:
                            WebDriverWait(self.driver, 10).until(
                                expected_conditions.presence_of_element_located((By.TAG_NAME, 'button')))
                            self.tag_with_text(
                                'button', 'Acessar').click()
                            # provavelmente uma mudança no sistema mas vou validar
                        # WebDriverWait(self.driver, 10).until(expected_conditions.new_window_is_opened(driver.window_handles))
                        WebDriverWait(self.driver, 10).until(
                            expected_conditions.number_of_windows_to_be(3))
                        driver.switch_to.window(driver.window_handles[2])

                        driver.execute_script(
                            "PrimeFaces.addSubmitParam('cabecalho',{'cabecalho:j_idt45':'cabecalho:j_idt45'}).submit('cabecalho');")
                        self.click_elements_by_tt('DEFERIDO E CONSOLIDADO')
                        sleep(1)
                        WebDriverWait(self.driver, 20).until(
                            expected_conditions.presence_of_element_located((By.ID, 'formListaDarf:idbtnDarf'))).click()

                        WebDriverWait(self.driver, 20).until(
                            expected_conditions.presence_of_element_located((By.TAG_NAME, 'table')))
                        compt_dividas_ativas = f'{self.m():02d}/{self.y()}'
                        print(compt_dividas_ativas)

                        sleep(7)

                        dris = driver.find_elements_by_css_selector(
                            ".colunaAlinhaCentro")

                        elemitidos = driver.find_elements_by_css_selector(
                            f"[title*='Já emitido']")
                        for el in elemitidos:
                            el.click()
                            sleep(.5)
                            self.send_keys_anywhere(Keys.ENTER)
                        print('breakou, baixou JÁ EMITIDOS')
                        self.contains_title('Não emitido').click()
                        sleep(.5)
                        self.send_keys_anywhere(Keys.ENTER)
                        self.click_ac_elementors(WebDriverWait(self.driver, 20).until(
                            expected_conditions.presence_of_element_located((
                                By.ID, 'formResumoParcelamentoDarf:dlgInformacoesEmissaoDarf'))))
                        self.send_keys_anywhere(Keys.TAB)
                        self.send_keys_anywhere(Keys.TAB)
                        self.send_keys_anywhere(Keys.ENTER)

                        self.click_ac_elementors(WebDriverWait(self.driver, 20). until(
                            expected_conditions.presence_of_element_located((By.ID, 'formResumoParcelamentoDarf:emitirDarf'))))

                        WebDriverWait(self.driver, 5)

                    else:
                        print('ACABOU, break')
                        break

    def loga_cert(self):
        """
        :return: mixes the two functions above (show_actual_tk_window, mensagem)
        """
        from threading import Thread
        from pyautogui import hotkey

        driver = self.driver
        while True:
            try:
                driver.get(
                    'https://cav.receita.fazenda.gov.br/autenticacao/login')
                driver.set_page_load_timeout(30)
                break
            except TimeoutException:
                driver.refresh()
            finally:
                sleep(1)

        activate_window('eCAC - Centro Virtual de Atendimento')
        """
        while True:
            try:
                driver.get('https://cav.receita.fazenda.gov.br/')
                driver.set_page_load_timeout(5)
                break
            except TimeoutException:
                driver.refresh()
            finally:
                sleep(1)
        """
        # initial = driver.find_element_by_id('caixa1-login-certificado')
        driver.get(
            'https://sso.acesso.gov.br/authorize?response_type=code&client_id=cav.receita.fazenda.gov.br&'
            'scope=openid+govbr_recupera_certificadox509+govbr_confiabilidades&'
            'redirect_uri=https://cav.receita.fazenda.gov.br/autenticacao/login/govbrsso')
        initial = driver.find_element_by_link_text('Certificado digital')

        print('ativando janela acima, logando certificado abaixo, linhas 270')
        sleep(2)
        # self.thread_pool_executor(initial.click, [hotkey, 'enter'])

        t = Thread(target=initial.click)
        t.start()
        tt = Thread(target=sleep(2.5))
        tt.start()
        # B4 enter, ir pra baixo por causa do certificado do castilho
        tb4 = Thread(target=hotkey('down'))
        tb4.start()
        tt2 = Thread(target=sleep(2))
        tt2.start()
        t2 = Thread(target=hotkey('enter'))
        t2.start()

    def change_ecac_client(self, CNPJ):
        """:return: vai até ao site de declaração do ECAC."""
        driver = self.driver

        def elem_with_text(elem, searched):
            _tag = driver.find_element_by_xpath(
                f"//{elem}[contains(text(),'{searched.rstrip()}')]")
            return _tag

        self.tags_wait('html', 'span')
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
        # c
Dividas()