from random import randint

'''
En el problema del 3 en raya se aplicará un Forward Search 
se utilizará para definir los estados una función step que cambiará el estado del sistema simulando ser 
el otro jugador que tendrá su propia politica más básica definida por simples reglas 
'''
S = {}#una variable que se usará de apoyo para representar el estado del tablero, los 0 son vacios que se irán llenando con x , o
U = {}
#set de ACIONES es poner o no poner en la ubicación
A = {}
d = 10
for i in range(0, 3):
    for j in range(0, 3):
        A[i,j] = (i,j)

def fin_juego(s):
    recompensa = {('x'): 100, ('o'): -100}
    for val, idx in enumerate(recompensa):
        for i in range(0, 3):
            if([s[i,0], s[i,1], s[i,2]]==[idx, idx, idx]):
                return True

        if(s[0,0]==idx and s[1,1]==idx and s[2,2]==idx):
            return True
        if(s[0,2]==idx and s[1,1]==idx and s[2,0]==idx):
            return True
    if(0 in s.values()):
        return 'Tie'

#Nota: S no se usa para representar por estados a las posiciones en el tablero, sino estados del tablero (empieza todo libre)
for i in range(0, 3):
    for j in range(0, 3):
        S[i, j] = 0

for i in range(0, 3):
    for j in range(0, 3):
        U[i, j] = 0

def step(s, a):
    #verificar si no se ha bloqueado el tablero o se sigue jugando
    if(fin_juego(s)==True): 
        print("Terminó en: ", s, "-", R(s))

        for i in range(0, 3):
            for j in range(0, 3):
                s[i, j] = 0
        return s
    if(s[a]==0):
        l, k = a
        s[l,k] = 'x' 
    else:
        #si en la ubicación donde quiere poner está ocupada debe elegir otra según este criterio
        for i in range(0, 2):
            for j in range(0, 2):
                if(s[i,j]==0):
                    s[i,j] = 'x'

    #oponente coloca su jugada según esta estrategia
    prob = randint(1,2)
    if(prob==1):
        for i in range(0, 2):
            for j in range(0, 2):
                if(s[i,j]==0):
                    s[i,j] = 'o'
                    return s
    else:
        for i in range(2, 0, -1):
            for j in range(2, 0, -1):
                if(s[i,j]==0):
                    s[i,j] = 'o'
                    return s
    return s

def R(s):
    #verificar los 3 en raya primero para el agente y luego para el oponente
    recompensa = {('x'): 100, ('o'): -100}
    for k, (idx,val) in enumerate(recompensa.items()):
        for i in range(0, 3):
            if([s[i,0], s[i,1], s[i,2]]==[idx, idx, idx]):
                return val

        if(s[0,0]==idx and s[1,1]==idx and s[2,2]==idx):
            return val
        if(s[0,2]==idx and s[1,1]==idx and s[2,0]==idx):
            return val
    #verificar si se ha trancado, se pone -10 porque tampoco nos interesa empatar todo el tiempo
    if(fin_juego(s)=='Tie'):
        return -10

    return 0



#Algoritmo para resolver el MDP: 
#Forward Search
print("*************Forward Search****************")


def lookahead(U, s, a, A):
    return R(step(s, a))

def forward_search(U, s, d, A):
    U_ = {}
    if(d <=0):
        return (0, 0) #(0, U[s])
    
    best = (0, float('-inf')) #(0, U[s])
    a_, u_ = forward_search(U, s, d-1, A)

    for a in A:
        u = lookahead(u_, s, a, A)
        _, best_u = best
        if(u > best_u):
            best = (a, u)
    
    return best

print(forward_search(U, S, d, A)) # <--- ejecutar forward search