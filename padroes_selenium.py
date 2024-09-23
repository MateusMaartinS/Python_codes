import pyautogui
import time
import random
import mousekey
import cv2
import numpy as np

mkey = mousekey.MouseKey()

def procurar_imagem(nome_arquivo, confidence=0.4, region=None, max_tentativas=30, horizontal=0, vertical=0, acao='clicar'):
   
    def clicar(x, y):
        pyautogui.click(x, y)

    def coordenada(x, y):
        print(f'Coordenadas da imagem: ({x}, {y})')

    def move_mouse(
        x,
        y,
        variationx=(-5, 5),
        variationy=(-5, 5),
        up_down=(0.2, 0.3),
        min_variation=-10,
        max_variation=10,
        use_every=4,
        sleeptime=(0.009, 0.019),
        linear=90,
    ):
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

    img_needle = cv2.imread(nome_arquivo, cv2.IMREAD_COLOR)

    if img_needle is None:
        raise FileNotFoundError(f"Imagem '{nome_arquivo}' não encontrada.")

    while tentativas < max_tentativas:
        tentativas += 1

        screenshot = pyautogui.screenshot(region=region) if region else pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screenshot, img_needle, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            x, y = max_loc
            x += img_needle.shape[1] // 2 + horizontal  
            y += img_needle.shape[0] // 2 + vertical
            coordenada(x, y)


            if acao == 'clicar':
                clicar(x, y)
            elif acao == 'mover_clicar':
                move_mouse(x, y)

            return True
        
        time.sleep(1)

# Exemplo de uso
procurar_imagem('testeCaptcha.png', acao='mover_clicar')
