import numpy as np
from .simulation import synchronization_time

def set_random_seed(seed=42):
    """Establece semilla para reproducibilidad"""
    np.random.seed(seed)

def calculate_metrics(results):
    """Calcula métricas adicionales de la simulación"""
    metrics = {}
    history_R = results['history_R']
    
    metrics['final_sync'] = history_R[-1]
    metrics['max_sync'] = np.max(history_R)
    metrics['avg_sync'] = np.mean(history_R)
    metrics['sync_stability'] = np.std(history_R[-50:])  # Últimos 50 pasos
    
    # Tiempo para alcanzar diferentes niveles de sincronización
    for threshold in [0.5, 0.8, 0.9]:
        metrics[f'time_to_{int(threshold*100)}'] = synchronization_time(
            history_R, threshold) * results['parameters']['dt']
    
    return metrics

def export_results(results, filename):
    """Exporta resultados a archivo"""
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(results, f)

def load_results(filename):
    """Carga resultados desde archivo"""
    import pickle
    with open(filename, 'rb') as f:
        return pickle.load(f)