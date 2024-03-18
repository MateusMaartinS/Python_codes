from pathlib import Path
import os

def localizar_pdf(caminho):


    caminho_pasta = Path(caminho)

    if not caminho_pasta.is_dir():
        print("Caminho passado não é um diretório válido")
        return

    for arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = caminho_pasta / arquivo

        if caminho_arquivo.is_file() and caminho_arquivo.suffix.lower() == '.pdf':
            print("arquivo encontrado:", caminho_arquivo)