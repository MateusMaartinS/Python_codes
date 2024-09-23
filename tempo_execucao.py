from datetime import datetime


def calcular_tempo_execucao(func, *args, **kwargs):
    tempo_inicio = datetime.now()
    resultado = func(*args, **kwargs)
    tempo_fim = datetime.now()
    tempo_execucao = tempo_fim - tempo_inicio
    
    # formatar texto
    largura_total = 28
    largura_interna = largura_total - 11

    linha_superior = "|¯¯ TEMPO DE EXECUÇÃO ¯¯|".center(largura_total)
    linha_inferior = f"|__ {str(tempo_execucao).center(largura_interna)} __|".center(largura_total)
    
    print(linha_superior)
    print(linha_inferior)
    
    return resultado
