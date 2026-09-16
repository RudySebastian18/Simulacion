import random
import time

def simulacion_clasificacion_kr(total_botellas):
    # Tipos de botellas y contadores iniciales
    sabores = ["KR Roja (Fresa)", "KR Amarilla (Piña)", "KR Negra (Cola)"]
    carriles = {"KR Roja (Fresa)": 0, "KR Amarilla (Piña)": 0, "KR Negra (Cola)": 0}
    
    print("--- INICIANDO LÍNEA AUTOMATIZADA KOLA REAL ---")
    
    for i in range(1, total_botellas + 1):
        # Simulamos que la KR Negra tiene mayor volumen de producción (40%)
        botella = random.choices(sabores, weights=[30, 30, 40])[0]
        
        print(f"[Sensor] Botella {i} ingresa a la faja principal.")
        time.sleep(0.3) # Simula el tiempo de transporte
        
        print(f" -> [Cámara IA] Detecta color. Clasificación: {botella}")
        time.sleep(0.2) # Simula el tiempo de procesamiento de imagen
        
        print(f" -> [Arduino] Activando servomotor. Desviando a carril correspondiente...\n")
        carriles[botella] += 1
        
    print("--- REPORTE DE PRODUCCIÓN (FIN DE LOTE) ---")
    for sabor, cantidad in carriles.items():
        print(f"Total {sabor} empaquetadas: {cantidad} unidades")

# Ejecutar simulación para un lote de prueba de 15 botellas
simulacion_clasificacion_kr(15)
