import numpy as np

#Definición del MDP
# bajo=0  , medio=1  , alto=2   ,  superior=3
S = np.array([0,1,2,3])
A = np.array([0,1,2]) # mover_lento=1   ,   mover_rapido=2 ,   no_mover=0
pi = np.array([0 for i in S]) #la politica de partida será no mover las ruedas nunca
U = np.array([0 for i in S]) #inicialización de la utilidad de los estados
gamma = 1
#pi = np.array([1,0,2,1])
#se define 'recompensas' que se usará más adelante en R(s,a)
recompensas = {
    (0,0): 0,
    (1,0): 3,
    (2,0): 3,
    (0,1): -1,
    (0,2): -2,
    (1,1): 2,
    (1,2): 1,
    (2,1): 2,
    (2,2): 1,
    (3,1): 2,
    (3,2): 1
}

def R(s, a):
    #se define como 1 si sube al mover las ruedas y 0 si baja al mover las ruedas
    if(a==1):
        res = np.random.choice([0,1], p=[0.7, 0.3])
        if(s!=3 and res==1):
            s +=1
        elif(s!=0 and res==0):
            s-=1 
    elif(a==2):
        res = np.random.choice([0, 2], p=[0.3, 0.7])
        if(s!=3 and res==1):
            s +=1
        elif(s!=0 and res==0):
            s-=1 
    else:
        res = 0
        if(s!=0):
            s-=1
        else:
            s=0
    return recompensas[s,res]
    

#Matriz de Transicion T(s, a, s')
T = {
    (0, 0, 0): 1,
    (0, 1, 0): 0.7,
    (0, 2, 0): 0.3,
    (0, 1, 1): 0.3,
    (0, 2, 1): 0.7, 
    (1, 1, 2): 0.3,
    (1, 1, 0): 0.7,
    (1, 2, 2): 0.7,
    (1, 2, 0): 0.3,
    (2, 1, 0): 0.7,
    (2, 1, 3): 0.3,
    (2, 2, 0): 0.3,
    (2, 2, 3): 0.7,
    (3, 1, 3): 0.3,
    (3, 2, 3): 0.7, 
    (3, 1, 0): 0.7,
    (3, 2, 0): 0.3,
    (2, 0, 1): 1,
    (1, 0, 0): 1,
    (3, 0, 2): 1
}


#Algoritmos 
#Lookahead

def lookahead(U, s, a, T, S,gamma):
    return R(s,a)+ gamma*sum(T[s,a,s1]*U[s1] for s1 in S if (s,a,s1) in T)

# Iteracion de valores

def backup(S,T,A, gamma,U, s):
    return max(lookahead(U, s, a, T,  S, gamma) for a in A)

def greedy(S, T, U, A, gamma, s):
    u_ = 0
    a_ = 0
    for a in A:
        u = lookahead(U, s, a, T, S, gamma)
        if (u >= u_):
            u_ = u
            a_ = a
    return a_, u_




def iteracion_valores(S, T, U, A, gamma, k_max):
    U = [0 for s in S]
    for k in range(0, k_max):
        U = [backup(S,T,A, gamma, U, s) for s in S]
    return U

print(iteracion_valores(S, T, U, A, gamma, 5)) # <----- ejecutar iteracion de valores

#Encontrar la politica optima

U = iteracion_valores(S, T, U, A, gamma, 5)

def optimizar(S, T, U, A, gamma):
    pi = [0 for s in S]
    for s in S:
       pi[s] = greedy(S, T, U, A, gamma, s)
    return pi

print(optimizar(S, T, U, A, gamma)) # <---- ejecutar optimizar
    