import pyautogui        # pip install pyautogui
import time             # (biblioteca padrão do Python)
import random           # (biblioteca padrão do Python)
import mousekey         # pip install mousekey - https://github.com/hansalemaos/mousekey
import pyscreeze        # pip install pyscreeze
from PIL import Image   # pip install pillow

def procurarImagem(nome_arquivo, confidence=0.8, region=None, maxTentativas=60, horizontal=0, vertical=0, dx=0, dy=0, acao='clicar', clicks=1, ocorrencia=1, delay_tentativa=1, usarRedimensionamento=False, resolucaoOriginal=(1920, 1080)):
    mkey = mousekey.MouseKey()

    def click(x, y):
        pyautogui.click(x, y)

    def doubleClick(x, y):
        pyautogui.doubleClick(x, y)

    def coordenada(x, y):
        print(f'Coordenadas da imagem {nome_arquivo}: ({x}, {y})')

    def moveMouse(x, y, variationx=(-5, 5), variationy=(-5, 5), up_down=(0.2, 0.3), min_variation=-10, max_variation=10, use_every=4, sleeptime=(0.009, 0.019), linear=90):
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

    def clickDrag(x, y, dx, dy):
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        pyautogui.moveTo(x + dx, y + dy, duration=0.5)
        pyautogui.mouseUp()

    def redimensionarImagem(caminhoImagem, resolucaoOriginal=(1920, 1080), caminhoSaida=None):
        larguraAtual, alturaAtual = pyautogui.size()
        larguraOriginal, alturaOriginal = resolucaoOriginal

        try:
            with Image.open(caminhoImagem) as img:
                escalaLargura = larguraAtual / larguraOriginal
                escalaAltura = alturaAtual / alturaOriginal
                
                escala = min(escalaLargura, escalaAltura)

                larguraNova = int(img.size[0] * escala)
                alturaNova = int(img.size[1] * escala)

                imgRedimensionada = img.resize((larguraNova, alturaNova), Image.Resampling.LANCZOS)

                if not caminhoSaida:
                    caminhoSaida = f'redimensionado_{caminhoImagem}'

                imgRedimensionada.save(caminhoSaida)
                print(f"Imagem redimensionada salva em: {caminhoSaida}")
                return caminhoSaida
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {caminhoImagem}")
            return None
        except Exception as e:
            print(f"Erro ao redimensionar a imagem: {e}")
            return None

    if usarRedimensionamento:
        resolucaoAtual = pyautogui.size()
        nome_arquivo = redimensionarImagem(nome_arquivo, resolucaoOriginal, resolucaoAtual)
        if not nome_arquivo:
            print(f"Erro ao redimensionar a imagem {nome_arquivo}. Verifique o arquivo.")
            return False

    acoesValidas = ['clicar', 'mover clicar', 'clicar arrastar']

    if acao not in acoesValidas:
        raise ValueError(f"Ação inválida: '{acao}'. Escolha entre {acoesValidas}.")

    tentativas = 0
    while tentativas < maxTentativas:
        tentativas += 1
        try:
            imag = list(pyautogui.locateAllOnScreen(nome_arquivo, confidence=confidence, region=region))
            
            if imag:
                if len(imag) >= ocorrencia:
                    img = imag[ocorrencia - 1]  
                    x, y = pyautogui.center(img) 
                    x += horizontal
                    y += vertical

                    match acao:
                        case 'clicar':
                            match clicks:
                                case 0:
                                    coordenada(x, y)
                                case 1:
                                    click(x, y)
                                case 2:
                                    doubleClick(x, y)

                        case 'mover clicar':
                            moveMouse(x, y)
                        
                        case 'clicar arrastar':
                            clickDrag(x, y, dx, dy)

                    return True
                else:
                    print(f'A ocorrência {ocorrencia} não foi encontrada.')
                    return False

        except pyscreeze.ImageNotFoundException:
            pass
        time.sleep(delay_tentativa)

    print(f'Imagem {nome_arquivo} não encontrada após {maxTentativas} tentativas.')
    return False


procurarImagem('teste.png', acao='mover clicar')
