import matplotlib
matplotlib.use("TkAgg")
import serial
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
PORT = "/dev/cu.usbserial-14340" 
BAUD = 115200
MUESTRAS = 100

# 1. DEFINIR LA DISTANCIA FIJA (Mídela con regla)
DISTANCIA_REAL_CM = 9.2  # <--- CAMBIA ESTO A TU DISTANCIA REAL (ej. 30 cm)
DISTANCIA_REAL_M = DISTANCIA_REAL_CM / 100.0

ser = serial.Serial(PORT, BAUD)

velocidades_calculadas = []

print(f"--- CALIBRACIÓN DE VELOCIDAD ---")
print(f"Distancia fija configurada: {DISTANCIA_REAL_CM} cm")
print(f"Tomando {MUESTRAS} muestras...")

# Esperar READY
while True:
    try:
        if "READY" in ser.readline().decode(): break
    except: pass

plt.ion()
fig, ax = plt.figure(figsize=(8, 5)), plt.gca()
plt.show(block=False)

while len(velocidades_calculadas) < MUESTRAS:
    try:
        line = ser.readline().decode().strip()
        if "," not in line: continue

        # Solo nos importa el TIEMPO (t_echo)
        # El Arduino manda: t_echo, dist_arduino
        parts = line.split(",")
        t_us = float(parts[0]) 
        
        # Convertir a segundos
        t_sec = t_us / 1_000_000.0
        
        if t_sec <= 0: continue

        # CÁLCULO FÍSICO REAL: v = 2d / t
        v_inst = (2 * DISTANCIA_REAL_M) / t_sec
        
        # Filtro de ruido (el sonido no viaja a 1000 m/s ni a 0 m/s)
        if 300 < v_inst < 400:
            velocidades_calculadas.append(v_inst)
            
            # Graficar en tiempo real
            ax.clear()
            ax.plot(velocidades_calculadas, 'o-', markersize=4, label='Medición Instantánea')
            
            # Calcular promedio actual
            promedio = np.mean(velocidades_calculadas)
            ax.axhline(promedio, color='r', linestyle='--', label=f'Promedio: {promedio:.2f} m/s')
            
            ax.set_title(f"Calibrando... Muestra {len(velocidades_calculadas)}/{MUESTRAS}")
            ax.set_ylabel("Velocidad Calculada (m/s)")
            ax.set_xlabel("Número de Muestra")
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.pause(0.01)

    except ValueError:
        pass

ser.close()

# --- RESULTADO FINAL ---
vel_final = np.mean(velocidades_calculadas)
std_dev = np.std(velocidades_calculadas)
temp_estimada = (vel_final - 331.4) / 0.6

print("\n" + "="*40)
print(f"RESULTADOS DEL ANÁLISIS")
print(f"="*40)
print(f"Velocidad Promedio medida: {vel_final:.2f} m/s")
print(f"Desviación Estándar (Ruido): +/- {std_dev:.2f} m/s")
print(f"Temperatura ambiente estimada: ~{temp_estimada:.1f} °C")
print(f"="*40)
print("Usa este valor de velocidad en tu código Arduino.")

plt.ioff()
plt.show()