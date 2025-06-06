from spline import spline
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, lsim

def simulate_theta(t, acc_list, mt, mp, l, g=9.81):
    I = (1/3) * mp * l**2
    M = mt + mp
    a = I + mp * l**2

    num = [-mp * l]
    den = [a * M, 0, mp * g * l * M - mp*2 * l*2]

    system = TransferFunction(num, den)

    # Converte aceleração para força
    U_t = M * np.array(acc_list)

    # Simula θ(t)
    _, theta, _ = lsim(system, U=U_t, T=t)

    # Plota o ângulo theta(t)
    plt.figure(figsize=(10, 5))
    plt.plot(t, theta)
    plt.xlabel('Tempo [s]')
    plt.ylabel('Ângulo do filamento θ(t) [rad]')
    plt.title('Resposta do filamento à aceleração variável da extrusora')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return theta