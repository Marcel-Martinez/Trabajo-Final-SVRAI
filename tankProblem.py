import numpy as np

#Definición del MDP

S = np.array([0,1,2])
A = np.array([0,1])
U = np.array([0 for i in S]) #inicialización de la utilidad de los estados
gamma = 0.8
# R(s,a)
R = {
    (0,0): 0,
    (0,1): 2,
    (1,1): 2,
    (2,1): 2, 
    (2,0): 3
}

#Matriz de Transicion T(s, a, s')
T = {
    (0, 0, 0): 1,
    (0, 1, 1): 1, 
    (1, 1, 2): 1,
    (2, 0, 1): 1,
    (1, 0, 0): 1,
    (2, 1, 2): 1
}


#Algoritmos 
#Lookahead

def lookahead(U, s, a, T, R, S,gamma):
    return R[s,a] + gamma*sum(T[s,a,s1]*U[s1] for s1 in S if (s,a,s1) in T)
    
# Iteracion de valores

def backup(S,T,R,A, gamma,U, s):
    return max(lookahead(U, s, a, T, R, S, gamma) for a in A if (s,a) in R)

def greedy(S, T, R, U, A, gamma, s):
    u_ = 0
    a_ = 0
    for a in A:
        if (s,a) in R:
            u = lookahead(U, s, a, T, R, S, gamma)
            if (u >= u_):
                u_ = u
                a_ = a
    return a_, u_




def iteracion_valores(S, T, R, U, A, gamma, k_max):
    U = [0 for s in S]
    for k in range(0, k_max):
        U = [backup(S,T,R,A, gamma, U, s) for s in S]
    return U

print(iteracion_valores(S, T, R, U, A, gamma, 20)) # <--- ejecutar iteracion de valores

#Encontrar la politica optima

U = iteracion_valores(S, T, R, U, A, gamma, 20) #con una funcion de valor optima U (sabemos que es la optima porque se obtuvo de iteracion de val)
#se procede a aplicar este proceso de optimizacion para obtener el pi optimo mediante un algoritmo voraz y U

def optimizar(S, T, R, U, A, gamma):
    pi = [0 for s in S]
    for s in S:
       pi[s] = greedy(S, T, R, U, A, gamma, s)
    return pi

print(optimizar(S, T, R, U, A, gamma)) # <--- ejecutar optimizar
    