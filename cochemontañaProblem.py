import numpy as np
import math

x = [-1.2, 0.6]
v = [-0.07, 0.07]
A = [-1, 0, 1]
goal = [0.6, 0]
gamma = 1
U = {}
d = 30


def inicializar_estado():
    state = tuple((np.random.uniform(-0.6, 0.2), 0))
    return state #los estados estan compuestos por pos (horizontal) y velocidad

def step(state, action):
    pos, v = state

    v = v + 0.001*action + 0.0025*math.cos(3*pos)

    #para evitar que el carro se salga de los limites del entorno:
    if((pos+v) < -1.2):
        action = 0
        v = v + 0.001*action + 0.0025*math.cos(3*pos)

    pos = (pos + v)

    state = (round(pos,4), round(v,4))
    return state

def R(s,a):
    #siempre vamos a recibir una recompenza de -1 en cada cambio de sentido
    recompensa = 0
    state = step(s,a)

    if((s[1]<0 and state[1]>0) or (s[1]>0 and state[1]<0)):
        recompensa = -1 

    
    if(state[0]>=goal[0] and state[1]>=goal[1]):
        recompensa = 100

    return recompensa

s = inicializar_estado() # pos, v

# T va a valer 1 siempre, no hay incertidumbre y las transiciónes ya las tenemos definidas en la función step

#Resolucion del juego

#Algoritmos

print("*************Forward Search****************")

def lookahead(U, s, a, A):
    return R(s, a) + U

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

print(forward_search(U, s, d, A)) # <---- ejecutar forward search

print("\n")
print("\n")
print("****************Simulacion Montecarlo*************")
# Simulacion Monte Carlo

# A partir de aqui se monta el entorno para la simulacion

s = inicializar_estado() #iniciamos el estado desde el que suponemos que empezamos la planificación online
U = {
    s: 0
}
N = {}
d = 150
m = 25
c = 100
Q = {}
#TR sería nuestra funcion step 

def MCTS(m, s, N, Q, c, A, gamma, d):
    for i in range(0, m):
        simulate(s, N, Q, c, U,A, gamma, d)
    print(Q)
    val_ = 0
    for a in A:
        val = Q[(s, a)]
        if(val>=val_):
            a_ = a
    return a_
    

def simulate(s, N, Q, c, U, A, gamma, d):
    if(d <=0):
        return U[s] 
    print(U)
    if((s, A[0]) not in N):
        for a in A:
            N[(s,a)] = 0
            Q[(s,a)] = 0
        return R(s,a) 

    a = explore(A, N, Q, c, s)
    s1 = step(s, a)
    r = R(s,a)
    q = r + gamma*simulate(s1, N, Q, c, U,A, gamma, d-1)
    U[s1] = q
    N[(s,a)] +=1
    Q[(s,a)] += (q-Q[(s,a)])/N[(s,a)]

    return q

def explore(A, N, Q, c, s):
    Ns = sum(N[(s, a)] for a in A)
    a_ = 0
    val_ = 0
    for a in A:
        val = Q[(s, a)] + c*bonus(N[(s,a)], Ns)
        if(val>=val_):
            a_ = a
    return a_


def bonus(Nsa, Ns):
    if(Nsa == 0):
        return float('inf')
    else:
        return math.sqrt(math.log(Ns)/Nsa)

res = MCTS(m, s, N, Q, c, A, gamma, d) # <---- ejecutar MCTS
print(res)