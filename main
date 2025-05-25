# Extrusora 3D com Splines Suavizadas (2D)
# Projeto de Matemática Computacional
# Objetivo: Suavizar o movimento da extrusora em 2D usando splines cúbicas e analisar jerk e forças envolvidas

import numpy as np  # Biblioteca para operações matemáticas e vetoriais
import matplotlib.pyplot as plt  # Biblioteca para gerar gráficos
from scipy.interpolate import CubicSpline  # Para gerar splines cúbicas

# -------------------------------
# 1. CONFIGURAÇÕES INICIAIS
# -------------------------------
massa = 0.5  # massa da extrusora (kg)
tempo_total = 5.0  # tempo total da simulação (s)
num_pontos = 6  # número de pontos de controle no caminho
jerk_limite = 10  # limite de jerk em mm/s³ (modelo inspirado no Marlin)
forca_jerk_limite = 5  # limite de força associada ao jerk (Newtons)

# Define os pontos de controle (tempo e posições X e Y)
t = np.linspace(0, tempo_total, num_pontos)  # tempo dos pontos de controle
x = np.array([0, 10, 20, 25, 30, 35])  # coordenadas X dos pontos de controle
y = np.array([0, 5, 0, -5, 0, 5])  # coordenadas Y dos pontos de controle

# -------------------------------
# 2. SPLINES CÚBICAS PARA X(t) E Y(t)
# -------------------------------
spline_x = CubicSpline(t, x)  # spline cúbica que modela X em função do tempo
spline_y = CubicSpline(t, y)  # spline cúbica que modela Y em função do tempo
t_fino = np.linspace(0, tempo_total, 1000)  # vetor de tempo com mais pontos para suavidade

# Avalia as posições ao longo do tempo
x_fino = spline_x(t_fino)  # posição X suavizada
y_fino = spline_y(t_fino)  # posição Y suavizada

# Calcula derivadas para obter velocidade, aceleração e jerk
vx = spline_x.derivative(1)(t_fino)  # velocidade em X
vy = spline_y.derivative(1)(t_fino)  # velocidade em Y
vel = np.sqrt(vx**2 + vy**2)  # módulo da velocidade

ax = spline_x.derivative(2)(t_fino)  # aceleração em X
ay = spline_y.derivative(2)(t_fino)  # aceleração em Y
acel = np.sqrt(ax**2 + ay**2)  # módulo da aceleração

jx = spline_x.derivative(3)(t_fino)  # jerk em X
jy = spline_y.derivative(3)(t_fino)  # jerk em Y
jerk = np.sqrt(jx**2 + jy**2)  # módulo do jerk

# -------------------------------
# 3. GHOST SCORE BASEADO NO JERK LIMITE
# -------------------------------
delta_v = np.abs(np.diff(vel))  # variação da velocidade entre dois pontos
jerk_efetivo = delta_v / np.diff(t_fino)  # jerk efetivo (mudança de vel. / tempo)
jerk_efetivo = np.concatenate([[0], jerk_efetivo])  # adiciona zero no início para manter tamanho

# Verifica onde o jerk efetivo excede o limite configurado
excede_limite = jerk_efetivo > jerk_limite

# Força associada ao jerk (massa * jerk)
forca_jerk = massa * jerk  # newtons
excede_forca = forca_jerk > forca_jerk_limite

# Scores de risco
ghost_score = np.sum(excede_limite) / len(jerk_efetivo) * 100  # % com jerk acima do limite
forca_ghost_score = np.sum(excede_forca) / len(forca_jerk) * 100  # % com força jerk acima do limite

# -------------------------------
# 4. PLOTAGEM DOS RESULTADOS
# -------------------------------
fig, axs = plt.subplots(5, 1, figsize=(10, 17), sharex=True)  # cria 5 gráficos empilhados

# Gráfico da trajetória XY
axs[0].plot(x_fino, y_fino, label="Trajetória 2D", color="blue")
axs[0].set_ylabel("Y (mm)")
axs[0].set_title("Movimento da Extrusora (XY)")
axs[0].legend()
axs[0].axis("equal")  # mantém proporção entre eixos

# Gráfico da velocidade
axs[1].plot(t_fino, vel, label="Velocidade", color="green")
axs[1].set_ylabel("Velocidade (mm/s)")
axs[1].legend()

# Gráfico da aceleração
axs[2].plot(t_fino, acel, label="Aceleração", color="orange")
axs[2].set_ylabel("Aceleração (mm/s²)")
axs[2].legend()

# Gráfico do jerk efetivo e limite
axs[3].plot(t_fino, jerk_efetivo, label="Jerk Efetivo", color="red")
axs[3].axhline(jerk_limite, color="black", linestyle="--", label="Limite de Jerk")
axs[3].set_ylabel("Jerk (mm/s³)")
axs[3].legend()

# Gráfico da força associada ao jerk
axs[4].plot(t_fino, forca_jerk, label="Força do Jerk (N)", color="purple")
axs[4].axhline(forca_jerk_limite, color="black", linestyle="--", label="Limite de Força")
axs[4].set_ylabel("Força (N)")
axs[4].set_xlabel("Tempo (s)")
axs[4].legend()

# Título geral e layout ajustado
plt.suptitle(f"Análise do Movimento da Extrusora com Splines\nGhost Score (Jerk): {ghost_score:.2f}% | Ghost Score (Força): {forca_ghost_score:.2f}%")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

# -------------------------------
# 5. CONCLUSÃO
# -------------------------------
print(f"Ghost Score baseado no jerk limite: {ghost_score:.2f}%")
print(f"Ghost Score baseado na força de jerk (massa * jerk): {forca_ghost_score:.2f}%")
print("Esses valores representam o percentual de movimento com risco de vibração/ghosting.")
