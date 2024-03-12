from tkinter import *
from tkinter import ttk

# Cores
color1 = "#202020"
color2 = "#ffffff"
color3 = "#323232"
color4 = "#3c3c3c"
color5 = "#9932CC"
color6 = "#4B0082"
color7 = "#000000"

# Configuração da janela
tela = Tk()

tela.title("Calculadora")
tela.geometry("323x395")
tela.config(bg=color1)

# Frames
frameDisplay = Frame(tela, width=323, height=120, bg=color1)
frameDisplay.grid(row=0, column=0)

frameTeclado = Frame(tela, width=323, height=250, bg=color1)
frameTeclado.grid(row=1, column=0)

frameRodape = Frame(tela, width=323, height=15, bg=color1)
frameRodape.grid(row=2, column=0)


# Funções
mostrarValor = StringVar()
valor = ''

def inputValue(event):
   global valor
   
   valor = valor + str(event)
   
   #Exibe o resultado na tela
   mostrarValor.set(valor)


def calculate():
   global valor
   
   result = eval(valor)
   mostrarValor.set(str(result))
   valor = str(result)


def clean():
   global valor
   
   valor = ''
   mostrarValor.set('')
   

# Label
labelScreen = Label(frameDisplay, textvariable=mostrarValor, bg=color1, fg=color2, font=("Ivy 24 bold"), width=16, padx=8, pady=40, justify="right", anchor="e", relief="flat")
labelScreen.pack()

versao = Label(frameRodape, text="V.: 1.3.3", bg=color1, fg=color2, font=("Ivy 9"), width=44, padx=8, justify="right", anchor="e")
versao.pack()



Bt_limpar = Button(frameTeclado, command = clean, text="C", width=17, height=2, bg=color3, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color4, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_limpar.place(x=0, y=0)

Bt_porcent = Button(frameTeclado, command = lambda: inputValue('%'), text="%", width=8, height=2, bg=color3, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color4, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_porcent.place(x=162, y=0)

Bt_div = Button(frameTeclado, command = lambda: inputValue('/'), text="/", width=8, height=2, bg=color3, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color4, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_div.place(x=243, y=0)

Bt_num7 = Button(frameTeclado, command = lambda: inputValue('7'), text="7", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num7.place(x=0, y=49)

Bt_num8 = Button(frameTeclado, command = lambda: inputValue('8'), text="8", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num8.place(x=81, y=49)

Bt_num9 = Button(frameTeclado, command = lambda: inputValue('9'), text="9", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num9.place(x=162, y=49)

Bt_mult = Button(frameTeclado, command = lambda: inputValue('*'), text="x", width=8, height=2, bg=color3, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color4, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_mult.place(x=243, y=49)


Bt_num4 = Button(frameTeclado, command = lambda: inputValue('4'), text="4", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num4.place(x=0, y=98)

Bt_num5 = Button(frameTeclado, command = lambda: inputValue('5'), text="5", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num5.place(x=81, y=98)

Bt_num6 = Button(frameTeclado, command = lambda: inputValue('6'), text="6", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num6.place(x=162, y=98)

Bt_sub = Button(frameTeclado, command = lambda: inputValue('-'), text="-", width=8, height=2, bg=color3, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color4, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_sub.place(x=243, y=98)


Bt_num1 = Button(frameTeclado, command = lambda: inputValue('1'), text="1", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num1.place(x=0, y=147)

Bt_num2 = Button(frameTeclado, command = lambda: inputValue('2'), text="2", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num2.place(x=81, y=147)

Bt_num3 = Button(frameTeclado, command = lambda: inputValue('3'), text="3", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num3.place(x=162, y=147)

Bt_soma = Button(frameTeclado, command = lambda: inputValue('+'), text="+", width=8, height=2, bg=color3, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color4, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_soma.place(x=243, y=147)


Bt_num0 = Button(frameTeclado, command = lambda: inputValue('0'), text="0", width=17, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_num0.place(x=0, y=196)

Bt_ponto = Button(frameTeclado, command = lambda: inputValue('.'), text=".", width=8, height=2, bg=color4, fg=color2, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color3, activeforeground=color2, highlightthickness=0, borderwidth=0)
Bt_ponto.place(x=162, y=196)

Bt_result = Button(frameTeclado, command = calculate, text="=", width=8, height=2, bg=color5, fg=color7, font=("Ivy 11 bold"), relief="flat", overrelief="raised", activebackground=color6, activeforeground=color7, highlightthickness=0, borderwidth=0)
Bt_result.place(x=243, y=196)


tela.mainloop()