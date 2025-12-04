const int TRIG = 9;
const int ECHO = 10;

void setup() {
  Serial.begin(115200);
  delay(500); // tiempo para estabilizar USB y Python

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  Serial.println("READY"); // Python espera este mensaje
}

void loop() {
  // Enviar pulso
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  // Leer eco con timeout de 30ms
  unsigned long t_echo = pulseIn(ECHO, HIGH, 30000);

  // Calcular distancia en cm
  float distancia = (t_echo * 1e-6 * 344.30 ) / 2.0;
  float distancia_cm = distancia * 100.0;

  // ---- Salida en CSV para Python ----
  Serial.print(t_echo);
  Serial.print(",");
  Serial.println(distancia_cm);

  delay(100); // lectura estable, 10 Hz
}

