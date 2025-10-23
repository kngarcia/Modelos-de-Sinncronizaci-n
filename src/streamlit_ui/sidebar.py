import streamlit as st

def create_sidebar():
    """Crea y gestiona la barra lateral con todos los controles"""
    
    st.sidebar.header("⚙️ Parámetros de Simulación")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        N = st.slider("Número de osciladores", 10, 200, 50)
        K = st.slider("Fuerza acoplamiento (K)", 0.1, 5.0, 2.0, 0.1)
        dt = st.slider("Paso temporal (dt)", 0.01, 0.1, 0.05, 0.01)
    with col2:
        steps = st.slider("Pasos simulación", 50, 1000, 500)
        omega_mean = st.slider("Frecuencia media (ω)", 0.5, 2.0, 1.0, 0.1)
        omega_std = st.slider("Diversidad (σ_ω)", 0.05, 0.5, 0.1, 0.05)
    
    # Selección de modelos
    st.sidebar.header("📊 Modelos a Comparar")
    use_kuramoto = st.sidebar.checkbox("Modelo Kuramoto", value=True)
    use_winfree = st.sidebar.checkbox("Modelo Winfree", value=True)
    
    models_to_compare = {}
    if use_kuramoto:
        models_to_compare["Kuramoto"] = "kuramoto"
    if use_winfree:
        models_to_compare["Winfree"] = "winfree"
    
    # Información sobre parámetros
    with st.sidebar.expander("💡 Guía de parámetros"):
        st.markdown("""
        - **K alto (2.0+)**: Sincronización más rápida
        - **σ_ω bajo (0.1)**: Menos diversidad, más fácil sincronizar
        - **Pasos (500+)**: Mejor para ver evolución completa
        """)
    
    run_simulation = st.sidebar.button("🚀 Ejecutar Simulación", type="primary")
    
    return {
        'N': N,
        'K': K,
        'dt': dt,
        'steps': steps,
        'omega_mean': omega_mean,
        'omega_std': omega_std,
        'models_to_compare': models_to_compare,
        'run_simulation': run_simulation
    }