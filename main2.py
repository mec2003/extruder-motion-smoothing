# Extrusora 3D com Splines Suavizadas (2D)
# Projeto de Matemática Computacional
# Objetivo: Suavizar o movimento da extrusora em 2D usando splines cúbicas e analisar jerk e forças envolvidas

import numpy as np
import matplotlib.pyplot as plt
from spline import spline  # importa sua função de spline personalizada

# Estilo bonito para os gráficos
plt.style.use('seaborn-v0_8-darkgrid')

# -------------------------------
# 1. CONFIGURAÇÕES INICIAIS
# -------------------------------
massa = 0.5  # massa da extrusora (kg)
tempo_total = 5.0  # tempo total da simulação (s)
num_pontos = 6  # número de pontos de controle no caminho
jerk_limite = 10  # limite de jerk em mm/s³
forca_jerk_limite = 5  # limite de força associada ao jerk (Newtons)

# Pontos de controle
t = np.linspace(0, tempo_total, num_pontos)
x = [0, 10, 20, 25, 30, 35]
y = [0,  5,  0, -5,  0,  5]

# -------------------------------
# 2. GERAÇÃO DAS SPLINES
# -------------------------------
splines_x = spline(t, x)
splines_y = spline(t, y)
t_fino = np.linspace(0, tempo_total, 1000)

# Avaliação da spline
X, Y, V, A, J = [], [], [], [], []
for t_val in t_fino:
    for k in splines_x:
        t0, t1 = splines_x[k]['domain']
        if t0 <= t_val <= t1:
            x_t = splines_x[k]['s'](t_val)
            y_t = splines_y[k]['s'](t_val)
            dx = splines_x[k]['ds'](t_val)
            dy = splines_y[k]['ds'](t_val)
            ddx = splines_x[k]['d2s'](t_val)
            ddy = splines_y[k]['d2s'](t_val)
            dddx = splines_x[k]['d3s'](t_val)
            dddy = splines_y[k]['d3s'](t_val)

            X.append(x_t)
            Y.append(y_t)
            V.append(np.hypot(dx, dy))
            A.append(np.hypot(ddx, ddy))
            J.append(np.hypot(dddx, dddy))
            break

# -------------------------------
# 3. GHOST SCORE
# -------------------------------
delta_v = np.abs(np.diff(V))
jerk_efetivo = delta_v / np.diff(t_fino)
jerk_efetivo = np.concatenate([[0], jerk_efetivo])

excede_jerk = jerk_efetivo > jerk_limite
forca_jerk = massa * np.array(J)
excede_forca = forca_jerk > forca_jerk_limite

ghost_score = np.mean(excede_jerk) * 100
ghost_score_forca = np.mean(excede_forca) * 100

# -------------------------------
# 4. PLOTAGEM APRIMORADA
# -------------------------------
fig, axs = plt.subplots(5, 1, figsize=(12, 18), sharex=True)
fig.suptitle(
    f"Análise do Movimento da Extrusora com Splines\n"
    f"Ghost Score (Jerk): {ghost_score:.2f}% | Ghost Score (Força): {ghost_score_forca:.2f}%",
    fontsize=16, weight='bold'
)

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

# 4. Jerk Efetivo
axs[3].plot(t_fino, jerk_efetivo, color='crimson', linewidth=2, label="Jerk Efetivo")
axs[3].axhline(jerk_limite, color='black', linestyle='--', label="Limite de Jerk")
axs[3].set_ylabel("Jerk (mm/s³)")
axs[3].set_title("Jerk Efetivo", fontsize=14)
axs[3].legend()

# 5. Força do Jerk
axs[4].plot(t_fino, forca_jerk, color='purple', linewidth=2, label="Força do Jerk (N)")
axs[4].axhline(forca_jerk_limite, color='black', linestyle='--', label="Limite de Força")
axs[4].set_ylabel("Força (N)")
axs[4].set_xlabel("Tempo (s)")
axs[4].set_title("Força de Jerk", fontsize=14)
axs[4].legend()

# Layout final
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# -------------------------------
# 5. CONCLUSÃO
# -------------------------------
print(f"Ghost Score baseado no jerk limite: {ghost_score:.2f}%")
print(f"Ghost Score baseado na força de jerk: {ghost_score_forca:.2f}%")
