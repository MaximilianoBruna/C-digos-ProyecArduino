import matplotlib
matplotlib.use("TkAgg")

import serial
import numpy as np
import matplotlib.pyplot as plt

PORT = "/dev/cu.usbserial-14340"
BAUD = 115200

ser = serial.Serial(PORT, BAUD)

# Esperar el READY inicial
while True:
    line = ser.readline().decode().strip()
    if "READY" in line:
        break

plt.ion()
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection="polar")
plt.show(block=False)

angles = []
distances = []

last_angle = None

while True:
    line = ser.readline().decode().strip()
    if "," not in line:
        continue

    ang, dist = line.split(",")
    ang = float(ang)
    dist = float(dist)

    # ----------- REINICIAR ARRAY CUANDO VUELVE A 0° -----------
    # Esto detecta el reinicio del barrido
    if last_angle is not None:
        if last_angle > 150 and ang < 30:
            angles = []
            distances = []

    last_angle = ang

    # Guardar valores
    angles.append(np.radians(ang))
    distances.append(dist)

# ... código anterior ...
    
    ax.clear()
    ax.scatter(angles, distances, s=15)
    ax.set_title("Sonar en tiempo real")
    
    # --- CAMBIO AQUÍ ---
    ax.set_theta_zero_location("W")      # 0° en el Oeste (Izquierda)
    ax.set_theta_direction(-1)           # Sentido horario (Clockwise)
    # -------------------

    plt.pause(0.0001)


