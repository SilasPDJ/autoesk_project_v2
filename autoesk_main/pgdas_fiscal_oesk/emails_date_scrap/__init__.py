class EmailsDateScrap:

    def vencimento_das(self):
        # pega o vencimento do site pra puxar em outro lugar, muito legal
        if self.check_venc_precisao():
            # return '22/02/2021'
            return self.das_venc_data()[0]

        return self.__calcula_venc_precisao()

    def vencimento_dividas(self):
        # pega o vencimento do site pra puxar em outro lugar, muito legal
        return self.__calcula_venc_precisao(False)

    def __calcula_venc_precisao(self, das_or_dividas=True):
        """
        # finalmente cheguei ao que eu queria
        :param das_or_dividas: True: se trata do DAS, False=> se trata das dívidas
        não checka => False e vai para a etapa de decidir o vencimento no último dia útil...
        :return: False => Site não está de acordo com o vencimento atual, preencha manualmente uma vez;
                 True  => Está de acordo, exemplo, mes de agora é 01, logo vence 30/01... Assim adiante
        """
        from dateutil.relativedelta import relativedelta
        from datetime import datetime as dt
        from datetime import date, timedelta
        m = dt.now().month

        def __business_day(calcday):
            while True:
                if calcday.weekday() == 6:
                    calcday += timedelta(days=1)
                elif calcday.weekday() == 5:
                    calcday -= timedelta(days=1)
                else:
                    # calc_days
                    calcday = f'{calcday.day:02d}/{calcday.month:02d}/{calcday.year}'
                    # return Now.date2date_brazil(calcday)
                    return calcday

        date_explicit = date(dt.now().year, m+1, 1)
        # calcula o último dia util do mês (sendme)
        calc_day = date_explicit - timedelta(days=1)

        if das_or_dividas is False:
            # DÍVIDAS
            calc_day = calc_day - relativedelta(days=1)
            return __business_day(calc_day)
        else:
            # DAS
            calc_day = calc_day + relativedelta(day=20)
            """    
            for i in range(1, 13):
                print(__business_day(date(2021, i, 20)))
            print(__business_day(calc_day))
            input('test')
            """
            return __business_day(calc_day)

    def inside_me_others(self, inside_me, *others):
        """
        :param str inside_me:
        :param str others:
        :return:

        Cria tags (*others) dentro da inside_me
        """
        # pega o final e separa para colocar no meio
        ff = inside_me.index('</')

        final = inside_me[ff:]
        returned = inside_me[:ff]

        for other in others:
            returned += other
            # input(returned)
        returned += final
        return returned

    def wcor(self, cor):
        r = f' style=color:{cor}'
        return r

    def das_venc_data(self):
        """

        bs4 BeautifulSoup requests

        :return: A_Main data de vencimento da competência de acordo com o portal
        """
        from bs4 import BeautifulSoup
        import requests

        def soup(me):
            """
            :param me: element
            :return:
            """
            me = str(me)
            btf = BeautifulSoup(me, 'html.parser')
            return btf

        # bto é btf
        req = requests.get('http://www8.receita.fazenda.gov.br/SimplesNacional/Agenda/Agenda.aspx')
        req.encoding = 'utf-8'
        req = req.text
        btinit = soup(req)
        # btinit = BeautifulSoup(rq, "html.parser")
        # aqui é o início, a soup vai ser com os elementos vindos daqui

        agenda = btinit.select('#agenda .prazo')
        # print(agenda) -> HTML
        venc = soup(agenda)
        venc_text = venc.get_text()
        venc_final = self.date_only(venc_text)

        # venc_final[0] -> DAS, venc_final[1] -> MEI
        venc_final = venc_final[0] if len(venc_final) == 1 else venc_final
        # return vencimento DAS date
        return venc_final

        # soup(el).get_text # -> somente um dos métodos, o mesmo retorna uma lista

    def last_portal_update(self):
        """
        :return: data da atualização
        """

        from bs4 import BeautifulSoup
        import requests

        def soup(me):
            """
            :param me: element
            :return:
            """
            me = str(me)
            btf = BeautifulSoup(me, 'html.parser')
            return btf

        # bto é btf
        req = requests.get('http://www8.receita.fazenda.gov.br/SimplesNacional/Agenda/Agenda.aspx').text
        btinit = soup(req)

        last_update = btinit.select('#atualizado')

        updt = soup(last_update)
        updt = updt.get_text()

        updt = self.date_only(updt)
        # se o len do update for 1, é o caso do id, não precisa colocar index

        try:
            with open('ultima_att_agenda.txt') as f:
                att = f.read()
                if self.date_only(att) != updt:
                    raise FileNotFoundError
                    # ele vai escrever a última atualização
                else:
                    raise FileExistsError
        except FileNotFoundError:
            with open('ultima_att_agenda.txt', 'w') as f:
                f.write(updt)
                print(' \033[1;31m -------> NOVA ATUALIZAÇÃO DO PORTAL!!!\033[m')
                return updt

        except FileExistsError:
            with open('ultima_att_agenda.txt', 'w') as f:
                f.write(f'ATUALIZADO -> {updt}')
                print('\033[1;34m ---> Portal está de acordo com o arquivo\033[m')
                return att

        # return True pra de acordo e False pra nova atualização????????????????????????????

    def check_venc_precisao(self):
        """
        Checka se a precisão do vencimento NO PORTAL está de acordo com a competência
        :return:
        """
        from dateutil.relativedelta import relativedelta
        from datetime import datetime as dt
        from datetime import date, timedelta
        m = dt.now().month
        date_explicit = date(dt.now().year, m, 1)

        venc_anterior = date_explicit - relativedelta(months=1)

        vd = self.das_venc_data()[0]

        VENCIMENTO_DAS_mes = vd[3:5]
        # Se ainda está ultrapassado NA WEB...
        if int(VENCIMENTO_DAS_mes) == int(venc_anterior.month):
            return False
        return True

    def date_only(self, venc_text):
        """
        :param venc_text: containing DATES
        :return: list scrapping DATES
        """
        try:
            venc_text = venc_text.split()
        except AttributeError:
            if isinstance(venc_text, object):
                print('prossegue')
            else:
                return False

        venc_final = []
        for el in venc_text:
            new_el = ''
            for e in el:
                if e.isnumeric() or e == '/':
                    new_el += e
                    new_el = new_el.strip()
            if new_el != '':
                venc_final.append(new_el)

        venc_final = venc_final[0] if len(venc_final) == 1 else venc_final
        # se tiver o tamanho só de 1, eu já retorno, por causa do teste na função self.last_portal_update
        return venc_final