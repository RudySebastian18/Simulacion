import streamlit as st
import random
import time
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Simulador Kola Real", layout="centered")

st.title("🏭 Simulación de Clasificación - Kola Real")
st.markdown("Panel de control interactivo para la línea automatizada con visión artificial.")

# Control de variables de entrada
total_botellas = st.slider("Cantidad de botellas en el lote:", min_value=5, max_value=100, value=15)

# Botón para iniciar el proceso
if st.button("Iniciar Simulación", type="primary"):
    
    sabores = ["KR Roja (Fresa)", "KR Amarilla (Piña)", "KR Negra (Cola)"]
    carriles = {"KR Roja (Fresa)": 0, "KR Amarilla (Piña)": 0, "KR Negra (Cola)": 0}
    
    # Elementos visuales que se actualizarán en tiempo real
    barra_progreso = st.progress(0)
    estado_texto = st.empty()
    
    st.markdown("### Contadores en Tiempo Real")
    col1, col2, col3 = st.columns(3)
    metrica_roja = col1.empty()
    metrica_amarilla = col2.empty()
    metrica_negra = col3.empty()
    
    # Inicializar contadores en 0
    metrica_roja.metric("Carril A (Fresa)", 0)
    metrica_amarilla.metric("Carril B (Piña)", 0)
    metrica_negra.metric("Carril C (Cola)", 0)
    
    st.divider()
    
    # Bucle de simulación
    for i in range(1, total_botellas + 1):
        # Probabilidad de producción (KR Negra tiene mayor demanda)
        botella = random.choices(sabores, weights=[30, 30, 40])[0]
        
        # Fase 1: Ingreso
        estado_texto.info(f"Botella {i}/{total_botellas} en faja principal. [Esperando cámara...]")
        time.sleep(0.3)
        
        # Fase 2: Detección y Desvío
        estado_texto.warning(f"📷 Cámara IA detecta: **{botella}**. Activando servomotor...")
        carriles[botella] += 1
        
        # Actualizar métricas dinámicamente
        metrica_roja.metric("Carril A (Fresa)", carriles["KR Roja (Fresa)"])
        metrica_amarilla.metric("Carril B (Piña)", carriles["KR Amarilla (Piña)"])
        metrica_negra.metric("Carril C (Cola)", carriles["KR Negra (Cola)"])
        
        # Actualizar barra de progreso
        barra_progreso.progress(i / total_botellas)
        time.sleep(0.3)
        
    estado_texto.success("✅ ¡Lote clasificado con éxito!")
    
    # Generar tabla final
    st.markdown("### Reporte Final de Lote")
    df_resultados = pd.DataFrame(
        list(carriles.items()), 
        columns=["Producto Detectado", "Unidades Empaquetadas"]
    )
    st.dataframe(df_resultados, use_container_width=True)
