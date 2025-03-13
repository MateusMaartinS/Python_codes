from datetime import datetime


def calcularTempoExecucao(func, *args, corLog='default', **kwargs):
    cores = {
        'default': '\033[0m',
        'vermelho': '\033[91m',
        'verde': '\033[92m',
        'amarelo': '\033[93m',
        'azul': '\033[94m',
        'magenta': '\033[95m',
        'ciano': '\033[96m',
    }
    corEscolhida = cores.get(corLog, cores['default'])
    
    tempoInicio = datetime.now()
    resultado = func(*args, **kwargs)
    tempoFim = datetime.now()
    tempoExecucao = str(tempoFim - tempoInicio)

    larguraTotal = max(len(tempoExecucao) + 8, 30)  
    titulo = " TEMPO DE EXECUÇÃO "
    
    linhaSuperior = f"{corEscolhida}╭{'─' * (larguraTotal - 2)}╮"
    linhaTitulo = f"│{titulo.center(larguraTotal - 2)}│"
    linhaMeio = f"│{tempoExecucao.center(larguraTotal - 2)}│"
    linhaInferior = f"╰{'─' * (larguraTotal - 2)}╯\033[0m"
    
    print(linhaSuperior)
    print(linhaTitulo)
    print(linhaMeio)
    print(linhaInferior)
    
    return resultado
