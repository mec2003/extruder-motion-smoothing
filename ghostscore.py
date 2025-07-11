# ghostscore.py
from numpy.polynomial.legendre import leggauss
from spline import gerar_splines
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, lsim

# Parâmetros físicos
mt = 0.7     # massa da extrusora [kg]
mp = 0.01   # massa do filamento [kg]
l = 0.02    # comprimento do filamento [m]
g = 9.81

# Pontos de trajetória
x_pontos = np.array([0, 2, 3, 5, 6, 9, 10, 16]) 
y_pontos = np.array([0, 2, 1, 3, 10, 3, 4, 4])

# Obtemos os splines
polys_x, polys_y, t_pontos = gerar_splines(x_pontos, y_pontos)

# Criamos vetor de tempo UNIFORME
t_total = np.linspace(t_pontos[0], t_pontos[-1], 1000)

# Inicializamos vetores
a_x = np.zeros_like(t_total)
a_y = np.zeros_like(t_total)
v_x = np.zeros_like(t_total)
v_y = np.zeros_like(t_total)

# Avaliamos aceleração nos trechos corretos
for i in range(len(t_pontos) - 1):
    mask = (t_total >= t_pontos[i]) & (t_total <= t_pontos[i+1])
    a_x[mask] = polys_x[i](t_total[mask], 2)
    a_y[mask] = polys_y[i](t_total[mask], 2)
    v_x[mask] = polys_x[i](t_total[mask], 1)
    v_y[mask] = polys_y[i](t_total[mask], 1)


# Aceleração resultante
a_mod = np.sqrt(a_x**2 + a_y**2)
v_mod = np.sqrt(v_x**2 + v_y**2)


# Simulação
def simulate_theta(t, acc_list, mt, mp, l, g=9.81):
    I = (1/3) * mp * l**2
    M = mt + mp
    a_din = I + mp * l**2

    num = [-mp * l]
    den = [a_din * M, 0, mp * g * l * M - mp**2 * l**2]

    system = TransferFunction(num, den)
    U_t = M * acc_list

    resultado = lsim(system, U=U_t, T=t)
    t_out = resultado[0]
    theta = resultado[1]

    dt = t_out[1] - t_out[0]
    
    dtheta_dt = np.gradient(theta,dt)

    from numpy.polynomial.legendre import leggauss

# Módulo da velocidade angular
    mod_dtheta_dt = np.abs(dtheta_dt)

    # Função de quadratura de Gauss-Legendre composta
    def gauss_legendre_integrate(f_vals, t_vals, n=5):
            
        if len(t_vals) < 2:
            raise ValueError("Intervalo de tempo muito curto.")

        integral = 0.0
        nodes, weights = leggauss(n)  # Pontos e pesos da Gauss-Legendre em [-1, 1]

        for i in range(len(t_vals) - 1):
            a = t_vals[i]
            b = t_vals[i + 1]
            mid = (a + b) / 2
            half_length = (b - a) / 2

            # Interpolação linear dos valores de f para o intervalo [a, b]
            fa = f_vals[i]
            fb = f_vals[i + 1]

            def f_interp(xi):
                t_mapped = mid + half_length * xi
                return fa + (fb - fa) * (t_mapped - a) / (b - a)

            integral += half_length * sum(w * f_interp(x) for x, w in zip(nodes, weights))

        return integral

    # Integral de |dθ/dt| com quadratura de Gauss
    int_gauss_mod = gauss_legendre_integrate(mod_dtheta_dt, t_out, n=5)
    print(f"Integral de |dθ/dt| por quadratura de Gauss (n=5): {int_gauss_mod:.4f} rad")
    
    # Gráfico da trajetória original sem interpolação
    plt.figure(figsize=(6, 6))
    plt.plot(x_pontos, y_pontos, 'o-', color='purple', label='Trajetória original')
    for i, (x, y) in enumerate(zip(x_pontos, y_pontos)):
        plt.text(x, y, f'{i}', fontsize=8, verticalalignment='bottom', horizontalalignment='right')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.title('Trajetória da extrusora')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    # Plot da velocidade linear
    plt.figure(figsize=(10, 4))
    plt.plot(t_total, v_mod, label='Velocidade linear |v|', color='blue')
    for t_n in t_pontos:
        plt.axvline(t_n, color='gray', linestyle='--', alpha=0.5)
        plt.text(t_n, np.interp(t_n, t_total, v_mod), f'{t_n:.1f}', fontsize=8, rotation=90,
                verticalalignment='bottom', horizontalalignment='right')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Velocidade linear [mm/s]')
    plt.title('Módulo da velocidade linear da extrusora')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Plot da aceleração linear
    plt.figure(figsize=(10, 4))
    plt.plot(t_total, a_mod, label='Aceleração linear |a|', color='red')
    for t_n in t_pontos:
        plt.axvline(t_n, color='gray', linestyle='--', alpha=0.5)
        plt.text(t_n, np.interp(t_n, t_total, a_mod), f'{t_n:.1f}', fontsize=8, rotation=90,
                verticalalignment='bottom', horizontalalignment='right')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Aceleração linear [mm/s²]')
    plt.title('Módulo da aceleração linear da extrusora')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(10, 5))
    plt.plot(t_out, theta, label='θ(t)')
    for t_n in t_pontos:
        plt.axvline(t_n, color='gray', linestyle='--', alpha=0.5)
        plt.text(t_n, np.interp(t_n, t_out, theta), f'{t_n:.1f}', fontsize=8, rotation=90,
            verticalalignment='bottom', horizontalalignment='right')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Ângulo do filamento θ(t) [rad]')
    plt.title('Resposta do filamento à aceleração da extrusora')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


    plt.figure(figsize=(10, 4))
    plt.plot(t_out, dtheta_dt, label='dθ/dt', color='orange')
    for t_n in t_pontos:
        plt.axvline(t_n, color='gray', linestyle='--', alpha=0.5)
        plt.text(t_n, np.interp(t_n, t_out, dtheta_dt), f'{t_n:.1f}', fontsize=8, rotation=90,
             verticalalignment='bottom', horizontalalignment='right')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Velocidade angular dθ/dt [rad/s]')
    plt.title('Velocidade angular do filamento')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


    # Gráfico do módulo da velocidade angular
    plt.figure(figsize=(10, 4))
    plt.plot(t_out, mod_dtheta_dt, label='|dθ/dt|', color='green')
    for t_n in t_pontos:
        plt.axvline(t_n, color='gray', linestyle='--', alpha=0.5)
        plt.text(t_n, np.interp(t_n, t_out, mod_dtheta_dt), f'{t_n:.1f}', fontsize=8, rotation=90,
                 verticalalignment='bottom', horizontalalignment='right')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Velocidade angular |dθ/dt| [rad/s]')
    plt.title('Módulo da velocidade angular do filamento')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

    return theta, dtheta_dt

# Rodar simulação
theta, dtheta_dt = simulate_theta(t_total, a_mod, mt, mp, l)
