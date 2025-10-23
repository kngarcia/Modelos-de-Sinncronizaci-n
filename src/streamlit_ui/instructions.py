import streamlit as st

def display_instructions():
    """Muestra instrucciones y configuración rápida cuando no hay simulación"""
    
    st.header("🎯 Instrucciones Rápidas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Para ver sincronización rápida:
        - **K = 2.0+** (acoplamiento fuerte)
        - **σ_ω = 0.1** (poca diversidad)
        - **Pasos = 500** (suficiente tiempo)
        - **N = 50** (suficientes osciladores)
        """)
        
        st.info("""
        **Comportamiento esperado:**
        - Kuramoto → R ≈ 0.9-1.0
        - Winfree → R ≈ 0.1-0.3
        """)
    
    with col2:
        st.markdown("""
        ### 🔬 Para ver dinámica interesante:
        - **K = 1.0-1.5** (acoplamiento medio)
        - **σ_ω = 0.2-0.3** (diversidad media)
        - **Pasos = 200-300** (transición gradual)
        - **N = 30** (menos osciladores)
        """)