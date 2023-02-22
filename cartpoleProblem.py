import numpy as np
import math

gravedad = 9.8
m_cart = 1
m_pole = 0.1
total_m = m_cart + m_pole
l = 0.5
gamma = 1
t = 0.01

#definimos una politica pi de simulacion
def pi(state):
    x, v, theta, w = state
    if(theta>=0):
        a = 10
    else:
        a = -10
    return a

def inicializar_estado():
    #inicializar aleatoriamente (dentro de unos valores razonables) las variables de S
    state = tuple(np.random.uniform(-0.05, 0.05, size=(4,)))
    return state


def step(state,action):
    x, v, theta, w = state

    tau = (action + (w**2)*l*math.sin(theta/2))/total_m

    alpha = (gravedad*math.sin(theta)-tau*math.cos(theta))/(0.5*((4/3)-(m_pole/total_m)*(math.cos(theta)**2)))
    a = tau-((l/2)*alpha*math.cos(theta)*(m_pole/total_m))

    #integración de Euler
    x = round(x + t*v, 4)
    v = round(v + t*a, 4)
    theta = round(theta + t*w, 4)
    w = round(w + t*alpha, 4)

    state = tuple((x, v, theta, w))
    return state


def R(state):
    x, v, theta, w = state
    # se define las condiciones que determinan que el jugador ha perdido la ronda
    x_limite = 10

    theta_limite = (12*2*math.pi)/360

    if (x > x_limite or theta > theta_limite or x< -x_limite or theta< -theta_limite):
        recompensa = 0
    else:
        recompensa = 1
    
    return recompensa

A = [-10,10]

# T va a valer 1 siempre, no hay incertidumbre y las transiciónes ya las tenemos definidas en la función step

#Resolución del Juego

#Algortimos

print("*************Lookahead con Simulacion (ROLLOUT)*************")

# Lookahead con Simulacion (ROLLOUT)

def lookahead(U, s, a):
    return R(step(s, a)) # lookahead de un paso 


def greedy(U, A, s):
    u_ = 0
    a_ = 10
    for a in A:
        #if s in R:
        u = lookahead(U, s,a)
        if (u > u_):
            u_ = u
            a_ = a
    return a_, u_

def rollout(gamma, s, depth):
    ret = 0

    for tt in range(1, depth):
        a = pi(s)
        s= step(s, a)
        recompensa = R(s)
        ret += recompensa*gamma**(tt-1)
    print(ret)
    return ret

def simulacion(U, A, gamma, s, depth):
    
    U[s] = rollout(gamma, s, depth)
    #print(U)
    return greedy(U, A, s)[0]

#aplicamos el algoritmo online para el estado inicial
s = inicializar_estado() # x, v, theta, w
pasos = 30
politica = {}
U = {} # inicializamos la funcion U

for i in range(0, pasos):
    accion = simulacion(U, A, gamma, s, 20)
    politica[s] = accion

    #damos un paso
    s = step(s, accion)
    

print(politica) #se imprime la politica simulada

print("\n")
print("\n")
print("****************Simulacion Montecarlo*************")

# Simulación Monte Carlo
# A partir de aqui se monta el entorno para la simulacion

s = inicializar_estado() #iniciamos el estado desde el que suponemos que empezamos la planificación online
U = {
    s: 0
}
N = {}
d = 15
m = 5
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
    if((s, A[0]) not in N):
        for a in A:
            N[(s,a)] = 0
            Q[(s,a)] = 0
        return R(step(s,a)) 

    a = explore(A, N, Q, c, s)
    s1 = step(s, a)
    r = R(s1)
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