a = input("Digite seu nome:")
b = int(input(f"Digite sua idade:"))
c = str(input(f"Digite seu genero:"))
d = float(input(f"Seu nivel de felicidade [0.1 - 1]:"))

if a[0] == "N" and "Masculino" or "Homem" in c:
    print(f"Certeza que seu nome e: {a}")
    if b >= 18 and d >= 0.5:
        print(f"Bora pro puteiro")
    else:
        print(f"Vai se fuder criança do carai")
else :
    print(f"voce e um indigente")
if d <= 0.3:
    print(f"Tu ta chato pra caralho hoje em")
else :
    print(f"Cheiro de peneu queimado, carburador furado")
if 'y' in a and 's' in a[6]:
    print (len(a))
if len(a) >= 7:
    print(3*a)
a += ' ' + str(input(f"Digite seu sobrenome:\n"))
print(a)