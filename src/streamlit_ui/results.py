import streamlit as st
from src.utils import calculate_metrics

def display_main_metrics(results):
    """Muestra las métricas principales en columnas"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🎯 Sincronización Final")
        for name, result in results.items():
            final_R = result['final_R']
            color = "🟢" if final_R > 0.8 else "🟡" if final_R > 0.5 else "🔴"
            st.metric(
                f"{color} {name}", 
                f"{final_R:.3f}",
                help="R = 1: sincronización perfecta, R = 0: desorden completo"
            )
    
    with col2:
        st.subheader("⏱️ Velocidad")
        for name, result in results.items():
            metrics = calculate_metrics(result)
            sync_time = metrics.get('time_to_90', result['history_time'][-1])
            st.metric(
                f"⏰ {name}", 
                f"{sync_time:.2f}s",
                help="Tiempo para alcanzar R ≥ 0.9"
            )
    
    with col3:
        st.subheader("🏆 Comparación")
        best_model = max(results.items(), key=lambda x: x[1]['final_R'])
        worst_model = min(results.items(), key=lambda x: x[1]['final_R'])
        
        st.success(f"**Mejor:** {best_model[0]} (R={best_model[1]['final_R']:.3f})")
        st.warning(f"**Peor:** {worst_model[0]} (R={worst_model[1]['final_R']:.3f})")
        
        if best_model[0] == "Kuramoto":
            st.info("✅ Comportamiento esperado: Kuramoto sincroniza mejor")
        else:
            st.warning("⚠️ Comportamiento inesperado: Revisar parámetros")

def display_detailed_metrics(results, steps):
    """Muestra métricas detalladas en pestañas"""
    
    for name, result in results.items():
        with st.expander(f"📊 {name} - Métricas Detalladas", expanded=False):
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
                st.metric("Pasos totales", steps)
                st.metric("Tiempo simulado", f"{result['history_time'][-1]:.2f}s")

def display_diagnostic_info(results):
    """Muestra información de diagnóstico"""
    
    with st.expander("🔍 Información de Diagnóstico", expanded=False):
        st.write("**Parámetros usados en la simulación:**")
        st.json(results[list(results.keys())[0]]['parameters'])
        
        st.write("**Resumen de ejecución:**")
        for name, result in results.items():
            st.write(f"- **{name}**: {len(result['history_phases'])} estados, R final = {result['final_R']:.4f}")