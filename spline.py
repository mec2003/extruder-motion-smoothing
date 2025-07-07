# spline.py
import numpy as np
from scipy.interpolate import BPoly
import matplotlib.pyplot as plt

def gerar_splines(x_pontos, y_pontos):
    t_pontos = np.linspace(0, 21, len(x_pontos))
    polinomios_x = []
    polinomios_y = []

    for i in range(len(t_pontos) - 1):
        t_intervalo = [t_pontos[i], t_pontos[i+1]]
        cond_x = [[x_pontos[i], 0, 0], [x_pontos[i+1], 0, 0]]
        cond_y = [[y_pontos[i], 0, 0], [y_pontos[i+1], 0, 0]]
        poly_x = BPoly.from_derivatives(t_intervalo, cond_x)
        poly_y = BPoly.from_derivatives(t_intervalo, cond_y)
        polinomios_x.append(poly_x)
        polinomios_y.append(poly_y)

    return polinomios_x, polinomios_y, t_pontos


    # Gráfico 2: Velocidade
    ax2.plot(t_final, v_final, '-', label='Magnitude da Velocidade')
    ax2.plot(t_pontos, np.zeros_like(t_pontos), 'ro', markersize=9, label='Velocidade Nula nos Nós')
    ax2.set_title('Velocidade x Tempo ')
    ax2.set_xlabel('Tempo (s)')
    ax2.set_ylabel('Velocidade (mm/s)')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

x_pontos = np.array([0, 0, 2, 2, 4, 4, 6, 6])
y_pontos = np.array([0, 2, 2, 3, 3, 2, 2, 0])
