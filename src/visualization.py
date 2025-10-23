import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from .models import order_parameter
from .simulation import synchronization_time

def plot_sync_comparison(results_dict, dt):
    """Crea gráficas comparativas de sincronización"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Evolución de Sincronización', 'Tiempo de Sincronización', 
                       'Distribución Final de Fases', 'Velocidad de Convergencia'],
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    colors = ['blue', 'red', 'green', 'orange']
    
    for i, (name, results) in enumerate(results_dict.items()):
        color = colors[i % len(colors)]
        time_array = results['history_time']
        R_array = results['history_R']
        
        # Evolución temporal
        fig.add_trace(
            go.Scatter(x=time_array, y=R_array, name=name, 
                      line=dict(color=color, width=2)),
            row=1, col=1
        )
        
        # Tiempo de sincronización
        sync_time = synchronization_time(R_array) * dt
        fig.add_trace(
            go.Bar(x=[name], y=[sync_time], name=name,
                  marker_color=color, showlegend=False),
            row=1, col=2
        )
        
        # Distribución de fases final
        phases = results['final_phases']
        fig.add_trace(
            go.Histogram(x=phases, name=name, nbinsx=20,
                        marker_color=color, opacity=0.7),
            row=2, col=1
        )
    
    fig.update_layout(height=800, title_text="Análisis Comparativo de Modelos")
    return fig

def create_circle_visualization(phases_history, model_names, dt):
    """Crea visualización circular animada"""
    fig = make_subplots(
        rows=1, cols=len(model_names),
        subplot_titles=model_names,
        specs=[[{"type": "scatter"} for _ in model_names]]
    )
    
    # Configurar ejes
    for i in range(len(model_names)):
        fig.update_xaxes(range=[-1.5, 1.5], row=1, col=i+1)
        fig.update_yaxes(range=[-1.5, 1.5], row=1, col=i+1)
    
    frames = []
    for frame_idx in range(len(phases_history[0])):
        frame_data = []
        for model_idx, phases_model in enumerate(phases_history):
            phases = phases_model[frame_idx]
            x = np.cos(phases)
            y = np.sin(phases)
            R = order_parameter(phases)
            
            # Puntos de fase
            scatter = go.Scatter(
                x=x, y=y, mode='markers',
                marker=dict(size=10, color=phases, colorscale='hsv',
                           line=dict(width=2, color='DarkSlateGrey')),
                name=model_names[model_idx]
            )
            frame_data.append(scatter)
            
            # Vector de orden
            mean_phase = np.angle(np.sum(np.exp(1j * phases)))
            arrow = go.Scatter(
                x=[0, R * np.cos(mean_phase)], 
                y=[0, R * np.sin(mean_phase)],
                mode='lines+markers',
                line=dict(color='red', width=4),
                marker=dict(size=8, color='red')
            )
            frame_data.append(arrow)
        
        frames.append(go.Frame(data=frame_data, name=str(frame_idx)))
    
    # Añadir círculo unitario
    for i in range(len(model_names)):
        theta = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(go.Scatter(
            x=np.cos(theta), y=np.sin(theta),
            mode='lines', line=dict(color='gray', dash='dash'),
            showlegend=False
        ), row=1, col=i+1)
    
    fig.frames = frames
    
    # Botones de animación
    fig.update_layout(
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {
                    "label": "Play",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 50, "redraw": True}}]
                }
            ]
        }]
    )
    
    return fig