import matplotlib
matplotlib.use("TkAgg")   # <- Fuerza backend con ventanas en Mac

import serial
import time
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# CONFIGURACIÓN DEL PUERTO
# ----------------------------
PORT = "/dev/cu.usbserial-14340"    # Linux / Mac
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)

# Esperar el mensaje "READY" del Arduino
print("Esperando Arduino...")
while True:
    line = ser.readline().decode().strip()
    if line == "READY":
        print("Arduino listo.")
        break

# ----------------------------
# INICIALIZAR FIGURA
# ----------------------------
plt.ion()
fig, ax = plt.subplots(figsize=(7,5))
plt.show(block=False)

tiempos = []
distancias = []
t0 = time.time()

linea, = ax.plot([], [], 'o', markersize=4)
recta, = ax.plot([], [], 'r-', linewidth=2)

ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Distancia (cm)")
ax.set_title("Medición en vivo: distancia vs. tiempo")

# ----------------------------
# LECTURA EN TIEMPO REAL
# ----------------------------
while True:
    raw = ser.readline().decode().strip()
    if "," not in raw:
        continue

    try:
        t_echo_raw, dist_cm_raw = raw.split(",")
        t_echo = int(t_echo_raw)
        dist_cm = float(dist_cm_raw)
    except:
        continue

    # Tiempo relativo desde que empezó el experimento
    t = time.time() - t0

    tiempos.append(t)
    distancias.append(dist_cm)

    # Actualizar puntos
    linea.set_xdata(tiempos)
    linea.set_ydata(distancias)

    # Ajuste lineal si hay suficientes puntos
    

    ax.relim()
    ax.autoscale_view()
    plt.pause(0.01)
