#include <Servo.h>

Servo servo;

const int TRIG = 9;
const int ECHO = 10;
const int SERVO_PIN = 6;

unsigned long t;
float distance;

void setup() {
  Serial.begin(115200);

  servo.attach(SERVO_PIN);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  Serial.println("READY");
}

unsigned long measureEcho() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  return pulseIn(ECHO, HIGH, 30000); // timeout 30ms
}

void loop() {
  for (int ang = 0; ang <= 180; ang++) {
    servo.write(ang);
    delay(70);

    unsigned long t = measureEcho();
    float d = (t * 1e-6 *  348.02 / 2.0); // metros

    Serial.print(ang);
    Serial.print(",");
    Serial.println(d);

    delay(50);
  }
}
