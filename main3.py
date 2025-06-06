from spline import spline
from ghostscore import simulate_theta
import numpy as np

# ====== Entradas ======
tempo_total = 5.0
num_pontos = 6
t_ctrl = np.linspace(0, tempo_total, num_pontos)

x_vals = [0, 10, 20, 25, 30, 35]
y_vals = [0,  5,  0, -5,  0,  5]

# Parâmetros físicos
mt = 1000
mp = 100
l = 2

# ====== Gera splines ======
x_splines = spline(t_ctrl, x_vals)
y_splines = spline(t_ctrl, y_vals)

# Vetor de tempo para amostragem
T = np.linspace(0, tempo_total, 1000)
acc_cart = []

# Extrai o módulo da aceleração ao longo do tempo
for t_val in T:
    for k in x_splines:
        t0, t1 = x_splines[k]['domain']
        if t0 <= t_val <= t1:
            ddx = x_splines[k]['d2s'](t_val)
            ddy = y_splines[k]['d2s'](t_val)
            acc = np.sqrt(ddx**2 + ddy**2)  # módulo da aceleração
            acc_cart.append(acc)
            break

# Chama a simulação com a aceleração calculada
theta = simulate_theta(T, acc_cart, mt, mp, l)

# Trajetória
X = []
Y = []
for t_val in T:
    for k in x_splines:
        t0, t1 = x_splines[k]['domain']
        if t0 <= t_val <= t1:
            X.append(x_splines[k]['s'](t_val))
            Y.append(y_splines[k]['s'](t_val))
            break

x = x_vals
y = y_vals

fig, axs = plt.subplots(2, 1, figsize=(10, 8))


# 1. Trajetória
axs[0].plot(X, Y, color='royalblue', label="Trajetória 2D", linewidth=2)
axs[0].scatter(x, y, color='black', label="Pontos de Controle", zorder=5)
axs[0].axis("equal")
axs[0].set_ylabel("Y (mm)")
axs[0].set_title("Trajetória da Extrusora (XY)", fontsize=14)
axs[0].legend()

# 2. Velocidade
axs[1].plot(t_fino, V, color='seagreen', linewidth=2, label="Velocidade")
axs[1].set_ylabel("Velocidade (mm/s)")
axs[1].set_title("Velocidade", fontsize=14)
axs[1].legend()

# 3. Aceleração
axs[2].plot(t_fino, A, color='darkorange', linewidth=2, label="Aceleração")
axs[2].set_ylabel("Aceleração (mm/s²)")
axs[2].set_title("Aceleração", fontsize=14)
axs[2].legend()