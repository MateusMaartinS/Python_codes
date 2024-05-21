from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException 
import pyautogui
import random
import mousekey
import time
mkey = mousekey.MouseKey()
"""
 A ideia é que você faça com que o selenium possa acessar uma instancia do chorme ja aberta
 Porém ao clicar em algum Captcha o Google vai identificar que é um robô, por conta do selenium estar ativado
 então desativamos o selenium para que seja feito o click no captcha e assim passamos
 logo em seguida ativamos novamente o selenium e seguimos com a altomação

"""
#-------------------------------CHROME DRIVER---------------------------

# funcao para iniciar o chorme e que o selenium possa acessar essa instancia
# start chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Selenium\ChromeTestProfile"
def iniciar_navegador(com_debugging_remoto=True):
    chrome_driver_path = ChromeDriverManager().install()
    service = Service(executable_path=chrome_driver_path)
    
    chrome_options = Options()
    if com_debugging_remoto:
        remote_debugging_port = 9222
        chrome_options.add_experimental_option("debuggerAddress", f"localhost:{remote_debugging_port}")
    
    navegador = webdriver.Chrome(service=service, options=chrome_options)
    return navegador

navegador = iniciar_navegador(com_debugging_remoto=True)

#-----------------------------------------------------------------------


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


def clicar_captcha(navegador):
    navegador.quit()

    move_mouse(87,52)
    move_mouse(52,370)

    navegador = iniciar_navegador(com_debugging_remoto=True)

    navegador.switch_to.default_content()

    iframe = navegador.find_element(By.ID, 'iframeteste')
    navegador.switch_to.frame(iframe)
    
    time.sleep(0.5)
    botaoProsseguir = navegador.find_element(By.XPATH, 'XPATH exemplo')
    botaoProsseguir.click()

    time.sleep(0.5)
    botaoPesquisar = navegador.find_element(By.XPATH, 'XPATH exemplo')
    botaoPesquisar.click()

