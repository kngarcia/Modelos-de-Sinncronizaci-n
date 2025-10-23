import streamlit as st
import sys
import os
import traceback

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.models import kuramoto_model_vectorized, winfree_model_vectorized
    from src.simulation import compare_models
    from src.streamlit_ui import (
        create_sidebar, 
        display_main_metrics, 
        display_visualizations,
        display_diagnostic_info,
        display_instructions
    )
except ImportError as e:
    st.error(f"Error importando módulos: {e}")

def main():
    st.set_page_config(
        page_title="Simulación Sincronización Luciérnagas - CORREGIDO",
        page_icon="🐝",
        layout="wide"
    )
    
    st.title("🐝 Simulación de Sincronización: Winfree vs Kuramoto")
        
    # Obtener controles de la barra lateral
    controls = create_sidebar()
    
    # Si se presiona el botón de simulación
    if controls['run_simulation']:
        models_to_compare = controls['models_to_compare']
        if not models_to_compare:
            st.error("Selecciona al menos un modelo para comparar")
            return
            
        with st.spinner("Simulando con implementación corregida..."):
            try:
                # Mapear nombres a funciones de modelo
                model_functions = {
                    "Kuramoto": kuramoto_model_vectorized,
                    "Winfree": winfree_model_vectorized
                }
                models_to_run = {name: model_functions[name] for name in models_to_compare}
                
                # Ejecutar simulaciones
                results = compare_models(
                    models_to_run, 
                    N=controls['N'],
                    K=controls['K'],
                    steps=controls['steps'],
                    dt=controls['dt'],
                    omega_mean=controls['omega_mean'],
                    omega_std=controls['omega_std']
                )
                
                # Mostrar resultados
                display_main_metrics(results)
                display_visualizations(results, controls['dt'])
                display_diagnostic_info(results)
                
            except Exception as e:
                st.error(f"❌ Error durante la simulación: {str(e)}")
                st.code(traceback.format_exc())
                st.info("""
                **Solución de problemas:**
                1. Ejecuta `python test_correction.py` para verificar los modelos
                2. Revisa que todos los archivos en `src/` estén presentes
                3. Reduce el número de osciladores o pasos si hay problemas de memoria
                """)
    else:
        display_instructions()

if __name__ == "__main__":
    main()