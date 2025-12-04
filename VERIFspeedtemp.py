import matplotlib
matplotlib.use("TkAgg")
import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats  # Para el ajuste lineal fiable

# --- CONFIGURACIÓN ---
PORT = "/dev/cu.usbserial-14340"  # Revisa que sea tu puerto correcto
BAUD = 115200
MUESTRAS_MAX = 100  # Cantidad de datos a tomar

ser = serial.Serial(PORT, BAUD)

# Listas para guardar datos
tiempos_vuelo = []   # Eje X
distancias = []      # Eje Y

print(f"--- INICIANDO EXPERIMENTO ---")
print(f"Voy a tomar {MUESTRAS_MAX} mediciones.")
print("IMPORTANTE: Mueve el objeto o el sensor a diferentes distancias")
print("mientras ves la barra de progreso para generar una recta.")
print("-----------------------------")

# Esperar al READY del Arduino
while True:
    try:
        line = ser.readline().decode().strip()
        if "READY" in line:
            print("Arduino listo. Comenzando captura...")
            break
    except:
        pass

# --- BUCLE DE CAPTURA ---
while len(tiempos_vuelo) < MUESTRAS_MAX:
    try:
        line = ser.readline().decode().strip()
        if "," not in line:
            continue

        # Arduino envía: t_echo (us), distancia (cm)
        parts = line.split(",")
        t_us = float(parts[0])
        d_cm = float(parts[1])

        # FILTRO: Ignorar lecturas erróneas (0 o muy lejanas)
        if d_cm <= 0 or d_cm > 400:
            continue

        # CONVERSIÓN A SISTEMA INTERNACIONAL (Metros y Segundos)
        # Eje X: Tiempo total de vuelo en segundos
        t_sec = t_us / 1_000_000.0  
        
        # Eje Y: Distancia en metros (esto es lo que reporta Arduino)
        d_met = d_cm / 100.0        

        tiempos_vuelo.append(t_sec)
        distancias.append(d_met)

        # Barra de progreso simple
        progreso = len(tiempos_vuelo)
        print(f"Capturando: {progreso}/{MUESTRAS_MAX} | Dist: {d_cm} cm", end="\r")

    except ValueError:
        pass

print("\n\nCaptura terminada. Calculando regresión...")
ser.close() # Liberamos el puerto

# --- ANÁLISIS DE DATOS ---
x = np.array(tiempos_vuelo)
y = np.array(distancias)

# Regresión Lineal (y = mx + b)
# slope: pendiente (m)
# intercept: intersección (b)
res = stats.linregress(x, y)
m = res.slope
b = res.intercept
r_sq = res.rvalue**2  # Coeficiente de determinación (qué tan recta es la línea)

# --- FÍSICA DETRÁS DEL CÁLCULO ---
# Fórmula física: Distancia = (Velocidad * Tiempo) / 2
# Reordenando:    Distancia = (Velocidad / 2) * Tiempo
#
# Nuestra Ecuación de la recta es: y = m * x + b
# Donde 'y' es Distancia y 'x' es Tiempo.
# Por lo tanto, la pendiente 'm' equivale a (Velocidad / 2).
#
# Entonces: Velocidad = 2 * pendiente

velocidad_calculada = m * 2

# --- GRAFICAR ---
plt.figure(figsize=(10, 6))

# 1. Puntos originales (Datos)
plt.scatter(x, y, label='Datos medidos', color='blue', alpha=0.6, s=20)

# 2. Línea de ajuste (Regresión)
plt.plot(x, m*x + b, color='red', label=f'Ajuste Lineal (R²={r_sq:.4f})')

# Textos informativos
texto_resultado = (
    f"Pendiente (m): {m:.2f} m/s (es v/2)\n"
    f"Velocidad Sonido Calculada: {velocidad_calculada:.2f} m/s\n"
    f"Ecuación: d = {m:.2f}t + {b:.3f}"
)

# Añadir cuadro de texto al gráfico
plt.text(0.05, 0.95, texto_resultado, transform=plt.gca().transAxes,
         fontsize=12, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

#plt.title("Cálculo Experimental de la Velocidad del Sonido")
plt.xlabel("Tiempo de Vuelo del Eco [s]")
plt.ylabel("Distancia reportada [m]")
#plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.show()