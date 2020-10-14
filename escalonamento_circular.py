def main():
    quantum = int(input('Quantum: '))
    tempo_troca = int(input('Tempo de troca de contexto: '))
    qtd_processos = int(input('Quantidade de processos: '))
    tempos_processos = [int(input(f'Tempo de execução do processo P{i+1}: ')) for i in range(qtd_processos)]
    turnaround = [0 for i in range(qtd_processos)]
    tempos_espera = [[] for i in range(qtd_processos)]
    processo_vez = 0
    aux_troca = 0
    turnaround_anterior = 0
    tempo_de_uso = 0
    
    while sum(tempos_processos) > 0:
        if len(tempos_espera[processo_vez]) > 0:
            tempos_espera[processo_vez].append((turnaround_anterior+aux_troca)-(tempo_de_uso+
                                                tempos_espera[processo_vez]
                                                [len(tempos_espera[processo_vez])-2]))
        else:
            tempos_espera[processo_vez].append(turnaround_anterior+aux_troca)
        tempo_de_uso = executar_processo(processo_vez, tempos_processos, quantum)
        turnaround[processo_vez] = tempo_de_uso + aux_troca + turnaround_anterior
        aux_troca = tempo_troca
        turnaround_anterior = turnaround[processo_vez] 
        processo_vez = qual_processo(processo_vez, tempos_processos)
    
    for p, tempo in enumerate(turnaround):
        print(f'Tempo de turnaround do P{p+1}: {tempo}')
    print(f'\nTempo médio de turnaround: {sum(turnaround)/qtd_processos:.2f}\n')
    
    for p, tempo in enumerate(tempos_espera):
        print(f'Tempo de espera do P{p+1}: {sum(tempo)}')
    print(f'\nTempo médio de espera: {sum([sum(tempo) for tempo in tempos_espera])/qtd_processos:.2f}')
        
        
def qual_processo(vez_processo, tempos_processos):
    proximo = vez_processo + 1
    if sum(tempos_processos) <= 0:
        return 0
    if proximo >= len(tempos_processos):
        proximo = 0
    if tempos_processos[proximo] <= 0:
        return qual_processo(proximo, tempos_processos)
    else:
        return proximo
        
        
def executar_processo(vez_processo, tempos_processos, quantum):
    if tempos_processos[vez_processo] < quantum:
        tempo_de_uso = tempos_processos[vez_processo]
        tempos_processos[vez_processo] -= tempo_de_uso
        return tempo_de_uso
    tempo_de_uso = quantum
    tempos_processos[vez_processo] -= tempo_de_uso
    return tempo_de_uso
    
    
if __name__ == "__main__":
    main()