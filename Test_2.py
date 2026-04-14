import time
while True:
    print("-- Escolha qual atividade gostaria de ver --")
    time.sleep(1)
    print("1. Calculadora")
    time.sleep(1)
    print("2. Curso")
    time.sleep(1)
    print("3. Peso")
    time.sleep(1)
    print("4. Senha")
    time.sleep(1)
    print("5. Show")
    time.sleep(1)
    print("6. Encerrar Programa")
    
    att = input("Digite sua Opção:\n")
    
    if att == "1" :
        while True:
            print("-- Calculadora --")
            time.sleep(1)
            print("1. Adiçao")
            time.sleep(1)
            print("2. Subtraçao")
            time.sleep(1)
            print("3. Multiplicaçao")
            time.sleep(1)
            print("4. Diviçao")
            time.sleep(1)
            print("5. Voltar")
            
            op = input("Escolha uma opçao de 1-5:\n")
            
            if op == "1":
                p1 = eval(input("Insira um valor:\n"))
                p2 = eval(input("Insira outro valor:\n"))
                time.sleep(1)
                print(f"{p1} + {p2} = {p1 + p2}")
                time.sleep(3)
                
            elif op == "2":
                minu = eval(input("Insira um valor:\n"))
                sub = eval(input("Insira outro valor:\n"))
                time.sleep(1)
                print(f"{minu} - {sub} = {minu - sub}")
                time.sleep(3)
                
            elif op == "3":
                fat1 = eval(input("Insira um valor:\n"))
                fat2 = eval(input("Insira outro valor:\n"))
                time.sleep(1)
                print(f"{fat1} x {fat2} = {fat1 * fat2}")
                time.sleep(3)
                
            elif op == "4":
                divi = eval(input("Insira um valor:\n"))
                dive = eval(input("Insira outro valor:\n"))
                time.sleep(1)
                print(f"{divi} / {dive} = {divi / dive}")
                time.sleep(3)
                
            elif op == "5":
                print("Voltando...")
                break
                
            else:
                print("Noçao Invalida!")
                time.sleep(2)
            print("Voltando...")
            
    elif att == "2":
        curso = str(input("Digite seu curso:\n")).lower().strip()
        
        if "engenharia" in curso:
            print("Acesso Permitido!")
        else :
            print("Acesso Negado.")
            
    elif att == "3":
        peso = float(input("Digite seu peso em Kg:\n"))
        altura = float(input("Digite sua altura em M:\n"))
        
        imc = peso / (altura**2)
        print(f"{imc}")
        
        if imc <18.5:
            print("Baixo Peso.")
        elif imc <25:
            print("Peso Adequado.")
        elif imc <30:
            print("Sobrepeso.")
        elif imc <35:
            print("Obesidade Grau 1.")
        elif imc <40:
            print("Obesidade Grau 2.")
        else :
            print("Obesidade Grau 3.")
            
    elif att == "4":
        user_c = "nycolas"
        sen_c = "kasus"
        
        user_i = input("User:\n").lower().strip()
        sen_i = input("Passaword:\n").lower().strip()
        
        if user_i == user_c and sen_i == sen_c :
            print("OwO")
        elif user_i != user_c :
            print("Escreve seu nome direito, burro.")
        else :
            print("Esqueçeu a senha bb??")
            
    elif att == "5":
        continuar = "s"
        while continuar == "s":
            sc = ["Ana Clara", "Paulo Sergio"]
            nome = str(input("Nome:\n"))
            idade = int(input("Idade:\n"))
            
            if nome in sc :
                print("Acesso Permitido!")
            elif idade >= 16 :
                print("Acesso Permitido!")
            else :
                print("Acesso Negado.")
            continuar = input("Adicionar outra pessoa? [s/n]\n").lower().strip()
        print("Voltando...")
        
    elif att == "6":
        print("Bye Bye UwU...")
        break