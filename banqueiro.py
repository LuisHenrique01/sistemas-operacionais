import os

def main():
    qtd_processos = int(input('Quantidade de processos: '))
    qtd_recursos = int(input('Quantidade de recursos: '))
    tracos()
    recursos_max = ler_recursos_maximos(qtd_recursos)
    tracos()
    matriz_demanda = []
    for i in range(qtd_processos):
        matriz_demanda.append(ler_demanda_processo(qtd_recursos, i))
    tracos()
    matriz_alocados = []
    for i in range(qtd_processos):
        matriz_alocados.append(ler_alocao_processo(qtd_recursos, i))
    
    recursos_disponiveis = calcular_recursos_disponiveis(recursos_max, matriz_alocados)
    matriz_necessidades = calcular_necessidades(matriz_demanda, matriz_alocados)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    mostrar_dados(matriz_demanda, recursos_max, matriz_alocados, matriz_necessidades, recursos_disponiveis)
    
    necessidades_faltando = sum([sum(linha) for linha in matriz_necessidades])
    while necessidades_faltando != 0:
        processo_escolhido = escolher_processo(matriz_necessidades, matriz_demanda,recursos_disponiveis)
        if processo_escolhido == 'DEADLOCK':
            print('DEADLOCK!! DEADLOCK!! DEADLOCK!!')
            break
        executa_processo(processo_escolhido, matriz_alocados, matriz_necessidades, recursos_disponiveis)
        mostrar_dados(matriz_demanda, recursos_max, matriz_alocados, matriz_necessidades, recursos_disponiveis)
        finalizar_processo(processo_escolhido, matriz_alocados, recursos_disponiveis)
        mostrar_dados(matriz_demanda, recursos_max, matriz_alocados, matriz_necessidades, recursos_disponiveis)
        os.system('cls' if os.name == 'nt' else 'clear')
        necessidades_faltando = sum([sum(linha) for linha in matriz_necessidades])
    print('TODOS OS PROCESSOS FORAM EXECUTADOS!\n')
    mostrar_dados(matriz_demanda, recursos_max, matriz_alocados, matriz_necessidades, recursos_disponiveis)
        
        
def finalizar_processo(processo_escolhido, matriz_alocados, recursos_disponiveis):
    for i, valor in enumerate(matriz_alocados[processo_escolhido]):
        recursos_disponiveis[i] += valor
        matriz_alocados[processo_escolhido][i] = 0
    
    
def executa_processo(processo_escolhido, matriz_alocados, matriz_necessidades, recursos_disponiveis):
    for i, valor in enumerate(matriz_necessidades[processo_escolhido]):
        matriz_alocados[processo_escolhido][i] += valor
        matriz_necessidades[processo_escolhido][i] = 0
        recursos_disponiveis[i] -= valor
    
    
def escolher_processo(matriz_necessidades, matriz_demanda, recursos_disponiveis):
    soma_recursos = []
    for p, linha in enumerate(matriz_necessidades):
        pode_executar = False
        for i, coluna in enumerate(linha):
            if recursos_disponiveis[i] >= coluna:
                pode_executar = True
            else:
                pode_executar = False
                break
        if pode_executar and sum(linha) != 0:
            soma_recursos.append((sum(matriz_demanda[p]), p))
    if len(soma_recursos) == 0:
        return 'DEADLOCK'
    return min(soma_recursos, key=lambda x: x[0])[1]

    
def calcular_necessidades(matriz_demanda, matriz_alocados):
    mn = [[v_md-v_ma for v_md, v_ma in zip(l_md, l_ma)] for l_md, l_ma in zip(matriz_demanda, matriz_alocados)]
    return mn
    
    
def calcular_recursos_disponiveis(recursos_max, matriz_alocados):
    rd = [rm-sum(linha[i] for linha in matriz_alocados) for i, rm in enumerate(recursos_max)]
    return rd
    
    
def ler_alocao_processo(qtd_recursos, i):
    p = list(map(int, input(f'Aloção de recursos do processo P{i+1}: ').split()))
    if len(p) == qtd_recursos:
        return p
    else:
        print('Corrija os recursos, tamanho do vetor incompatível.\n')
        return ler_alocao_processo(qtd_recursos)
    
    
def ler_demanda_processo(qtd_recursos, i):
    p = list(map(int, input(f'Demanda máxima de recursos do processo P{i+1}: ').split()))
    if len(p) == qtd_recursos:
        return p
    else:
        print('Corrija os recursos, tamanho do vetor incompatível.\n')
        return ler_demanda_processo(qtd_recursos)


def ler_recursos_maximos(qtd_recursos):
    recursos_max = tuple(map(int, input(f'Capacidade máxima dos {qtd_recursos} em ordem, exemplo(2 2 2):\n').split()))
    if len(recursos_max) == qtd_recursos:
        return recursos_max
    else:
        print('Corrija os recursos máximos, tamanho do vetor incompatível.\n')
        return ler_recursos_maximos(qtd_recursos)


def tracos(qtd=80, tituloRodape=False):
    if tituloRodape:
        print(f"+{'-'*qtd}+")
    else:
        print(f"|{'-'*qtd}|")


def print_vetor(vetor, nome):
    print("Tabela de", nome, '\n')
    tam = len(vetor)
    tracos(tam*6, tituloRodape=True)
    print(f"|{'{:^6}'*tam}|".format(*[f'R{i+1}' for i in range(tam)]))
    tracos(tam*6)
    print(f"|{'{:^6}'*tam}|".format(*vetor))
    tracos(tam*6, tituloRodape=True)
    print()
    
    
def print_matriz(matriz, nome):
    print("Tabela de", nome, '\n')
    tam = len(matriz[0]) + 1
    tracos(tam*6, tituloRodape=True)
    print(f"|{'{:^6}'*tam}|".format(*['--' if i==0 else f'R{i}' for i in range(tam)]))
    tracos(tam*6)
    for i, linha in enumerate(matriz):
        print(f"|{'P%d'%(i+1):^6}{'{:^6}'*(tam-1)}|".format(*linha))
    tracos(tam*6, tituloRodape=True)
    print()
    
    
def mostrar_dados(matriz_demanda, recursos_max, matriz_alocados, matriz_necessidades, recursos_disponiveis):
    print_matriz(matriz_demanda, 'demanda')
    print_vetor(recursos_max, 'recursos máximos')
    print_matriz(matriz_alocados, 'alocados')
    print_matriz(matriz_necessidades, 'necessidades')
    print_vetor(recursos_disponiveis, 'recursos disponíveis')
    input('pressione Enter para continuar')
    
    
if __name__ == "__main__":
    main()