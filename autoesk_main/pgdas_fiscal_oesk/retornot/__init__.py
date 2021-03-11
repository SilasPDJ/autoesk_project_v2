from time import sleep
import pyautogui as pygui
import pyperclip as ppclip


class RetidosNorRetidos:
    def __init__(self):
        sleep(2)
        pygui.hotkey('enter')
        sleep(.5)
        pygui.hotkey('ctrl', 'v')
        sleep(.5)
        self.auto_ajuste() # F de formato no atalho
        self.GET_KEY_STATE(False)

        sleep(2)
        pygui.hotkey('ctrl', 'down')
        sleep(.5)
        self.foritab(2, 'down')
        sleep(.5)
        pygui.hotkey('ctrl', 'n')
        sleep(.5)
        pygui.write('Valor total')
        sleep(.5)
        self.foritab(2, 'right')
        self.auto_soma_reterNreter()

        """"""
        # self.localizar_to('A') # alt
        # achar A1, C2, E5, etc.
        """"""

        """~~~~~~~~~~~~~~~~~~~~"""
        # self.write_formula("SE(D1=0;C1;0)")
        # RETIDO
        # self.write_formula('SOMASE(D1:D12;">"&0;C1:C12)')
        """self.somaSE_v1(';">"&0;', ups=3)"""

        self.somaSE_v2(3, ">")
        sleep(.5)
        pygui.hotkey('up') # volta e formata
        sleep(.5)
        self.auto_formatar('Contábil')
        sleep(.5)
        pygui.hotkey('enter')
        """~~~~~~~~~~~~~~~~~~~~"""
        """~~~~~~~~~~~~~~~~~~~~"""
        # self.write_formula("SE(D1>0;C1;0)")
        # NÃO RETIDO
        # self.SOMA_SE_v1('SOMASE(D1:D12;"="&0;C1:C12)')
        """self.somaSE_v1(';"="&0;', ups=4)"""

        self.somaSE_v2(4, "=")
        sleep(.5)
        pygui.hotkey('up') # volta e formata
        sleep(.5)
        self.auto_formatar('Contábil')
        sleep(.5)
        pygui.hotkey('enter')
        """~~~~~~~~~~~~~~~~~~~~"""

        self.ctrl_arrow('left')
        pygui.hotkey('up')
        sleep(1.5)
        ppclip.copy('NÃO RETIDO')
        sleep(1)
        pygui.hotkey('ctrl', 'v')

        sleep(.5)
        self.foritab(1, 'up')
        pygui.write('RETIDO')
        sleep(.5)
        self.foritab(3, 'up')

        self.foritab(2, 'right') # para não excluir as NF

        self.ctrl_shift_arrow('up', 'right')
        self.auto_formatar('Contábil')
        # função boa

       # adiciona o filtro
        self.ctrl_arrow('up', 'right')
        sleep(.5)
        pygui.hotkey('up')
        for i in range(10):
            pygui.write('cancel.=vermelho')
            sleep(.5)
            self.hotkey = pygui.hotkey('left')
        pygui.hotkey('up')
        self.auto_filtrar()
        sleep(.5)
        self.alt_arrow('down')
        self.foritab(6, 'down')
        sleep(.5)
        pygui.hotkey('enter', 'down', 'enter', interval=.5)
        sleep(1)
        # ctrl C FS A
    def somaSE_v1(self, condit, ups):
        """
        funções-self: foritab, ctrl_sfhit_arrow
        :param: ups -> a distância para pressionar up
        :param condit: sempre com o ; no início e ; no final.
        :return:
        """
        """escreve formula"""

        pygui.write("=SOMASE(")
        '''
        pygui.hotkey('tab')
        sleep(.5)
        '''
        self.foritab(1, 'right')
        sleep(.5)
        self.foritab(ups, 'up')
        sleep(.5)
        self.ctrl_shift_arrow('up')
        sleep(.5)
        pygui.write(condit)

        '''
        pygui.hotkey('tab')
        sleep(.5)
        '''
        # self.foritab(1, 'right')
        self.foritab(ups, 'up')
        sleep(.25)
        self.ctrl_shift_arrow('up')
        sleep(.5)
        pygui.write(')')
        sleep(.2)
        pygui.hotkey('enter')

    def somaSE_v2(self, ups, operador):
        """
        funções-self: foritab, ctrl_sfhit_arrow
        :param: ups -> a distância para pressionar up
        :param operador: >, <, <> =, excel.
        :return:
        """
        """escreve formula"""

        pygui.write("=SOMARPRODUTO(SUBTOTAL(9;DESLOC(C2;LIN(")

        self.foritab(ups, 'up')
        sleep(.25)
        self.ctrl_shift_arrow('up')
        sleep(.5)
        pygui.write(')-LIN(C2);0));(')
        sleep(.2)

        sleep(.5)

        '''
        pygui.hotkey('tab')
        sleep(.5)
        '''
        # self.foritab(1, 'right')
        self.foritab(1, 'right')
        sleep(.5)
        self.foritab(ups, 'up')
        sleep(.5)
        self.ctrl_shift_arrow('up')
        sleep(.5)
        pygui.write(f'{operador}0)+0)')
        sleep(.5)
        pygui.hotkey('enter')

    def write_formula(self, formula):
        pygui.write(f"={formula}", interval=0.1)
        sleep(.5)
        pygui.hotkey('enter')
        sleep(1)

    def auto_soma(self):
        """
        :return: AUTO SOMA NAVEGADO POR ATALHOS
        # not in uso, but useful
        """
        pygui.hotkey('ctrl', 'n')  # negrita
        sleep(.5)
        pygui.hotkey('alt', interval=.5)
        pygui.write('cus', interval=.5)
        sleep(.5)
        pygui.hotkey('enter')
        sleep(1)

    def auto_soma_reterNreter(self):
        pygui.hotkey('ctrl', 'n')
        sleep(.5)
        self.auto_formatar('contábil')# negrita
        sleep(1)
        pygui.write('=SOMA(')
        sleep(.5)
        pygui.hotkey('down')
        sleep(.5)
        pygui.write(':')
        sleep(.5)
        pygui.hotkey('down')
        sleep(.5)
        pygui.write(')')
        sleep(.5)

        pygui.hotkey('enter')

    def auto_formatar(self, format_as):
        # atalho no excel que formata o formato da célula rs
        ppclip.copy(format_as)
        pygui.hotkey('alt', 'c', interval=.25)
        sleep(.5)
        pygui.write('FN')
        sleep(.5)
        pygui.hotkey('ctrl','v')
        sleep(.5)
        pygui.hotkey('enter')

    def auto_filtrar(self):
        # INICIA/ DESABILITA
        pygui.hotkey('alt', 'c', interval=.25)
        sleep(.5)
        pygui.write('sf', interval=.5)
        sleep(.5)

    def auto_ajuste(self):
        what = 'O'
        pygui.hotkey('alt', 'c')
        sleep(.5)
        pygui.write(what)
        sleep(.5)
        pygui.write('H')
        sleep(.5)
        pygui.write('15')
        sleep(.5)
        pygui.hotkey('enter')

    # ~~~~~~~~~~~~~~~ARROWS~~~~~~~~~~~~~ #
    def ctrl_shift_arrow(self, *arrows):
        # excel -> seleciona de várias em várias com valor

        pygui.keyDown('ctrl')
        pygui.keyDown('shift')
        for arr in arrows:
            sleep(.25)
            pygui.hotkey(arr)
        pygui.keyUp('shift')
        pygui.keyUp('ctrl')

    def shift_arrow(self, *arrows):
        # excel -> seleciona uma por uma
        pygui.keyDown('shift')
        for arr in arrows:
            sleep(.25)
            pygui.hotkey(arr)
        pygui.keyUp('shift')

    def ctrl_arrow(self, *arrows):
        # se movimenta da com valor até a prox
        pygui.keyDown('ctrl')
        for arr in arrows:
            sleep(.25)
            pygui.hotkey(arr)
        pygui.keyUp('ctrl')

    def alt_arrow(self, *arrows):
        # se movimenta da com valor até a prox
        pygui.keyDown('alt')
        for arr in arrows:
            sleep(.25)
            pygui.hotkey(arr)
        pygui.keyUp('alt')
    # ~~~~~~~~~~~~~~~ARROWS~~~~~~~~~~~~~ #

    def localizar_to(self, letra_final):
        """not in use yet"""
        pygui.hotkey('alt', 'c', interval=.5)
        pygui.write('FS')
        sleep(.5)
        pygui.write(letra_final)

    def GET_KEY_STATE(self, set_enable):
        from win32api import GetKeyState
        from win32con import VK_NUMLOCK, VK_CAPITAL
        """
        :param str key: numlock / capslock
        :param bool set_enable: True -> enabled, False -> Disabled
        :return: desliga ou liga capslock/numlock
        """
        numlock = GetKeyState(VK_NUMLOCK)
        capslock = GetKeyState(VK_CAPITAL)
        if set_enable:
            if numlock == 0 or capslock == 0:
                pygui.hotkey('numlock')
                pygui.hotkey('capslock')
        else:
            if numlock == 1 or capslock == 1:
                pygui.hotkey('numlock')
                pygui.hotkey('capslock')

    def foritab(self, n, key, interval=.13):
        """
        :param int n: qtd de vezes
        :param str key: hotkey
        :param float interval: interval
        :return:
        """

        for ii in range(n):
            pygui.hotkey(key, interval=interval)

            E = 'E'
            # pygui.write("=SE(D1=0;C1;0)")

            # pygui.write("=SE(D1>0;C1;0)")


def save_after_changes(name):
    """
    :param name:
    :return: CHECKAR QUAIS XLSX foram criados... Fazer ainda
    """
    from shutil import copyfileobj
    import os
    from datetime import datetime as dt
    ano = dt.now().year
    mes = dt.now().month

    with_title_name = '../with_titlePATH.txt'
    f = open(with_title_name, 'r')
    onde_ir = f.read()
    competencia = f'{mes - 1:02d}-{ano}'
    volta = os.getcwd()

    PASTA_NOME = 'G5'

    g5 = r'{}/../{}'.format(onde_ir, PASTA_NOME)
    g5_list = os.listdir(g5)
    os.chdir(g5)
    print(os.getcwd())

    for folder in g5_list:
        os.chdir(folder)

        os.chdir(r'{}\{}'.format(ano, competencia))
        arqs = os.listdir()
        # arquivos presentes
        if folder == name:
            if len(arqs) > 0:
                print(f'\033[1;32m{folder}\033[m')
                for arq in arqs:
                    if arq.endswith('.xlsx'):
                        print(arq, end=' ')
                        copyfileobj('{}'.format(arq),
                              r'{}\{}'.format(volta, arq))

                print()
        os.chdir('../../..')
    f.close()


class RnrSo1(RetidosNorRetidos):
    # RETINDOS_N_RETIDOS só com 1 valor

    # it's omited but I don't want to call it.
    def __init__(self):
        super(RnrSo1).__init__()
        sleep(2)
        sleep(.5)
        pygui.hotkey('ctrl', 'v')
        sleep(.5)
        self.auto_ajuste() # F de formato no atalho
        self.GET_KEY_STATE(False)

        valores = ['Valor total', 'RETIDO', 'NÃO RETIDO']

        foritab = self.foritab
        write = pygui.write

        for wr in valores:
            foritab(1, 'down')
            if valores.index(wr) == len(valores) - 1:
                ppclip.copy(wr)
                sleep(1)
                pygui.hotkey('ctrl', 'v')
                break
            write(wr)
        f_ret = '=SOMARPRODUTO(SUBTOTAL(9;DESLOC(C1;LIN(C1)-LIN(C1);0));(D1>0)+0)'
        f_nnt = '=SOMARPRODUTO(SUBTOTAL(9;DESLOC(C1;LIN(C1)-LIN(C1);0));(D1=0)+0)'

        foritab(2, 'right')
        for formula in [f_nnt, f_ret]:
            self.auto_formatar('Contábil')
            write(formula)
            foritab(1, 'up')
        self.auto_soma_reterNreter()
        foritab(1, 'enter')
        sleep(.5)
        pygui.hotkey('alt', 'f4')
        sleep(2)
        pygui.hotkey('enter')
