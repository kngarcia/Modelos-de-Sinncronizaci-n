import numpy as np

def kuramoto_model_vectorized(phases, omega, K, dt):
    """Modelo de Kuramoto CORREGIDO"""
    N = len(phases)
    # Calcular diferencias de fase correctamente
    phase_diff = phases - phases[:, np.newaxis]  # θ_j - θ_i
    coupling = np.sum(np.sin(phase_diff), axis=1)
    phases += (omega + (K / N) * coupling) * dt
    return phases % (2 * np.pi)

def winfree_model_vectorized(phases, omega, K, dt):
    """Modelo de Winfree CORREGIDO"""
    N = len(phases)
    phase_diff = phases - phases[:, np.newaxis]  # θ_j - θ_i
    coupling = np.sum((1 + np.cos(phase_diff)), axis=1)
    phases += (omega + (K / N) * coupling) * dt
    return phases % (2 * np.pi)

def order_parameter(phases):
    """Parámetro de orden - ya estaba correcto"""
    return np.abs(np.sum(np.exp(1j * phases)) / len(phases))

def mean_phase(phases):
    """Fase media del sistema"""
    return np.angle(np.sum(np.exp(1j * phases)))