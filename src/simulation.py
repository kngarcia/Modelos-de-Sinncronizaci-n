import time
import numpy as np
from .models import order_parameter

def simulate_model(model, N=50, K=1.5, dt=0.05, steps=200, omega_mean=1.0, omega_std=0.2):
    """Ejecuta una simulación completa de un modelo"""
    # Inicialización
    phases = np.random.uniform(0, 2 * np.pi, N)
    omega = np.random.normal(omega_mean, omega_std, N)
    
    history_R = []
    history_phases = []
    history_time = []
    
    start_time = time.time()
    
    # Simulación
    for t in range(steps):
        phases = model(phases, omega, K, dt)
        R = order_parameter(phases)
        
        history_R.append(R)
        history_phases.append(phases.copy())
        history_time.append(t * dt)
    
    total_time = time.time() - start_time
    
    results = {
        'final_R': history_R[-1],
        'total_time': total_time,
        'history_R': np.array(history_R),
        'history_phases': np.array(history_phases),
        'history_time': np.array(history_time),
        'final_phases': phases,
        'parameters': {
            'N': N, 'K': K, 'dt': dt, 'steps': steps,
            'omega_mean': omega_mean, 'omega_std': omega_std
        }
    }
    
    return results

def compare_models(models_dict, **kwargs):
    """Compara múltiples modelos"""
    results = {}
    for name, model in models_dict.items():
        print(f"Simulando {name}...")
        results[name] = simulate_model(model, **kwargs)
    return results

def synchronization_time(history_R, threshold=0.9, window=5):
    """Calcula el tiempo de sincronización"""
    for i in range(len(history_R) - window):
        if np.all(history_R[i:i+window] >= threshold):
            return i
    return len(history_R) - 1