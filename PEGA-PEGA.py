import time
from tkinter import *
import pyautogui
import random
import threading


def tela():
    janela = Tk()
    janela. title('PEGA-PEGA')
    posicao_janela = "+780+470"
    janela.geometry("300x100" + posicao_janela)

    pegar = Button(janela, text="Peguei!", command=lambda:peguei(janela))
    pegar.pack(side=LEFT, padx=40)

    cansei = Button(janela, text="Cansei!", command=lambda:parar(janela))
    cansei.pack(side=RIGHT, padx=40)

    janela.mainloop()


def peguei(janela):
    posicao_random = f"+{random.randint(0, 1600)}+{random.randint(0, 700)}"
    janela.geometry("300x100" + posicao_random)

def parar(janela):
    janela.destroy()

tela()