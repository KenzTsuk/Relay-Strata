o = str(["plasma", "casco", "ethos"])
i = 0
for a in o:
    if a in "aeiouAEIOU":
        i += 1
print(f"{i}")
print(f"{a}")

s = ["carlos", "caca", "jojo"]
s.append(["jaja", "jojo"]) #.append() adiciona um elemento ao final da lista.
s.count("jojo") #.count() faz uma contagem de vezes que um elemento aparece na lista.
s.remove("carlos") #.remove() remove o primeiro elemento citado no parentes da lista.
s.pop() #.pop() remove o ultimo elemento da lista. 
s.reverse() #.reverse() Inverte a ordem dos elementos da lista.
s.sort() # .sort() Organiza em ordem crescente ou alfabetica.
s.insert(1, "bb") #.insert() insere um elemento antes do primeiro elemento no parentes.
print(f"{s}")

l = ["caca", "coco"]
for  f in l :
    print(f.upper()) #Exibe os elementos em caixa alta.
    
y = [2, 3, 4]
dob = []
for m in y:
    dob.append(m*2)
print(dob)