import streamlit as st
import plotly.graph_objects as go
import numpy as np
from src.models import order_parameter
from src.visualization import plot_sync_comparison

def create_circle_figure(phases, model_name):
    """Crea una figura circular para visualizar las fases"""
    R = order_parameter(phases)
    
    # Convertir a coordenadas cartesianas
    x = np.cos(phases)
    y = np.sin(phases)
    
    # Crear figura
    fig = go.Figure()
    
    # Añadir círculo unitario
    theta = np.linspace(0, 2*np.pi, 100)
    fig.add_trace(go.Scatter(
        x=np.cos(theta), y=np.sin(theta),
        mode='lines', line=dict(color='gray', dash='dash'),
        name='Círculo unitario'
    ))
    
    # Añadir puntos de fase
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='markers',
        marker=dict(
            size=10, 
            color=phases, 
            colorscale='hsv',
            showscale=True,
            colorbar=dict(title="Fase")
        ),
        name=f'Osciladores (R={R:.3f})'
    ))
    
    # Añadir vector de orden
    mean_phase = np.angle(np.sum(np.exp(1j * phases)))
    fig.add_trace(go.Scatter(
        x=[0, R * np.cos(mean_phase)], 
        y=[0, R * np.sin(mean_phase)],
        mode='lines+markers',
        line=dict(color='red', width=4),
        marker=dict(size=8, color='red'),
        name='Vector de orden'
    ))
    
    fig.update_layout(
        title=f'{model_name} - Estado Final (R={R:.3f})',
        xaxis_title='X',
        yaxis_title='Y',
        showlegend=True,
        width=400,
        height=400,
        xaxis=dict(range=[-1.2, 1.2], scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-1.2, 1.2])
    )
    
    return fig

def create_individual_plot(result, model_name):
    """Crea gráfica individual de evolución"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=result['history_time'],
        y=result['history_R'],
        mode='lines',
        name=f'{model_name}',
        line=dict(width=3)
    ))
    fig.update_layout(
        title=f'Evolución de {model_name}',
        xaxis_title='Tiempo',
        yaxis_title='Parámetro de Orden R',
        height=300
    )
    return fig

def display_visualizations(results, dt):
    """Muestra todas las visualizaciones organizadas en pestañas"""
    
    tab1, tab2, tab3 = st.tabs(["📈 Evolución Temporal", "🎯 Estados Finales", "📋 Métricas Detalladas"])
    
    with tab1:
        st.subheader("Evolución del Parámetro de Orden R")
        fig_comparison = plot_sync_comparison(results, dt)
        st.plotly_chart(fig_comparison, use_container_width=True, key="evolution_chart")
    
    with tab2:
        st.subheader("Distribución de Fases Finales")
        
        # Crear columnas dinámicamente según número de modelos
        cols = st.columns(len(results))
        
        for idx, (name, result) in enumerate(results.items()):
            with cols[idx]:
                phases = result['final_phases']
                fig_circle = create_circle_figure(phases, name)
                st.plotly_chart(fig_circle, use_container_width=True, key=f"circle_{name}_{idx}")
    
    with tab3:
        st.subheader("Métricas Detalladas por Modelo")
        
        for name, result in results.items():
            with st.expander(f"📊 {name} - Métricas Detalladas", expanded=False):
                from src.utils import calculate_metrics
                metrics = calculate_metrics(result)
                
                col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
                
                with col_metrics1:
                    st.markdown("**📈 Sincronización**")
                    st.metric("Final", f"{metrics['final_sync']:.4f}")
                    st.metric("Máxima", f"{metrics['max_sync']:.4f}")
                    st.metric("Promedio", f"{metrics['avg_sync']:.4f}")
                
                with col_metrics2:
                    st.markdown("**⏱️ Tiempos de Sincronización**")
                    for threshold in [50, 80, 90]:
                        time_val = metrics.get(f'time_to_{threshold}', result['history_time'][-1])
                        st.metric(f"R ≥ {threshold}%", f"{time_val:.2f}s")
                
                with col_metrics3:
                    st.markdown("**📊 Estabilidad**")
                    st.metric("Estabilidad", f"{metrics['sync_stability']:.4f}")
                    st.metric("Pasos totales", len(result['history_R']))
                    st.metric("Tiempo simulado", f"{result['history_time'][-1]:.2f}s")
                
                # Gráfica de evolución individual
                st.markdown("**📈 Evolución Individual**")
                fig_individual = create_individual_plot(result, name)
                st.plotly_chart(fig_individual, use_container_width=True, key=f"individual_{name}")