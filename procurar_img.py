import pyautogui
import time


def procurar_imagem(nome_arquivo, confidence=0.8, region=False, max_tentativas=50, horizontal=0 , vertical=0):
    clicou = False
    tentativas = 0

    while not clicou and tentativas < max_tentativas:
        try:
            tentativas += 1
            opcao = pyautogui.locateCenterOnScreen(nome_arquivo, confidence=confidence, region=region)
            x, y = opcao
            x += horizontal
            y += vertical
            pyautogui.click(x, y)
            clicou = True
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)