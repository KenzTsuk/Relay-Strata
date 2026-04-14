import time
import random
baralho = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Q", "J", "K"]
naipes = ["Ouros", "Espadas", "Copas", "Paus"]
jogadores = []

while True:

    try:
        print("Maximo de Jogadores: 4")
        qj = int(input("Quantos jogadores teremos na mesa:\n"))
        qa = [2, 3, 4]
        qi = [0, 1]
        
        if qj in qa:
            break
    
        elif qj in qi:
            print("Jogadores Insuficientes para começar o jogo.")
    
        elif qj >= 5:
            print("Jogadores demais na mesa, Maximo de 4 jogadores.")
            continue

    except ValueError:
        print("Valor Invalido!")
        
while True:
    
    while len(jogadores) < qj:
        user = str(input("Insira o Jogador:\n")).strip().lower()
        jogadores.append(user)
        print(f"Jogadores\n{jogadores}")
        
    if len(jogadores) == qj:
        break
    break

while True:
    print("Escolha o jogo:\n 1. BlackJack\n 2. Poker")
    jogo = int(input())

    if jogo == 1:
        break

    elif jogo == 2:
        break
        
    else:
        print("Esse jogo nao existe.")