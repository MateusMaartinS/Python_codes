import pyautogui
import time
import random
import mousekey
import pyscreeze

def procurar_imagem(nome_arquivo, confidence=0.8, region=None, max_tentativas=60, horizontal=0, vertical=0, acao='clicar', clicks=1, ocorrencia=1):
    mkey = mousekey.MouseKey()
    
    def click(x, y):
        pyautogui.click(x, y)

    def doubleClick(x, y):
        pyautogui.doubleClick(x, y)

    def coordenada(x, y):
        print(f'Coordenadas da imagem: ({x}, {y})')

    def move_mouse(x, y, variationx=(-5, 5), variationy=(-5, 5), up_down=(0.2, 0.3), min_variation=-10, max_variation=10, use_every=4, sleeptime=(0.009, 0.019), linear=90):
        mkey.left_click_xy_natural(
            int(x) - random.randint(*variationx),
            int(y) - random.randint(*variationy),
            delay=random.uniform(*up_down),
            min_variation=min_variation,
            max_variation=max_variation,
            use_every=use_every,
            sleeptime=sleeptime,
            print_coords=True,
            percent=linear,
        )

    acoes_validas = ['clicar', 'mover_clicar']

    if acao not in acoes_validas:
        raise ValueError(f"Ação inválida: '{acao}'. Escolha entre {acoes_validas}.")

    tentativas = 0
    while tentativas < max_tentativas:
        tentativas += 1
        try:
            imag = list(pyautogui.locateAllOnScreen(nome_arquivo, confidence=confidence, region=region))
            
            if imag:
                if len(imag) >= ocorrencia:
                    img = imag[ocorrencia - 1]  
                    x, y = pyautogui.center(img) 
                    x += horizontal
                    y += vertical

                    if acao == 'clicar':
                        match clicks:
                            case 0:
                                coordenada(x, y)
                            case 1:
                                click(x, y)
                            case 2:
                                doubleClick(x, y)

                    elif acao == 'mover_clicar':
                        move_mouse(x, y)
                    return True
                else:
                    print(f'A ocorrência {ocorrencia} não foi encontrada.')
                    return False

        except pyscreeze.ImageNotFoundException:
            pass
        time.sleep(1)

    print(f'Imagem não encontrada após {max_tentativas} tentativas.')
    return False

procurar_imagem('testeCaptcha.png', acao='mover_clicar')
