def cria_site_v1(write, qtd_text):
    from concurrent.futures import ThreadPoolExecutor
    from time import sleep
    import pyautogui as pygui
    import os
    """
    :param write: lista q vai ser escrita no arquivo html
    :return: True p/ criar Arquivo, False para não
    """

    import re
    # write_find = [m.start() for m in re.finditer('.notaCancelada', str(write))]
    tables = write_find = [m.start() for m in re.finditer('<table', str(write))]
    # input(f'MAX-VALUE NO FILE->{write_find}')
    len_tables = len(tables)

    # if len(write_find) > 0: # -> legal, mas não vou conseguir usar, vou ter que exportar todos pois pode ser que todos tenham
    print("retornando tupla se True...")
    if True:
        from time import sleep
        from os import system
        s = 'new-site.html'
        site = open(s, 'w')

        site.write(write)
        site.close()

        executors_list = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            executors_list.append(executor.submit(system, 'new-site.html'))
            sleep(2)
            # pygui.click(1900, 1000)
            # pygui.drag(-1900, -1000, duration=.5)
            x, y = pygui.position()
            # ou então pygui append hotkey ('control', 'a')

            executors_list.append(executor.submit(pygui.getActiveWindow().maximize))
            sleep(2)
            executors_list.append(executor.submit(pygui.click, pygui.getActiveWindow().centerx,
                                                  pygui.getActiveWindow().centery))
            executors_list.append(executor.submit(pygui.hotkey, 'ctrl', 'a', interval=.2))
            sleep(2)
            print('holy')

            # executors_list.append(executor.submit(pygui.click, x, y))
            executors_list.append(executor.submit(pygui.hotkey, 'ctrl', 'c'))
           # sleep(.2)
            # executors_list.append(executor.submit(pygui.click, x, y))
            sleep(2)
            executors_list.append(executor.submit(pygui.click, pygui.position()))
            # executors_list.append(executor.submit(pygui.hotkey, 'ctrl', 'f'))
            executors_list.append(executor.submit(pygui.hotkey, 'ctrl', 'w'))

    return True, len_tables
