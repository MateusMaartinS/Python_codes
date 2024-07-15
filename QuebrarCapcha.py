import random
import time
import pyautogui
import cv2
import numpy as np
import mousekey
mkey = mousekey.MouseKey()
mkey.enable_failsafekill('ctrl+e')


def find_and_click(target_image_path, threshold=0.8):
    # Captura a tela atual
    screen = pyautogui.screenshot()
    screen_np = np.array(screen)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

    # Carrega a imagem alvo
    target = cv2.imread(target_image_path, 0)

    # Correspondência de modelo
    result = cv2.matchTemplate(screen_gray, target, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    for pt in zip(*loc[::-1]):
        pyautogui.click(pt[0] + target.shape[1] // 2, pt[1] + target.shape[0] // 2)
        break

def find_img(target_image_path, threshold=0.8):
    # Captura a tela atual
    screen = pyautogui.screenshot()
    screen_np = np.array(screen)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

    # Carrega a imagem alvo
    target = cv2.imread(target_image_path, 0)

    # Correspondência de modelo
    result = cv2.matchTemplate(screen_gray, target, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    click_positions = []
    for pt in zip(*loc[::-1]):
        click_x = pt[0] + target.shape[1] // 2
        click_y = pt[1] + target.shape[0] // 2
        #pyautogui.click(click_x, click_y)
        click_positions.append((click_x, click_y))
        break
    
    return click_positions

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


campoCnpj = find_img('Quebrar Capcha\\campoCnpj.png')

if campoCnpj:
    move_mouse(campoCnpj[0][0],campoCnpj[0][1])


time.sleep(1.5)
pyautogui.typewrite("05.720.367/0001-01")


capchat = find_img('Quebrar Capcha\\opcaoCap.png')

if capchat:
    move_mouse(capchat[0][0], capchat[0][1])

consulta = find_img('Quebrar Capcha\\consultar.png')

time.sleep(2)

if consulta:
    move_mouse(consulta[0][0], consulta[0][1])


#move_mouse(369,799)