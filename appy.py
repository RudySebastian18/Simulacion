import streamlit as st
import random
import time

# Configuración básica de la página web
st.set_page_config(page_title="Simulador KR", layout="centered")

st.title("🏭 Simulación Web - Clasificación Kola Real")
st.markdown("Primera versión interactiva (V1) del prototipo de visión artificial.")

# Controles en la barra lateral
st.sidebar.header("Panel de Control")
total_botellas = st.sidebar.slider("Cantidad de botellas:", 1, 20, 5)
velocidad = st.sidebar.slider("Velocidad de faja:", 0.05, 0.5, 0.1)

# Botón para iniciar
if st.button("▶️ Iniciar Simulación en Vivo", type="primary"):
    
    # Variables y contadores
    carriles = {"Fresa": 0, "Piña": 0, "Cola": 0}
    iconos = {"Fresa": "🔴", "Piña": "🟡", "Cola": "⚫"}
    sabores = list(iconos.keys())
    
    # Interfaz de contadores
    st.markdown("### 📦 Cajas Empaquetadas (Six-Packs)")
    col1, col2, col3 = st.columns(3)
    metrica_roja = col1.empty()
    metrica_amarilla = col2.empty()
    metrica_negra = col3.empty()
    
    # Inicializar contadores en la pantalla
    metrica_roja.metric("Carril A (Fresa)", 0)
    metrica_amarilla.metric("Carril B (Piña)", 0)
    metrica_negra.metric("Carril C (Cola)", 0)
    
    st.divider()
    
    # Espacios para la animación
    st.markdown("### ⚙️ Faja Transportadora Principal")
    faja_visual = st.empty()
    estado_camara = st.empty()
    
    # Bucle de la producción de botellas
    for i in range(1, total_botellas + 1):
        # Elegir botella aleatoria (KR Negra sale con más frecuencia)
        botella_actual = random.choices(sabores, weights=[30, 30, 40])[0]
        icono = iconos[botella_actual]
        
        # Animación de la botella avanzando (10 pasos)
        for paso in range(11):
            # Construir visualmente la faja: [Inicio] -- botella -- [Fin]
            faja = ["➖"] * 11
            faja[paso] = icono
            faja_str = "".join(faja)
            
            # Hacer el texto grande para que se vea como un gráfico
            faja_html = f"<h1 style='text-align: center; letter-spacing: 10px;'>🏭{faja_str}⬇️</h1>"
            faja_visual.markdown(faja_html, unsafe_allow_html=True)
            
            # Lógica de la cámara (ubicada a la mitad de la faja, paso 5)
            if paso < 5:
                estado_camara.info("⚪ Sensor IA en espera...")
            elif paso == 5:
                estado_camara.warning(f"📸 ¡Cámara detecta botella de **{botella_actual}**!")
            else:
                estado_camara.success("✅ Servomotor desviando botella al carril...")
            
            # Pausa para crear el efecto de movimiento
            time.sleep(velocidad)
            
        # Al llegar al final de la faja, sumar al contador
        carriles[botella_actual] += 1
        
        # Actualizar las tarjetas de los contadores numéricos
        metrica_roja.metric("Carril A (Fresa)", carriles["Fresa"])
        metrica_amarilla.metric("Carril B (Piña)", carriles["Piña"])
        metrica_negra.metric("Carril C (Cola)", carriles["Cola"])
        
    estado_camara.success("🎉 ¡Lote finalizado y clasificado exitosamente!")
    st.balloons() # Animación final
