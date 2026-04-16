from random import randint

while True:
    print(f"\n---Escolha qual atividade deseja vizualizar---")
    print(f"1. Secret Number")
    print(f"2. UniRico")
    print(f"3. Robo do tempo")
    
    opcao = int(input(f"Digite sua escolha:\n"))
    
    if opcao == 1:
        
        print(f"Hehe Vamos jogar, adivinhe o numero que estou pensando.")
        ns = randint(1,100)
        tv = 0
        
        while True:
            try:
                palpite = int(input(f"\nAdivinhe o numero secreto de (1-100)\n"))
                
                if palpite<1 or palpite>100 :
                    print(f"\nDigite um numero de (1-100).")
                    
                elif ns == palpite:
                    print(f"\nParabens, voce acertou o numero.")
                    print(f"\nOhh, voce precisou de {tv} Tentativas.")
                    break
                    
                elif palpite > ns:
                    print(f"Mais pra Baixo Patrao.")
                    tv += 1
                    
                else:
                    print(f"Mais pra Cima Xuxu.")
                    tv += 1
                    
            except ValueError:
                print(f"\nDeixa de ser burro, digita um numero INTEIRO de 1 - 100. ")
                
    elif opcao == 2:
        
        print(f"Voce escolheu Estudar?? Que nojo cara.")
        eng = ["eletrica", "mecatronica", "mecanica"]
        s_eng = 0
        
        while s_eng<35:
            try:
                
                mod = str(input(f"\nEm qual modalidade voce esta matriculado?\n")).lower().strip()
                
                if mod in eng:
                    print(f"Acesso Liberado.")
                    cont = str(input(f"Ainda tem alunos para entrar? (s/n)\n"))
                    s_eng += 1
                    
                    if cont == "n":
                        break
                    else:
                        print(f"Esperando proximo aluno....")
                
                else:
                    print(f"Acesso Negado.")
                    print(f"\nEsperando proximo aluno....")
                    
            except ValueError:
                print(f"Digita a sua Modalidade de engenharia.")
                
        print(f"Temos {s_eng} presentes.")        