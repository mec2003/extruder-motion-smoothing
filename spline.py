import numpy as np
import matplotlib.pyplot as plt

# Função que gera os polinômios de spline cúbica e suas derivadas
def spline(t, pos):
    n = len(t)  # número de pontos

    # 'a' é o valor da função em cada ponto (coeficiente inicial de cada polinômio)
    a = {k: v for k, v in enumerate(pos)}

    # 'h[k]' é o intervalo entre t[k] e t[k+1]
    h = {k: t[k+1] - t[k] for k in range(n - 1)}

    # Matrizes do sistema linear para calcular os coeficientes 'c'
    A = [[1] + [0] * (n - 1)]  # primeira linha para condição de contorno natural
    B = [0]  # vetor do lado direito

    # Construção do sistema linear para os coeficientes 'c'
    for i in range(1, n - 1):
        row = [0] * n
        row[i - 1] = h[i - 1]
        row[i] = 2 * (h[i - 1] + h[i])
        row[i + 1] = h[i]
        A.append(row)
        B.append(3 * (a[i+1] - a[i]) / h[i] - 3 * (a[i] - a[i-1]) / h[i-1])

    # Última equação: condição de contorno natural (segunda derivada zero no fim)
    A.append([0] * (n - 1) + [1])
    B.append(0)

    # Resolve o sistema para obter os coeficientes 'c'
    c = dict(zip(range(n), np.linalg.solve(A, B)))

    # Calcula os coeficientes 'b' e 'd' para cada polinômio da spline
    b, d = {}, {}
    for k in range(n - 1):
        b[k] = (a[k+1] - a[k]) / h[k] - (h[k] / 3) * (2 * c[k] + c[k+1])
        d[k] = (c[k+1] - c[k]) / (3 * h[k])

    # Criação dos polinômios spline e suas derivadas
    splines = {}
    for k in range(n - 1):
        ak, bk_, ck, dk = a[k], b[k], c[k], d[k]
        tk = t[k]

        # Polinômio da spline: S(t)
        s = lambda t, a=ak, b=bk_, c=ck, d=dk, tk=tk: a + b * (t - tk) + c * (t - tk)**2 + d * (t - tk)**3
        # Primeira derivada: velocidade
        ds = lambda t, b=bk_, c=ck, d=dk, tk=tk: b + 2 * c * (t - tk) + 3 * d * (t - tk)**2
        # Segunda derivada: aceleração
        d2s = lambda t, c=ck, d=dk, tk=tk: 2 * c + 6 * d * (t - tk)
        # Terceira derivada: jerk
        d3s = lambda t, d=dk: 6 * d

        # Armazena as funções e o domínio de validade de cada spline
        splines[k] = {
            's': s,
            'ds': ds,
            'd2s': d2s,
            'd3s': d3s,
            'domain': [t[k], t[k+1]]
        }

    return splines

# ====== Definição dos dados ======

# Tempo total e número de pontos
tempo_total = 5.0
num_pontos = 6
t = np.linspace(0, tempo_total, num_pontos)

# Coordenadas x e y ao longo do tempo (trajetória)
x_vals = [0, 10, 20, 25, 30, 35]
y_vals = [0,  5,  0, -5,  0,  5]

# Geração das splines para x(t) e y(t)
x_splines = spline(t, x_vals)
y_splines = spline(t, y_vals)

# ====== Avaliação das funções spline em muitos pontos ======
T = np.linspace(0, tempo_total, 1000)  # vetor de tempo mais denso para o gráfico

# Listas para armazenar os resultados
X, Y = [], []
V, A, J = [], [], []

# Para cada instante de tempo em T, encontra o intervalo correspondente e calcula:
# posição (x, y), velocidade, aceleração e jerk
for t_val in T:
    for k in x_splines:
        t0, t1 = x_splines[k]['domain']
        if t0 <= t_val <= t1:
            # Avalia posição
            x_t = x_splines[k]['s'](t_val)
            y_t = y_splines[k]['s'](t_val)

            # Avalia derivadas
            dx = x_splines[k]['ds'](t_val)
            dy = y_splines[k]['ds'](t_val)
            ddx = x_splines[k]['d2s'](t_val)
            ddy = y_splines[k]['d2s'](t_val)
            dddx = x_splines[k]['d3s'](t_val)
            dddy = y_splines[k]['d3s'](t_val)

            # Armazena resultados
            X.append(x_t)
            Y.append(y_t)
            V.append(np.sqrt(dx**2 + dy**2))         # Módulo da velocidade
            A.append(np.sqrt(ddx**2 + ddy**2))       # Módulo da aceleração
            J.append(np.sqrt(dddx**2 + dddy**2))     # Módulo do jerk
            break

# ====== Plotagem dos gráficos ======

fig, axs = plt.subplots(4, 1, figsize=(10, 14), sharex=False)

# 1. Trajetória XY
axs[0].plot(X, Y, label="Trajetória", color='blue')
axs[0].scatter(x_vals, y_vals, color='black')  # pontos de controle
axs[0].set_title("Trajetória 2D")
axs[0].set_xlabel("X (mm)")
axs[0].set_ylabel("Y (mm)")
axs[0].axis('equal')
axs[0].grid(True)
axs[0].legend()

# 2. Velocidade
axs[1].plot(T, V, label="Velocidade", color='green')
axs[1].set_title("Módulo da Velocidade")
axs[1].set_ylabel("Velocidade (mm/s)")
axs[1].grid(True)
axs[1].legend()

# 3. Aceleração
axs[2].plot(T, A, label="Aceleração", color='orange')
axs[2].set_title("Módulo da Aceleração")
axs[2].set_ylabel("Aceleração (mm/s²)")
axs[2].grid(True)
axs[2].legend()

# 4. Jerk
axs[3].plot(T, J, label="Jerk", color='red')
axs[3].set_title("Módulo do Jerk")
axs[3].set_ylabel("Jerk (mm/s³)")
axs[3].set_xlabel("Tempo (s)")
axs[3].grid(True)
axs[3].legend()
