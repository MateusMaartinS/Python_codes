import threading
import tkinter as tk
from PIL import ImageGrab, Image
import cv2
import numpy as np
import pyautogui
import pytesseract
import difflib
import time
import re
import ctypes

def mostrar_quadrado(coordenadas, duracao=1):
    x, y = coordenadas
    largura = 100
    altura = 100

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "white")
    root.geometry(f"{largura*2}x{altura*2}+{x-largura}+{y-altura}")

    canvas = tk.Canvas(root, width=largura*2, height=altura*2, bg="white", highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(0, 0, largura*2, altura*2, outline="red", width=3)

    def fechar():
        root.destroy()

    root.after(int(duracao * 1000), fechar)
    root.mainloop()


def buscar_e_clicar(texto_busca=None, ocorrencia=1, horizontal=0, vertical=0, click=1, coordenadas=None, max_tentativas=10, debug=False, return_all_text=False):
    def prepararImagens(imagem):
        imagemArray = np.array(imagem)

        imagemCinza = cv2.cvtColor(imagemArray, cv2.COLOR_BGR2GRAY)
        imagemCinza = cv2.resize(imagemCinza, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        imagemCinza = cv2.normalize(imagemCinza, None, 0, 255, cv2.NORM_MINMAX)

        _, imagemBinaria = cv2.threshold(imagemCinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        imagemInvertida = cv2.bitwise_not(imagemBinaria)

        return [
            Image.fromarray(imagemCinza),
            Image.fromarray(imagemBinaria),
            Image.fromarray(imagemInvertida)]

    def tentarDeteccao(imagem, config):
        try:
            return pytesseract.image_to_data(imagem, lang="por", output_type=pytesseract.Output.DICT, config=config)
        except Exception as e:
            print(f"Erro na detecção: {e}")
            return None

    def normalizarTexto(texto):
        if not texto:
            return ""

        texto = texto.lower()
        texto = texto.replace("ç", "c")
        texto = texto.replace("ã", "a")
        texto = texto.replace("á", "a")
        texto = texto.replace("à", "a")
        texto = texto.replace("â", "a")
        texto = texto.replace("é", "e")
        texto = texto.replace("ê", "e")
        texto = texto.replace("í", "i")
        texto = texto.replace("ó", "o")
        texto = texto.replace("ô", "o")
        texto = texto.replace("õ", "o")
        texto = texto.replace("ú", "u")

        return "".join(
            c for c in texto
            if c.isalnum() or c in "., "
        ).strip()

    def textosParecidos(textoDetectado, textoBusca):
        textoDetectadoNormalizado = normalizarTexto(textoDetectado)
        textoBuscaNormalizado = normalizarTexto(textoBusca)

        if not textoDetectadoNormalizado or not textoBuscaNormalizado:
            return False

        if textoBuscaNormalizado in textoDetectadoNormalizado:
            return True

        similaridade = difflib.SequenceMatcher(None, textoDetectadoNormalizado, textoBuscaNormalizado).ratio()

        return similaridade >= 0.70

    def calcularPosicaoClique(x, y, largura, altura, bbox):
        if bbox:
            posicaoX = bbox[0] + x + (largura // 2) + horizontal
            posicaoY = bbox[1] + y + (altura // 2) + vertical
        else:
            posicaoX = x + (largura // 2) + horizontal
            posicaoY = y + (altura // 2) + vertical

        return posicaoX, posicaoY

    todosTextos = []

    if coordenadas:
        xCentro, yCentro = coordenadas

        larguraBbox = 300
        alturaBbox = 180

        threading.Thread(target=mostrar_quadrado, args=(coordenadas, 1), daemon=True).start()

        bbox = (
            xCentro - larguraBbox // 2,
            yCentro - alturaBbox // 2,
            xCentro + larguraBbox // 2,
            yCentro + alturaBbox // 2)
    else:
        bbox = None

    configs = [
        "--oem 3 --psm 6",
        "--oem 3 --psm 11",
        "--oem 3 --psm 12"]

    textoBuscaNormalizado = normalizarTexto(texto_busca) if texto_busca else ""

    for tentativa in range(max_tentativas):
        if debug:
            print(f"Tentativa {tentativa + 1} de {max_tentativas}")

        screenshot = ImageGrab.grab(bbox=bbox)

        imagensParaTestar = prepararImagens(screenshot)

        for imagemTratada in imagensParaTestar:
            for config in configs:
                textoTela = tentarDeteccao(imagemTratada, config)

                if not textoTela:
                    continue

                palavrasDetectadas = textoTela["text"]

                coordenadasDetectadas = list(zip(
                    textoTela["left"],
                    textoTela["top"],
                    textoTela["width"],
                    textoTela["height"]))

                textosValidos = [
                    palavra for palavra in palavrasDetectadas
                    if palavra and palavra.strip()]

                todosTextos.extend(textosValidos)

                if debug:
                    print(f"Textos detectados: {textosValidos}")

                if not texto_busca:
                    continue

                textoCompletoTela = normalizarTexto(" ".join(textosValidos))

                if debug:
                    print(f"Texto completo OCR: {textoCompletoTela}")

                ocorrenciasEncontradas = []

                # Primeiro tenta achar a frase completa no OCR
                if textoBuscaNormalizado in textoCompletoTela:
                    if debug:
                        print(f'Frase "{texto_busca}" encontrada no texto completo.')

                    # Como a frase foi encontrada no texto completo,
                    # clica na primeira palavra parecida com a primeira palavra da busca
                    primeiraPalavraBusca = texto_busca.split()[0]

                    for i, palavraDetectada in enumerate(palavrasDetectadas):
                        if textosParecidos(palavraDetectada, primeiraPalavraBusca):
                            x, y, largura, altura = coordenadasDetectadas[i]
                            ocorrenciasEncontradas.append((x, y, largura, altura, palavraDetectada))

                # Se não achou frase completa, tenta por palavra
                if not ocorrenciasEncontradas:
                    palavrasBusca = texto_busca.split()

                    for palavraBusca in palavrasBusca:
                        for i, palavraDetectada in enumerate(palavrasDetectadas):
                            if not palavraDetectada or not palavraDetectada.strip():
                                continue

                            if textosParecidos(palavraDetectada, palavraBusca):
                                x, y, largura, altura = coordenadasDetectadas[i]

                                ocorrenciasEncontradas.append((x, y, largura, altura, palavraDetectada))

                if len(ocorrenciasEncontradas) >= ocorrencia:
                    x, y, largura, altura, palavraDetectada = ocorrenciasEncontradas[ocorrencia - 1]

                    posicaoX, posicaoY = calcularPosicaoClique(x, y, largura, altura, bbox)
                    pyautogui.moveTo(posicaoX, posicaoY)

                    if click == 2:
                        pyautogui.doubleClick()
                    else:
                        pyautogui.click()

                    print(
                        f'Clique realizado em "{texto_busca}". '
                        f'O OCR detectou "{palavraDetectada}" em ({posicaoX}, {posicaoY}).')

                    if return_all_text:
                        return todosTextos

                    return True

        time.sleep(0.2)

    print(f'Não encontrou "{texto_busca}" após {max_tentativas} tentativas.')

    if debug and todosTextos:
        print("Textos capturados durante todas as tentativas:")
        print(todosTextos)

    if return_all_text:
        return todosTextos

    return False