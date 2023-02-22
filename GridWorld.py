import numpy as np
from random import randrange
import matplotlib.pyplot as plt

# Definición del MDP

S = []
pi = {}
U = {}

for i in range(0, 10):
    for j in range(0, 10):
        S.append((i,j))
        pi[i,j] = randrange(4)
        U[i,j] = 0

#print(S)

A = np.array([0,1,2,3]) # arriba=0  ,  abajo=1   ,  derecha=2   ,  izquierda=3
gamma = 1

recompensa = {}

for i in S:
    if i ==(8,7):
        recompensa[i] = 10
    elif i ==(7,2):
        recompensa[i] = 3
    elif i==(3,5):
        recompensa[i] = -5
    elif i==(3,7):
        recompensa[i] = -10
    else:
        recompensa[i] = 0

def R(s, a):
    if(a==0):
        res = np.random.choice([0,1,2,3], p=[0.7, 0.1, 0.1, 0.1])
    elif(a==1):
        res = np.random.choice([0,1,2,3], p=[0.1, 0.7, 0.1, 0.1])
    elif(a==2):
        res = np.random.choice([0,1,2,3], p=[0.1, 0.1, 0.7, 0.1])
    elif(a==3):
        res = np.random.choice([0,1,2,3], p=[0.1, 0.1, 0.1, 0.7])
    i, j = s
    if(res==0 and j<9):
        s1 = (i, j+1)
    elif(res==1 and j>0):
        s1 = (i, j-1)
    elif(res==2 and i<9):
        s1 = (i+1, j)
    elif(res==3 and i>0):
        s1 = (i-1,j)
    else:
        return -1
    return recompensa[s1]

T = {}

for (i,j) in S:
    if((i,j)!=(8,7) and (i,j)!=(7,2) and (i,j)!=(3,5) and (i,j)!=(3,7)):
        T[(i,j), 0, (i,j+1)] = 0.7
        T[(i,j), 0, (i,j-1)] = 0.1
        T[(i,j), 0, (i+1,j)] = 0.1
        T[(i,j), 0, (i-1,j)] = 0.1

        T[(i,j), 1, (i,j+1)] = 0.1
        T[(i,j), 1, (i,j-1)] = 0.7
        T[(i,j), 1, (i+1,j)] = 0.1
        T[(i,j), 1, (i-1,j)] = 0.1

        T[(i,j), 2, (i,j+1)] = 0.1
        T[(i,j), 2, (i,j-1)] = 0.1
        T[(i,j), 2, (i+1,j)] = 0.7
        T[(i,j), 2, (i-1,j)] = 0.1

        T[(i,j), 3, (i,j+1)] = 0.1
        T[(i,j), 3, (i,j-1)] = 0.1
        T[(i,j), 3, (i+1,j)] = 0.1
        T[(i,j), 3, (i-1,j)] = 0.7
    else:
        num1 = np.random.choice([0,9])
        num2 = np.random.choice([0,9])
        T[(i,j), 0, (num1,num2)] = 1
        T[(i,j), 1, (num1,num2)] = 1
        T[(i,j), 2, (num1,num2)] = 1
        T[(i,j), 3, (num1,num2)] = 1

#Algoritmos para resolver el MDP: Iterative_policy_evaluation e Iteracion de valores

#se necesita definir la funcion Lookahead

def lookahead(U, s, a, T, S,gamma):
    return R(s,a) + gamma*sum(T[s,a,s1]*U[s1] for s1 in S if (s,a,s1) in T)
    
#Iterative_policy_evaluation
def evaluacion_iterativa(S, T, U, gamma, pi, k_max):
    for i in range(0, k_max):
        for s in S:
            U[s] = lookahead(U, s, pi[s], T, S, gamma)
                #print(U[s], ' - ', s, ' - ', pi[s])
    return U

#print(evaluacion_iterativa(S, T, U, gamma, pi, 10)) #  <--- ejecutar evaluacion iterativa

def graficar(data):
    fig, ax = plt.subplots(figsize=(12,12))
    ax.grid(False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    for (i,j), (k,l) in zip(S, data.items()):
        ax.text(i-0.5, j+0.5, f'{round(l[0], 2)}')
    plt.axis('off')
    plt.show()

#graficar(evaluacion_iterativa(S, T, U, gamma, pi, 50)) # <-----graficar resultado evaluacion iterativa

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
    for k in range(0, k_max):
        for s in S:
            U[s] = backup(S,T,A, gamma, U, s)
    return U

#print(iteracion_valores(S, T, U, A, gamma, 10)) # <--- ejecutar iteracion de valores

#graficar(iteracion_valores(S, T, U, A, gamma, 10)) # <---- graficar resultado iteracion de valores
#Encontrar la politica optima

U = iteracion_valores(S, T, U, A, gamma,10)

def optimizar(S, T, U, A, gamma):
    #pi = [0 for s in S]
    pi = {}
    for s in S:
       pi[s] = greedy(S, T, U, A, gamma, s)
    return pi

#print(optimizar(S, T, U, A, gamma)) # <----- ejecutar optimizar

graficar(optimizar(S, T, U, A, gamma)) # <----- graficar resultado de optimizar